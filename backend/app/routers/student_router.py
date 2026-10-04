from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict
from datetime import datetime, timezone
import random

from app.auth import get_current_user, require_roles
from app.models import CorrectionRequestCreate
from app.database_mock import STUDENTS_DB, CORRECTION_REQUESTS, get_privacy_masked_peers

router = APIRouter(prefix="/api/student", tags=["Student Portal & Privacy Masking"])

@router.get("/profile")
def get_student_profile(current_user: Dict = Depends(require_roles(["STUDENT"]))):
    """
    Returns the authenticated student's full academic profile.
    Reflects the Data Freezing Gate status (is_locked = True).
    """
    reg_no = current_user.get("sub")
    profile = STUDENTS_DB.get(reg_no)

    if not profile:
        # Fallback profile if registered during active session
        profile = {
            "register_no": reg_no,
            "roll_no": f"21IT{random.randint(10, 99)}",
            "name": current_user.get("name", "Student"),
            "gender": "Male",
            "department": current_user.get("department", "IT"),
            "year": current_user.get("year", "IV"),
            "section": current_user.get("section", "A"),
            "email": current_user.get("email", ""),
            "mobile": "9876543210",
            "cgpa": 8.72,
            "active_arrears": 0,
            "history_arrears": 0,
            "attendance": 94.5,
            "is_locked": True, # Data Freezing Gate
            "skills": ["Python", "React", "SQL"],
            "eligibility": "Eligible",
            "placement_status": "Not Placed",
            "company": None,
            "package_lpa": 0.0,
            "resume_url": "#",
            "semesters": {
                1: {"gpa": 8.45, "arrears": 0, "official_credits": 22.0},
                2: {"gpa": 8.60, "arrears": 0, "official_credits": 25.0},
                3: {"gpa": 8.75, "arrears": 0, "official_credits": 22.5},
                4: {"gpa": 8.80, "arrears": 0, "official_credits": 22.5},
                5: {"gpa": 8.90, "arrears": 0, "official_credits": 22.5},
                6: {"gpa": 8.85, "arrears": 0, "official_credits": 21.0},
            }
        }
        STUDENTS_DB[reg_no] = profile

    return profile

@router.get("/peers")
def get_section_peers(current_user: Dict = Depends(require_roles(["STUDENT"]))):
    """
    Section-Segregated Peer Directory API:
    - Reads the logged-in student's Year and Section.
    - Exposes ONLY peers from their own batch/section (e.g. 4th Year Section A).
    - Enforces Privacy Masking Rule: Exposes Name, Reg No, Roll No, Email, Mobile, Resume Link.
    - STRICTLY MASKS: CGPA, subject marks, and backlog histories are hidden!
    """
    year = current_user.get("year", "IV")
    section = current_user.get("section", "A")

    peers = get_privacy_masked_peers(year=year, section=section)
    return {
        "filtered_year": year,
        "filtered_section": section,
        "privacy_masking_applied": True,
        "total_peers_found": len(peers),
        "peers": peers
    }

@router.post("/request-correction", status_code=status.HTTP_201_CREATED)
def request_profile_correction(
    payload: CorrectionRequestCreate,
    current_user: Dict = Depends(require_roles(["STUDENT"]))
):
    """
    Data Freezing Gate & Permission Workflow:
    Because student profiles are locked upon submission, direct editing is prevented.
    Students trigger this digital correction request, which queues for Class Tutor / Incharge review.
    """
    request_id = len(CORRECTION_REQUESTS) + 1
    req = {
        "request_id": request_id,
        "register_no": payload.register_no,
        "student_name": current_user.get("name", "Student"),
        "year": current_user.get("year", "IV"),
        "section": current_user.get("section", "A"),
        "requested_field": payload.requested_field,
        "new_value": payload.new_value,
        "reason": payload.reason,
        "status": "PENDING",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    CORRECTION_REQUESTS.append(req)

    return {
        "message": "Digital permission request registered successfully. Awaiting Class Tutor / Incharge audit.",
        "request": req
    }

@router.get("/correction-requests")
def get_student_correction_requests(current_user: Dict = Depends(require_roles(["STUDENT"]))):
    """Lists all permission requests submitted by the logged-in student."""
    reg_no = current_user.get("sub")
    my_requests = [r for r in CORRECTION_REQUESTS if r.get("register_no") == reg_no]
    return {
        "total_requests": len(my_requests),
        "requests": my_requests
    }
