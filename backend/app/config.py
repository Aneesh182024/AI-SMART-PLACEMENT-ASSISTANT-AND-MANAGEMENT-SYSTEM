import os

# JWT Secret & Security
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "psna_cet_it_placement_secret_key_2026_aneesh_anne")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

# Institutional Metadata
COLLEGE_NAME = "PSNA COLLEGE OF ENGINEERING AND TECHNOLOGY, DINDIGUL"
DEPARTMENT = "INFORMATION TECHNOLOGY"
SYSTEM_TITLE = "AI SMART PLACEMENT ASSISTANT AND MANAGEMENT SYSTEM"
DEVELOPERS = "ANEESH KANNA N and ANNE BENILDA A"
CURRENT_YEAR = 2026

# Anna University R-2022 Official Semester Credit Weights
R2022_SEMESTER_CREDITS = {
    1: 22.0,
    2: 25.0,
    3: 22.5,
    4: 22.5,
    5: 22.5,
    6: 21.0,
    7: 17.5,
    8: 10.0
}
TOTAL_DEGREE_CREDITS = sum(R2022_SEMESTER_CREDITS.values()) # 163 credits

# SMTP Email & OTP Configuration (Gmail App Passwords & Resend API)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "") # 16-character Google App Password
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
OTP_EXPIRY_MINUTES = 5

