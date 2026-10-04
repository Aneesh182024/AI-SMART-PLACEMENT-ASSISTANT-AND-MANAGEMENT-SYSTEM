"""
PSNA College of Engineering and Technology, Dindigul
Department of Information Technology
Authentication & Login Strict Verification Test Suite
Developed by: ANEESH KANNA N and ANNE BENILDA A
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_strict_login_validation():
    print("=================================================================")
    print("RUNNING STRICT LOGIN VALIDATION & DATABASE AUTHENTICATION TESTS")
    print("=================================================================\n")

    # TEST 1: Blank / Empty credentials
    print("1. Testing empty credentials...")
    resp = client.post("/api/auth/login", json={"email": "", "password": ""})
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    assert resp.status_code == 401, f"Expected 401, got {resp.status_code}"
    assert resp.json().get("detail") == "Invalid Email or Password! Account illai endral register seiyavum."
    print("   [PASS] Empty credentials strictly rejected with Tamil warning message.\n")

    # TEST 2: Non-existent email (User not in database)
    print("2. Testing non-existent user email...")
    resp = client.post("/api/auth/login", json={
        "email": "ghost.student@psnacet.edu.in",
        "password": "Password@123"
    })
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    assert resp.status_code == 401, f"Expected 401, got {resp.status_code}"
    assert resp.json().get("detail") == "Invalid Email or Password! Account illai endral register seiyavum."
    print("   [PASS] Non-existent user strictly rejected with 401.\n")

    # TEST 3: Existing user with WRONG password
    print("3. Testing existing user with WRONG password...")
    resp = client.post("/api/auth/login", json={
        "email": "staff@psnacet.edu.in",
        "password": "WrongPassword999!"
    })
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    assert resp.status_code == 401, f"Expected 401, got {resp.status_code}"
    assert resp.json().get("detail") == "Invalid Email or Password! Account illai endral register seiyavum."
    print("   [PASS] Invalid password strictly rejected with 401.\n")

    # TEST 4: Valid Student Credentials
    print("4. Testing VALID student login (713821104001@psnacet.edu.in)...")
    resp = client.post("/api/auth/login", json={
        "email": "713821104001@psnacet.edu.in",
        "password": "Student@123"
    })
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "success", "Expected status: success"
    assert data.get("role") == "student", f"Expected role 'student', got {data.get('role')}"
    assert data.get("token") is not None, "Expected valid token"
    print(f"   [PASS] Student authenticated successfully with role '{data.get('role')}'.\n")

    # TEST 5: Valid Teacher Credentials
    print("5. Testing VALID teacher login (staff@psnacet.edu.in)...")
    resp = client.post("/api/auth/login", json={
        "email": "staff@psnacet.edu.in",
        "password": "Teacher@123"
    })
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "success", "Expected status: success"
    assert data.get("role") == "teacher", f"Expected role 'teacher', got {data.get('role')}"
    assert data.get("token") is not None, "Expected valid token"
    print(f"   [PASS] Teacher authenticated successfully with role '{data.get('role')}'.\n")

    # TEST 6: Valid Student by Register Number
    print("6. Testing VALID student login using register number (713821104001)...")
    resp = client.post("/api/auth/login", json={
        "identifier": "713821104001",
        "password": "Student@123"
    })
    print(f"Status: {resp.status_code}, Response: {resp.json()}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "success"
    assert data.get("role") == "student"
    print("   [PASS] Student authenticated using register number identifier.\n")

    print("=================================================================")
    print("ALL STRICT LOGIN & DATABASE VALIDATION TESTS PASSED 100%!")
    print("=================================================================")

if __name__ == "__main__":
    test_strict_login_validation()
