from typing import Dict, List, Optional
from datetime import datetime, timezone
import random

# In-memory persistent data store for PSNA IT Department
USERS_DB: Dict[str, Dict] = {
    # Default Student
    "713821104001": {
        "id": "u-stud-001",
        "identifier": "713821104001",
        "email": "713821104001@psnacet.edu.in",
        "phone": "9876543210",
        "password_hash": "$2b$12$hF0zJmzKBCNghJAYNDkoyux6yhjXmNj3fGh.Eh.6J7RDf3s2xNT22",
        "plain_fallback": "Student@123",
        "name": "Aneesh Kanna N",
        "role": "STUDENT",
        "gender": "Male",
        "department": "IT",
        "year": "IV",
        "section": "A",
        "created_at": "2026-10-04T00:00:00Z"
    },
    # Default Student 2
    "713821104002": {
        "id": "u-stud-002",
        "identifier": "713821104002",
        "email": "713821104002@psnacet.edu.in",
        "phone": "9876543211",
        "password_hash": "$2b$12$hF0zJmzKBCNghJAYNDkoyux6yhjXmNj3fGh.Eh.6J7RDf3s2xNT22",
        "plain_fallback": "Student@123",
        "name": "Anne Benilda A",
        "role": "STUDENT",
        "gender": "Female",
        "department": "IT",
        "year": "IV",
        "section": "A",
        "created_at": "2026-10-04T00:00:00Z"
    },
    # Default Teacher (Tutor)
    "staff@psnacet.edu.in": {
        "id": "u-teach-001",
        "identifier": "staff@psnacet.edu.in",
        "email": "staff@psnacet.edu.in",
        "phone": "9876543219",
        "password_hash": "$2b$12$9Rn3wAGGcPNjypAdux2x1OdJZzjFhJrXhJTgi5l4gl7kSF2Wq2Zni",
        "plain_fallback": "Teacher@123",
        "name": "Dr. S. Karthik",
        "role": "TEACHER",
        "department": "IT",
        "created_at": "2026-10-04T00:00:00Z"
    },
    # Default HOD
    "hod.it@psnacet.edu.in": {
        "id": "u-hod-001",
        "identifier": "hod.it@psnacet.edu.in",
        "email": "hod.it@psnacet.edu.in",
        "phone": "9876543200",
        "password_hash": "$2b$12$mRM/q0aFbiA6Huj1YrsEp.JY65srMAdY/llWrQ3/8gI2N/yiQ9WpW",
        "plain_fallback": "Hod@123",
        "name": "Dr. M. IT Department HOD",
        "role": "HOD",
        "department": "IT",
        "created_at": "2026-10-04T00:00:00Z"
    }
}

# Student Academic Profiles (Protected by Data Freezing Gate)
STUDENTS_DB: Dict[str, Dict] = {
    "713821104001": {
        "register_no": "713821104001",
        "roll_no": "21IT001",
        "name": "Aneesh Kanna N",
        "gender": "Male",
        "department": "IT",
        "year": "IV",
        "section": "A",
        "email": "713821104001@psnacet.edu.in",
        "mobile": "9876543210",
        "cgpa": 9.20,
        "active_arrears": 0,
        "history_arrears": 0,
        "cleared_arrears": 0,
        "attendance": 96.5,
        "is_locked": True, # Data Freezing Gate: Profiles lock upon submission
        "skills": ["Python", "React", "FastAPI", "PostgreSQL"],
        "eligibility": "Eligible",
        "placement_status": "Placed",
        "company": "TCS Digital",
        "package_lpa": 7.5,
        "resume_url": "/resumes/713821104001_resume.pdf",
        "semesters": {
            1: {"gpa": 9.00, "arrears": 0, "official_credits": 22.0},
            2: {"gpa": 9.15, "arrears": 0, "official_credits": 25.0},
            3: {"gpa": 9.20, "arrears": 0, "official_credits": 22.5},
            4: {"gpa": 9.30, "arrears": 0, "official_credits": 22.5},
            5: {"gpa": 9.25, "arrears": 0, "official_credits": 22.5},
            6: {"gpa": 9.30, "arrears": 0, "official_credits": 21.0},
        }
    },
    "713821104002": {
        "register_no": "713821104002",
        "roll_no": "21IT002",
        "name": "Anne Benilda A",
        "gender": "Female",
        "department": "IT",
        "year": "IV",
        "section": "A",
        "email": "713821104002@psnacet.edu.in",
        "mobile": "9876543211",
        "cgpa": 9.45,
        "active_arrears": 0,
        "history_arrears": 0,
        "cleared_arrears": 0,
        "attendance": 98.0,
        "is_locked": True,
        "skills": ["Python", "Machine Learning", "Java", "Cloud"],
        "eligibility": "Eligible",
        "placement_status": "Placed",
        "company": "Zoho Corp",
        "package_lpa": 9.0,
        "resume_url": "/resumes/713821104002_resume.pdf",
        "semesters": {
            1: {"gpa": 9.20, "arrears": 0, "official_credits": 22.0},
            2: {"gpa": 9.40, "arrears": 0, "official_credits": 25.0},
            3: {"gpa": 9.50, "arrears": 0, "official_credits": 22.5},
            4: {"gpa": 9.60, "arrears": 0, "official_credits": 22.5},
            5: {"gpa": 9.45, "arrears": 0, "official_credits": 22.5},
            6: {"gpa": 9.55, "arrears": 0, "official_credits": 21.0},
        }
    },
    "713821104003": {
        "register_no": "713821104003",
        "roll_no": "21IT003",
        "name": "Balamurugan K",
        "gender": "Male",
        "department": "IT",
        "year": "IV",
        "section": "A",
        "email": "bala@psnacet.edu.in",
        "mobile": "9876543212",
        "cgpa": 8.65,
        "active_arrears": 0,
        "history_arrears": 1,
        "cleared_arrears": 1,
        "attendance": 92.0,
        "is_locked": True,
        "skills": ["Python", "SQL", "Docker"],
        "eligibility": "Eligible",
        "placement_status": "In Process",
        "company": "Cognizant",
        "package_lpa": 4.5,
        "resume_url": "/resumes/713821104003_resume.pdf",
        "semesters": {
            1: {"gpa": 8.40, "arrears": 0, "official_credits": 22.0},
            2: {"gpa": 8.50, "arrears": 1, "official_credits": 25.0},
            3: {"gpa": 8.70, "arrears": 0, "official_credits": 22.5},
            4: {"gpa": 8.80, "arrears": 0, "official_credits": 22.5},
            5: {"gpa": 8.75, "arrears": 0, "official_credits": 22.5},
            6: {"gpa": 8.90, "arrears": 0, "official_credits": 21.0},
        }
    },
    "713821104004": {
        "register_no": "713821104004",
        "roll_no": "21IT004",
        "name": "Dharani S",
        "gender": "Female",
        "department": "IT",
        "year": "IV",
        "section": "B",
        "email": "dharani@psnacet.edu.in",
        "mobile": "9876543213",
        "cgpa": 7.80,
        "active_arrears": 1,
        "history_arrears": 1,
        "cleared_arrears": 0,
        "attendance": 88.0,
        "is_locked": True,
        "skills": ["Java", "HTML/CSS", "JavaScript"],
        "eligibility": "Not Eligible",
        "placement_status": "Not Placed",
        "company": None,
        "package_lpa": 0.0,
        "resume_url": "/resumes/713821104004_resume.pdf",
        "semesters": {
            1: {"gpa": 7.60, "arrears": 0, "official_credits": 22.0},
            2: {"gpa": 7.70, "arrears": 0, "official_credits": 25.0},
            3: {"gpa": 7.50, "arrears": 1, "official_credits": 22.5},
            4: {"gpa": 8.00, "arrears": 0, "official_credits": 22.5},
            5: {"gpa": 8.10, "arrears": 0, "official_credits": 22.5},
            6: {"gpa": 8.00, "arrears": 0, "official_credits": 21.0},
        }
    },
    "713821104005": {
        "register_no": "713821104005",
        "roll_no": "21IT005",
        "name": "Gokulnath R",
        "gender": "Male",
        "department": "IT",
        "year": "IV",
        "section": "B",
        "email": "gokul@psnacet.edu.in",
        "mobile": "9876543214",
        "cgpa": 8.85,
        "active_arrears": 0,
        "history_arrears": 0,
        "cleared_arrears": 0,
        "attendance": 95.0,
        "is_locked": True,
        "skills": ["Python", "Django", "React", "AWS"],
        "eligibility": "Eligible",
        "placement_status": "Eligible",
        "company": "Hexaware",
        "package_lpa": 5.0,
        "resume_url": "/resumes/713821104005_resume.pdf",
        "semesters": {
            1: {"gpa": 8.60, "arrears": 0, "official_credits": 22.0},
            2: {"gpa": 8.80, "arrears": 0, "official_credits": 25.0},
            3: {"gpa": 8.90, "arrears": 0, "official_credits": 22.5},
            4: {"gpa": 9.00, "arrears": 0, "official_credits": 22.5},
            5: {"gpa": 8.85, "arrears": 0, "official_credits": 22.5},
            6: {"gpa": 8.95, "arrears": 0, "official_credits": 21.0},
        }
    },
    "713821104006": {
        "register_no": "713821104006",
        "roll_no": "21IT006",
        "name": "Harini M",
        "gender": "Female",
        "department": "IT",
        "year": "IV",
        "section": "C",
        "email": "harini@psnacet.edu.in",
        "mobile": "9876543215",
        "cgpa": 8.40,
        "active_arrears": 0,
        "history_arrears": 1,
        "cleared_arrears": 1,
        "attendance": 91.0,
        "is_locked": True,
        "skills": ["C++", "SQL", "Linux"],
        "eligibility": "Eligible",
        "placement_status": "In Process",
        "company": "Wipro",
        "package_lpa": 4.0,
        "resume_url": "/resumes/713821104006_resume.pdf",
        "semesters": {
            1: {"gpa": 8.20, "arrears": 0, "official_credits": 22.0},
            2: {"gpa": 8.30, "arrears": 1, "official_credits": 25.0},
            3: {"gpa": 8.50, "arrears": 0, "official_credits": 22.5},
            4: {"gpa": 8.60, "arrears": 0, "official_credits": 22.5},
            5: {"gpa": 8.40, "arrears": 0, "official_credits": 22.5},
            6: {"gpa": 8.50, "arrears": 0, "official_credits": 21.0},
        }
    },
    "713821104007": {
        "register_no": "713821104007",
        "roll_no": "21IT007",
        "name": "Kavitha S",
        "gender": "Female",
        "department": "IT",
        "year": "IV",
        "section": "C",
        "email": "kavitha@psnacet.edu.in",
        "mobile": "9876543216",
        "cgpa": 8.15,
        "active_arrears": 0,
        "history_arrears": 1,
        "cleared_arrears": 0,
        "attendance": 90.0,
        "is_locked": True,
        "skills": ["Java", "Spring Boot", "MySQL"],
        "eligibility": "Eligible",
        "placement_status": "Eligible",
        "company": None,
        "package_lpa": 0.0,
        "resume_url": "/resumes/713821104007_resume.pdf",
        "semesters": {
            1: {"gpa": 7.80, "arrears": 1, "official_credits": 22.0},
            2: {"gpa": 8.00, "arrears": 0, "official_credits": 25.0},
            3: {"gpa": 8.20, "arrears": 0, "official_credits": 22.5},
            4: {"gpa": 8.30, "arrears": 0, "official_credits": 22.5},
            5: {"gpa": 8.25, "arrears": 0, "official_credits": 22.5},
            6: {"gpa": 8.20, "arrears": 0, "official_credits": 21.0},
        }
    }
}

# Digital Correction Requests (Triggered by students for Tutor approval)
CORRECTION_REQUESTS: List[Dict] = []

# Active OTP Store { email: { "otp": "123456", "expires_at": timestamp } }
OTP_CACHE: Dict[str, Dict] = {}

def get_privacy_masked_peers(year: str, section: str) -> List[Dict]:
    """
    Simulates PostgreSQL `Privacy_Masked_Student_View`:
    Exposes only safe parameters: Name, Reg No, Roll No, Email, Mobile, Resume Link.
    STRICTLY HIDES: CGPA, marks, failures, parent details.
    """
    peers = []
    for s in STUDENTS_DB.values():
        if s.get("year") == year and s.get("section") == section:
            peers.append({
                "name": s["name"],
                "register_no": s["register_no"],
                "roll_no": s.get("roll_no", "N/A"),
                "year": s["year"],
                "section": s["section"],
                "email": s["email"],
                "mobile": s["mobile"],
                "resume_url": s.get("resume_url", "#")
                # Notice: cgpa, arrears, semesters are NOT returned here!
            })
    return peers
