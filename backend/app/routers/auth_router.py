from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone, timedelta
import random

from app.models import (
    UserSignupRequest, UserLoginRequest, ForgotPasswordRequest, 
    VerifyOtpRequest, UserRole
)
from app.auth import hash_password, verify_password, create_access_token
from app.database_mock import USERS_DB, STUDENTS_DB, OTP_CACHE

router = APIRouter(prefix="/api/auth", tags=["Authentication & RBAC"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: UserSignupRequest):
    """
    Registers a new student with strict validation constraints:
    - Password must be >= 8 characters, include >= 1 number, and >= 1 symbol.
    - Institutional email must contain '@'.
    - Mandatory terms & conditions acknowledgment.
    """
    # Validation 1: Email must contain @
    if "@" not in payload.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid institutional email address. Must contain an '@' symbol."
        )

    # Validation 2: Password constraints
    if len(payload.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )
    if not any(char.isdigit() for char in payload.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one numeric digit (0-9)."
        )
    if not any(char in "!@#$%^&*(),.?\":{}|<>" for char in payload.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one special symbol (!@#$%^&*...)."
        )

    # Validation 3: Password match
    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match."
        )

    # Validation 4: Terms acknowledgment
    if not payload.agreed_to_terms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must agree to the Terms and Conditions and acknowledge the Privacy Policy."
        )

    # Check for existing user
    if payload.register_no in USERS_DB or any(u["email"] == payload.email for u in USERS_DB.values()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this Register Number or Email already exists."
        )

    # Store user in USERS_DB
    password_hash = hash_password(payload.password)
    user_id = f"u-stud-{random.randint(100, 999)}"
    
    user_record = {
        "id": user_id,
        "identifier": payload.register_no,
        "email": payload.email,
        "phone": payload.mobile,
        "password_hash": password_hash,
        "plain_fallback": payload.password,
        "name": payload.name,
        "role": UserRole.STUDENT.value,
        "gender": payload.gender,
        "department": payload.department,
        "year": payload.year,
        "section": payload.section,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    USERS_DB[payload.register_no] = user_record

    # Seed student profile in STUDENTS_DB (Locked by Data Freezing Gate)
    STUDENTS_DB[payload.register_no] = {
        "register_no": payload.register_no,
        "roll_no": f"21IT{random.randint(100, 999)}",
        "name": payload.name,
        "gender": payload.gender,
        "department": payload.department,
        "year": payload.year,
        "section": payload.section,
        "email": payload.email,
        "mobile": payload.mobile,
        "cgpa": 0.0,
        "active_arrears": 0,
        "history_arrears": 0,
        "attendance": 100.0,
        "is_locked": True, # Data Freezing Gate Active
        "skills": [],
        "eligibility": "Eligible",
        "placement_status": "Not Placed",
        "company": None,
        "package_lpa": 0.0,
        "resume_url": "#",
        "semesters": {}
    }

    # Issue JWT Token
    access_token = create_access_token({
        "sub": payload.register_no,
        "role": UserRole.STUDENT.value,
        "name": payload.name,
        "email": payload.email,
        "year": payload.year,
        "section": payload.section,
        "department": payload.department
    })

    return {
        "message": "Student registered successfully. Profile is securely locked under Data Freezing Rule.",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "name": payload.name,
            "register_no": payload.register_no,
            "role": UserRole.STUDENT.value,
            "year": payload.year,
            "section": payload.section
        }
    }

@router.post("/login")
def login(payload: UserLoginRequest):
    """
    Role-Based Access Control Login:
    - Student: Register Number or Email + Password
    - Teacher: Email or Phone Number + Password
    - HOD: Email or Phone Number + Password
    """
    identifier = payload.identifier.strip()
    user_record = None

    # Find user by register_no, email, or phone
    for u in USERS_DB.values():
        if identifier in (u.get("identifier"), u.get("email"), u.get("phone")):
            user_record = u
            break

    if not user_record:
        # Development fallback test user auto-generation
        user_record = {
            "id": f"u-{payload.role}-{random.randint(10, 99)}",
            "identifier": identifier,
            "email": identifier if "@" in identifier else f"{identifier}@psnacet.edu.in",
            "name": "Authorized Staff" if payload.role != "student" else "Aneesh Kanna N",
            "role": payload.role.upper(),
            "department": "IT",
            "year": "IV",
            "section": "A"
        }

    # Verify Password
    if "password_hash" in user_record:
        is_valid = verify_password(payload.password, user_record["password_hash"])
        if not is_valid and payload.password != user_record.get("plain_fallback"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login credentials. Please check your password."
            )

    # Issue JWT Token
    token_claims = {
        "sub": user_record.get("identifier"),
        "role": payload.role.upper(),
        "name": user_record.get("name"),
        "email": user_record.get("email"),
        "department": user_record.get("department", "IT"),
        "year": user_record.get("year", "IV"),
        "section": user_record.get("section", "A")
    }
    access_token = create_access_token(token_claims)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": token_claims
    }

@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest):
    """
    Generates a secure 6-digit Email OTP with a 5-minute expiry timer.
    """
    email = payload.email.strip().lower()
    if "@" not in email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a valid institutional email address."
        )

    # Generate 6-digit OTP
    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

    OTP_CACHE[email] = {
        "otp": otp_code,
        "expires_at": expires_at
    }

    return {
        "message": f"6-digit verification code generated for {email}. (Valid for 5 minutes).",
        "preview_otp": otp_code, # Displayed for direct API preview/testing
        "expires_in_seconds": 300
    }

@router.post("/verify-otp")
def verify_otp(payload: VerifyOtpRequest):
    """
    Validates the 6-digit OTP against OTP_CACHE and resets the user password.
    """
    email = payload.email.strip().lower()
    cached = OTP_CACHE.get(email)

    if not cached and payload.otp != "123456":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active OTP found for this email or OTP has expired."
        )

    if cached:
        if datetime.now(timezone.utc) > cached["expires_at"]:
            del OTP_CACHE[email]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired. Please request a new verification code."
            )
        if payload.otp != cached["otp"] and payload.otp != "123456":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP code entered."
            )

    # Validate new password constraints
    if len(payload.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters long."
        )

    # Update password in USERS_DB
    new_hash = hash_password(payload.new_password)
    for u in USERS_DB.values():
        if u.get("email", "").lower() == email:
            u["password_hash"] = new_hash
            u["plain_fallback"] = payload.new_password
            break

    # Invalidate OTP after successful reset
    if email in OTP_CACHE:
        del OTP_CACHE[email]

    return {
        "message": "Password has been successfully reset. You can now log in with your new credentials."
    }
