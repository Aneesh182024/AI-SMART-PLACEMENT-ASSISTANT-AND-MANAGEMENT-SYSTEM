import io
import openpyxl
from fastapi.testclient import TestClient

from app.main import app
from app.auth import create_access_token

client = TestClient(app)

def test_api_excel():
    print("Testing live FastAPI Excel Endpoints...")

    # Create faculty JWT token
    faculty_token = create_access_token({
        "sub": "u-teach-001",
        "email": "staff@psnacet.edu.in",
        "role": "TEACHER",
        "name": "Dr. S. Karthik"
    })
    headers = {"Authorization": f"Bearer {faculty_token}"}

    # 1. Test POST /api/admin/upload-excel with CSV
    csv_data = (
        "Register No,Name,Gender,Year,Section,Email,Mobile,CGPA,Arrears\n"
        "713821104005,Gokulnath R,Male,IV,B,gokul.updated@psnacet.edu.in,9876543214,8.99,0\n"
        "713821104105,Pooja S,Female,IV,A,pooja@psnacet.edu.in,9876543255,8.80,0\n"
    )
    files = {
        "file": ("roster.csv", csv_data.encode("utf-8"), "text/csv")
    }
    resp = client.post("/api/admin/upload-excel", headers=headers, files=files)
    print("POST /api/admin/upload-excel (CSV) response:", resp.status_code, resp.json())
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["updated_count"] >= 1
    assert data["inserted_count"] >= 1

    # 2. Test POST /api/admin/upload-excel with XLSX
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Register No", "Name", "Gender", "Year", "Section", "Email", "Mobile", "CGPA", "Arrears"])
    ws.append(["713821104106", "Rajesh K", "Male", "IV", "E", "rajesh@psnacet.edu.in", "9876543256", "7.75", "1"])
    out = io.BytesIO()
    wb.save(out)
    out.seek(0)

    files_xlsx = {
        "file": ("new_batch.xlsx", out.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }
    resp_xlsx = client.post("/api/admin/upload-excel", headers=headers, files=files_xlsx)
    print("POST /api/admin/upload-excel (XLSX) response:", resp_xlsx.status_code, resp_xlsx.json())
    assert resp_xlsx.status_code == 200

    # 3. Test GET /api/admin/export-excel with Bearer header
    resp_export = client.get("/api/admin/export-excel", headers=headers)
    print("GET /api/admin/export-excel (Bearer header) response:", resp_export.status_code, len(resp_export.content), "bytes")
    assert resp_export.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in resp_export.headers.get("content-type", "")
    assert "attachment; filename=" in resp_export.headers.get("content-disposition", "")
    assert len(resp_export.content) > 5000

    # 4. Test GET /api/admin/export-excel with ?token= query parameter (for direct browser streaming download)
    resp_export_query = client.get(f"/api/admin/export-excel?token={faculty_token}")
    print("GET /api/admin/export-excel (?token= query) response:", resp_export_query.status_code, len(resp_export_query.content), "bytes")
    assert resp_export_query.status_code == 200
    assert len(resp_export_query.content) > 5000

    # 5. Test unauthorized access
    resp_unauth = client.get("/api/admin/export-excel")
    print("GET /api/admin/export-excel (Unauthorized) response:", resp_unauth.status_code)
    assert resp_unauth.status_code in (401, 403)

    print("\n[ALL FASTAPI EXCEL ROUTE INTEGRATION TESTS PASSED 100%!]")

if __name__ == "__main__":
    test_api_excel()
