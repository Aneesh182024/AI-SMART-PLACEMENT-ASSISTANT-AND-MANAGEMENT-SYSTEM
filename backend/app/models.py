from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    HOD = "HOD"

# Auth Models
class UserSignupRequest(BaseModel):
    name: str
    register_no: str
    gender: str
    department: str = "IT"
    year: str # 'I', 'II', 'III', 'IV'
    section: str # 'A', 'B', 'C', 'D', 'E', 'F'
    mobile: str
    email: str
    password: str
    confirm_password: str
    agreed_to_terms: bool

class UserLoginRequest(BaseModel):
    identifier: str # Register No, Email, or Phone
    password: str
    role: str # 'student', 'teacher', 'hod'

class ForgotPasswordRequest(BaseModel):
    email: str

class VerifyOtpRequest(BaseModel):
    email: str
    otp: str
    new_password: str

# Academic R-2022 Models
class SubjectMarkInput(BaseModel):
    subject_code: str
    subject_name: str
    credits: float
    internal_marks: float
    end_sem_marks: float
    attendance_percentage: float = 100.0

class CalculateGpaRequest(BaseModel):
    semester_num: int = Field(..., ge=1, le=8)
    subjects: List[SubjectMarkInput]

class CalculateCgpaRequest(BaseModel):
    semesters: Dict[int, float] # {1: 8.5, 2: 8.8, ...}

# Data Freezing & Correction Request
class CorrectionRequestCreate(BaseModel):
    register_no: str
    requested_field: str # 'cgpa', 'sem_gpa', 'skills', 'name'
    new_value: str
    reason: str

class CorrectionRequestReview(BaseModel):
    request_id: int
    status: str # 'APPROVED' | 'REJECTED'
    tutor_remarks: Optional[str] = None

# Placement Eligibility Models
class UpdateEligibilityRequest(BaseModel):
    register_no: str
    eligibility: str # 'Eligible' | 'Not Eligible'
    placement_status: Optional[str] = None # 'Not Placed' | 'In Process' | 'Placed'
    company: Optional[str] = None
    package_lpa: Optional[float] = 0.0

class BatchEligibilityRequest(BaseModel):
    register_numbers: List[str]
    eligibility: str
    company: Optional[str] = None
