from fastapi import APIRouter, HTTPException, status
from typing import Dict

from app.models import CalculateGpaRequest, CalculateCgpaRequest
from app.academic_engine import AnnaUniversityR2022Engine
from app.config import R2022_SEMESTER_CREDITS, TOTAL_DEGREE_CREDITS

router = APIRouter(prefix="/api/academic", tags=["Anna University R-2022 Engine"])

@router.get("/credit-scale")
def get_credit_scale():
    """
    Returns official Anna University R-2022 CBCS Semester Credit Breakdown for B.Tech IT.
    """
    return {
        "curriculum": "Anna University R-2022 CBCS Regulations",
        "department": "Information Technology (IT)",
        "semester_credits": R2022_SEMESTER_CREDITS,
        "total_degree_credits": TOTAL_DEGREE_CREDITS,
        "grade_points_scale": {
            "O": {"gp": 10, "marks": "91 - 100", "performance": "Outstanding"},
            "A+": {"gp": 9, "marks": "81 - 90", "performance": "Excellent"},
            "A": {"gp": 8, "marks": "71 - 80", "performance": "Very Good"},
            "B+": {"gp": 7, "marks": "61 - 70", "performance": "Good"},
            "B": {"gp": 6, "marks": "50 - 60", "performance": "Average"},
            "RA": {"gp": 0, "marks": "< 50 or EndSem < 45%", "performance": "Re-Appearance Arrear"},
            "SA": {"gp": 0, "marks": "Attendance < 75%", "performance": "Shortage of Attendance Override"}
        }
    }

@router.post("/calculate-gpa")
def calculate_gpa(payload: CalculateGpaRequest):
    """
    Computes weighted semester GPA under Anna University R-2022 regulations.
    - Passing condition: Total >= 50% AND End-Sem Exam >= 45%.
    - Attendance < 75% triggers an automatic 'SA' override (0 GP).
    """
    result = AnnaUniversityR2022Engine.calculate_semester_gpa(
        semester_num=payload.semester_num,
        subjects=payload.subjects
    )
    return result

@router.post("/calculate-cgpa")
def calculate_cgpa(payload: CalculateCgpaRequest):
    """
    Calculates Cumulative CGPA across completed terms using credit-weighted formulas:
    CGPA = SUM(Credits * GPA) / SUM(Credits).
    Also returns Year 1 joint credit average.
    """
    # Transform dictionary format for engine
    transformed = {}
    for sem_str, gpa in payload.semesters.items():
        sem_num = int(sem_str)
        transformed[sem_num] = {
            "gpa": float(gpa),
            "official_credits": R2022_SEMESTER_CREDITS.get(sem_num, 22.0),
            "arrears": 0
        }

    result = AnnaUniversityR2022Engine.calculate_cumulative_cgpa(transformed)
    return result
