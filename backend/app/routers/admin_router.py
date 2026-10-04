from fastapi import APIRouter, HTTPException, Depends, status, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Optional
from datetime import datetime, timezone

from app.auth import get_current_user, require_roles, decode_access_token
from app.models import UpdateEligibilityRequest, BatchEligibilityRequest, CorrectionRequestReview
from app.database_mock import STUDENTS_DB, CORRECTION_REQUESTS
from app.excel_service import ExcelService

router = APIRouter(prefix="/api/admin", tags=["Teacher & HOD Control Center"])

security_optional = HTTPBearer(auto_error=False)

def verify_faculty_access(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    token: Optional[str] = Query(None, description="Optional download JWT token for direct browser streaming")
) -> Dict:
    """Verifies Teacher or HOD permissions via HTTP Bearer token or direct download query token."""
    raw_token = credentials.credentials if credentials else token
    if not raw_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Faculty authentication required. Please provide Bearer token or ?token= parameter."
        )
    user = decode_access_token(raw_token)
    if user.get("role", "").upper() not in ["TEACHER", "HOD"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This service is restricted to PSNA IT Faculty and HOD."
        )
    return user

@router.post("/upload-excel")
async def upload_student_excel(
    file: UploadFile = File(..., description="Student roster spreadsheet (.xlsx or .csv)"),
    current_user: Dict = Depends(verify_faculty_access)
):
    """
    SMART BULK EXCEL INGESTION ENGINE:
    - Accepts .xlsx or .csv student roster file.
    - Reads columns: Register No, Name, Gender, Year, Section, Email, Mobile, CGPA, Arrears.
    - Executes PostgreSQL smart upsert on register_no: updates existing student academic records 
      without duplicating names or generating multiple database entries.
    """
    filename = file.filename or ""
    if not (filename.lower().endswith(".xlsx") or filename.lower().endswith(".csv")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload an official Excel (.xlsx) or CSV (.csv) roster file."
        )

    content = await file.read()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    result = ExcelService.ingest_spreadsheet(content, filename)
    if result.get("status") == "error":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=result.get("message", "Failed to parse spreadsheet.")
        )

    return result

@router.get("/export-excel")
def export_color_coded_excel(
    token: Optional[str] = Query(None, description="Direct download JWT token"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional)
):
    """
    5-TIER COLOR-CODED EXCEL EXPORT ENGINE:
    Generates and streams official PSNA IT placement roster .xlsx file applying conditional cell styling:
      1. Emerald Green (#10B981): Student's Register Number column if Without Arrear.
      2. Crimson Red (#EF4444): Specific Failed Subject column for Current Arrear.
      3. Amber Orange (#F59E0B): Subject cell + Semester column for Previous Arrear.
      4. Soft Pastel Blue (#3B82F6): Cleared Subject + Cleared Sem column for Previous Arrear Cleared.
      5. Bright Gold / Yellow (#EAB308): Student's Register Number column for High CGPA Top Performer.
    Automatically adjusts column widths and adds PSNA IT Department official placement header.
    """
    verify_faculty_access(credentials, token)

    excel_stream = ExcelService.generate_5tier_color_roster()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    download_filename = f"PSNA_IT_Placement_Roster_{timestamp}.xlsx"

    return StreamingResponse(
        excel_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{download_filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )


@router.get("/roster")
def get_placement_roster(
    section: Optional[str] = Query(None, description="Filter by section A-F"),
    current_user: Dict = Depends(require_roles(["TEACHER", "HOD"]))
):
    """
    Returns full placement roster with academic metrics for faculty & HOD review.
    """
    roster = list(STUDENTS_DB.values())
    if section and section.upper() != "ALL":
        roster = [s for s in roster if s.get("section") == section.upper()]

    return {
        "total_students": len(roster),
        "requested_section": section or "ALL",
        "roster": roster
    }

@router.post("/eligibility")
def update_student_eligibility(
    payload: UpdateEligibilityRequest,
    current_user: Dict = Depends(require_roles(["TEACHER", "HOD"]))
):
    """
    One-Click Eligibility Marking API:
    Updates student status as 'Eligible', 'Not Eligible', or 'Placed' (with company and package).
    """
    reg_no = payload.register_no
    student = STUDENTS_DB.get(reg_no)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with Register Number {reg_no} not found."
        )

    student["eligibility"] = payload.eligibility
    if payload.placement_status:
        student["placement_status"] = payload.placement_status
    if payload.company:
        student["company"] = payload.company
    if payload.package_lpa is not None:
        student["package_lpa"] = payload.package_lpa

    return {
        "message": f"Placement eligibility for {student['name']} ({reg_no}) updated to '{payload.eligibility}'.",
        "student": student
    }

@router.post("/batch-eligibility")
def update_batch_eligibility(
    payload: BatchEligibilityRequest,
    current_user: Dict = Depends(require_roles(["TEACHER", "HOD"]))
):
    """
    Batch Eligibility Marking API:
    Triggered by faculty or automatically by the Placement AI Chatbot!
    """
    updated_count = 0
    for reg_no in payload.register_numbers:
        if reg_no in STUDENTS_DB:
            STUDENTS_DB[reg_no]["eligibility"] = payload.eligibility
            if payload.company:
                STUDENTS_DB[reg_no]["company"] = payload.company
            updated_count += 1

    return {
        "message": f"Successfully updated eligibility to '{payload.eligibility}' for {updated_count} students.",
        "updated_count": updated_count
    }

@router.get("/correction-requests")
def list_correction_requests(current_user: Dict = Depends(require_roles(["TEACHER", "HOD"]))):
    """
    Lists all student digital permission requests awaiting Tutor/Incharge review.
    """
    return {
        "total_pending": len([r for r in CORRECTION_REQUESTS if r["status"] == "PENDING"]),
        "requests": CORRECTION_REQUESTS
    }

@router.post("/review-correction")
def review_correction_request(
    payload: CorrectionRequestReview,
    current_user: Dict = Depends(require_roles(["TEACHER", "HOD"]))
):
    """
    Approves or rejects a student digital correction request.
    If approved, applies modification to STUDENTS_DB.
    """
    target_req = next((r for r in CORRECTION_REQUESTS if r["request_id"] == payload.request_id), None)
    if not target_req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Correction request #{payload.request_id} not found."
        )

    target_req["status"] = payload.status.upper()
    target_req["reviewed_by"] = current_user.get("name", "Faculty")
    target_req["tutor_remarks"] = payload.tutor_remarks
    target_req["reviewed_at"] = datetime.now(timezone.utc).isoformat()

    # If approved, update student profile
    if payload.status.upper() == "APPROVED":
        reg_no = target_req["register_no"]
        field = target_req["requested_field"]
        new_val = target_req["new_value"]

        if reg_no in STUDENTS_DB:
            if field in ("cgpa", "package_lpa", "attendance"):
                STUDENTS_DB[reg_no][field] = float(new_val)
            else:
                STUDENTS_DB[reg_no][field] = new_val

    return {
        "message": f"Correction request #{payload.request_id} marked as {payload.status}.",
        "request": target_req
    }

@router.get("/analytics")
def get_control_center_analytics(current_user: Dict = Depends(require_roles(["TEACHER", "HOD"]))):
    """
    Computes real-time KPI metrics & chart data for Teacher and HOD visual dashboards.
    """
    students_list = list(STUDENTS_DB.values())
    total = len(students_list)
    eligible = sum(1 for s in students_list if s.get("eligibility") == "Eligible")
    placed = sum(1 for s in students_list if s.get("placement_status") == "Placed")
    active_arrears = sum(s.get("active_arrears", 0) for s in students_list)

    # CGPA Distribution for Recharts Bar Chart
    dist = {
        "9.0 - 10.0 (Elite)": 0,
        "8.0 - 8.9 (First Class)": 0,
        "7.0 - 7.9 (Good)": 0,
        "< 7.0 (Arrear Risk)": 0
    }
    for s in students_list:
        c = s.get("cgpa", 0.0)
        if c >= 9.0:
            dist["9.0 - 10.0 (Elite)"] += 1
        elif c >= 8.0:
            dist["8.0 - 8.9 (First Class)"] += 1
        elif c >= 7.0:
            dist["7.0 - 7.9 (Good)"] += 1
        else:
            dist["< 7.0 (Arrear Risk)"] += 1

    chart_data = [{"range": k, "count": v} for k, v in dist.items()]

    return {
        "kpi_metrics": {
            "total_students": total,
            "eligible_count": eligible,
            "placed_count": placed,
            "total_active_backlogs": active_arrears,
            "placement_percentage": round((placed / total * 100), 1) if total > 0 else 0.0
        },
        "cgpa_distribution_chart": chart_data
    }
