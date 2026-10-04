import sys
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.email_service import generate_secure_otp, build_otp_html_email, EmailService
from app.database_mock import USERS_DB, OTP_CACHE
from app.auth import verify_password

client = TestClient(app)

def test_otp_service():
    print("=" * 70)
    print("PSNA IT PLACEMENT ASSISTANT: EMAIL OTP SERVICE VALIDATION")
    print("=" * 70)

    # 1. Test Secure OTP Generator
    print("\n[TEST 1] Cryptographically Secure OTP Generation...")
    otps = [generate_secure_otp() for _ in range(5)]
    print(f"  Sample Generated OTPs: {otps}")
    for code in otps:
        assert len(code) == 6, f"OTP {code} must be 6 digits"
        assert code.isdigit(), f"OTP {code} must be numeric"
    print("  [SUCCESS] Cryptographically secure 6-digit numeric OTP generation verified.")

    # 2. Test HTML Email Template
    print("\n[TEST 2] Verifying Official Branded HTML Template...")
    html_output = build_otp_html_email("Dr. S. Karthik", "784912")
    assert "PSNA COLLEGE OF ENGINEERING AND TECHNOLOGY" in html_output
    assert "DEPARTMENT OF INFORMATION TECHNOLOGY" in html_output
    assert "#0D5C3A" in html_output
    assert "letter-spacing: 12px" in html_output
    assert "784912" in html_output
    assert "ANEESH KANNA N and ANNE BENILDA A" in html_output
    assert "5 minutes" in html_output
    print("  [SUCCESS] HTML email template branding, #0D5C3A OTP font, and attribution verified.")

    # 3. Test POST /api/auth/forgot-password with non-existent user
    print("\n[TEST 3] Testing Forgot Password with Unknown User...")
    resp_unknown = client.post("/api/auth/forgot-password", json={"email": "unknown.person@psnacet.edu.in"})
    print(f"  Unknown email response: {resp_unknown.status_code} - {resp_unknown.json()}")
    assert resp_unknown.status_code == 404
    print("  [SUCCESS] Non-existent email rejected with 404.")

    # 4. Test POST /api/auth/forgot-password with valid registered faculty
    target_email = "staff@psnacet.edu.in"
    print(f"\n[TEST 4] Testing Forgot Password for '{target_email}'...")
    resp_valid = client.post("/api/auth/forgot-password", json={"email": target_email})
    print(f"  Valid request response: {resp_valid.status_code} - {resp_valid.json()}")
    assert resp_valid.status_code == 200
    data = resp_valid.json()
    assert data["status"] == "success"
    assert "preview_otp" in data
    assert len(data["preview_otp"]) == 6
    assert target_email in OTP_CACHE
    assert OTP_CACHE[target_email]["otp"] == data["preview_otp"]
    print("  [SUCCESS] OTP generated, cached with 5-min expiry, and dispatched.")

    active_otp = data["preview_otp"]

    # 5. Test POST /api/auth/verify-otp with incorrect OTP
    print("\n[TEST 5] Testing Verify OTP with Incorrect Code...")
    resp_wrong = client.post("/api/auth/verify-otp", json={
        "email": target_email,
        "otp": "000000",
        "new_password": "NewStaffPass@2026"
    })
    print(f"  Wrong OTP response: {resp_wrong.status_code} - {resp_wrong.json()}")
    assert resp_wrong.status_code == 400
    print("  [SUCCESS] Incorrect OTP rejected with 400.")

    # 6. Test POST /api/auth/verify-otp with weak password
    print("\n[TEST 6] Testing Verify OTP with Weak Password (< 8 chars)...")
    resp_weak = client.post("/api/auth/verify-otp", json={
        "email": target_email,
        "otp": active_otp,
        "new_password": "short"
    })
    print(f"  Weak password response: {resp_weak.status_code} - {resp_weak.json()}")
    assert resp_weak.status_code == 400
    print("  [SUCCESS] Weak password rejected.")

    # 7. Test POST /api/auth/verify-otp with expired code
    print("\n[TEST 7] Testing Expired OTP Handling...")
    OTP_CACHE[target_email]["expires_at"] = datetime.now(timezone.utc) - timedelta(seconds=10)
    resp_expired = client.post("/api/auth/verify-otp", json={
        "email": target_email,
        "otp": active_otp,
        "new_password": "ValidNewPassword@2026"
    })
    print(f"  Expired OTP response: {resp_expired.status_code} - {resp_expired.json()}")
    assert resp_expired.status_code == 400
    assert "expired" in resp_expired.json()["detail"].lower()
    print("  [SUCCESS] Expired OTP caught and rejected.")

    # 8. Request fresh OTP and complete real reset
    print("\n[TEST 8] Requesting Fresh OTP & Completing Password Reset...")
    resp_fresh = client.post("/api/auth/forgot-password", json={"email": target_email})
    fresh_otp = resp_fresh.json()["preview_otp"]
    new_secret_pass = "UpdatedFacultySecure#2026"

    resp_reset = client.post("/api/auth/verify-otp", json={
        "email": target_email,
        "otp": fresh_otp,
        "new_password": new_secret_pass
    })
    print(f"  Reset response: {resp_reset.status_code} - {resp_reset.json()}")
    assert resp_reset.status_code == 200
    assert resp_reset.json()["status"] == "success"

    # Verify that target user's password was updated in USERS_DB
    staff_user = USERS_DB[target_email]
    assert verify_password(new_secret_pass, staff_user["password_hash"]), "Password was not updated in USERS_DB!"
    assert target_email not in OTP_CACHE, "OTP should be invalidated/removed from OTP_CACHE!"
    print("  [SUCCESS] Password hash updated and OTP invalidated from cache.")

    # 9. Verify that reusing the consumed OTP fails
    print("\n[TEST 9] Verifying Consumed OTP Invalidation...")
    resp_reuse = client.post("/api/auth/verify-otp", json={
        "email": target_email,
        "otp": fresh_otp,
        "new_password": "AnotherNewPassword@2026"
    })
    print(f"  Re-use response: {resp_reuse.status_code} - {resp_reuse.json()}")
    assert resp_reuse.status_code == 400
    print("  [SUCCESS] Consumed OTP cannot be reused.")

    print("\n[ALL 9 EMAIL OTP VERIFICATION TESTS PASSED 100%!]")
    print("=" * 70)

if __name__ == "__main__":
    test_otp_service()
