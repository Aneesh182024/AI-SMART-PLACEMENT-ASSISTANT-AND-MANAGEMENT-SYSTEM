import io
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from typing import Dict, List, Tuple
from datetime import datetime

from app.config import COLLEGE_NAME, DEPARTMENT, SYSTEM_TITLE, DEVELOPERS, CURRENT_YEAR
from app.database_mock import STUDENTS_DB

# ==============================================================================
# 5-TIER COLOR CODING PATTERNS (Hex Colors from Project Specification)
# ==============================================================================
# 1. Emerald Green: Register Number if Without Arrear
FILL_EMERALD_GREEN = PatternFill(start_color="10B981", end_color="10B981", fill_type="solid")
FONT_WHITE_BOLD    = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

# 2. Crimson Red: Failed Subject Cell if Current Arrear
FILL_CRIMSON_RED   = PatternFill(start_color="EF4444", end_color="EF4444", fill_type="solid")

# 3. Amber Orange: Subject + Sem if Historical Arrear
FILL_AMBER_ORANGE  = PatternFill(start_color="F59E0B", end_color="F59E0B", fill_type="solid")

# 4. Soft Pastel Blue: Cleared Subject if Arrear Cleared
FILL_PASTEL_BLUE   = PatternFill(start_color="3B82F6", end_color="3B82F6", fill_type="solid")

# 5. Bright Gold / Yellow: Register Number if High CGPA Top Performer (>= 9.0)
FILL_BRIGHT_GOLD   = PatternFill(start_color="EAB308", end_color="EAB308", fill_type="solid")
FONT_BLACK_BOLD    = Font(name="Calibri", size=11, bold=True, color="000000")

# Header Styles
FILL_HEADER_EMERALD = PatternFill(start_color="0D5C3A", end_color="0D5C3A", fill_type="solid")
FONT_HEADER_WHITE   = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_TITLE_MAIN     = Font(name="Calibri", size=15, bold=True, color="0D5C3A")
FONT_SUBTITLE       = Font(name="Calibri", size=11, bold=True, color="475569")
BORDER_THIN         = Border(
    left=Side(style='thin', color='E2E8F0'),
    right=Side(style='thin', color='E2E8F0'),
    top=Side(style='thin', color='E2E8F0'),
    bottom=Side(style='thin', color='E2E8F0')
)

class ExcelService:
    """
    Excel Ingestion with De-Duplication & 5-Tier Color Coded Export Engine
    Engineered for PSNA CET Department of Information Technology.
    """

    @classmethod
    def ingest_spreadsheet(cls, file_bytes: bytes, filename: str) -> Dict:
        """
        Parses uploaded .xlsx or .csv student spreadsheet.
        Executes Smart Upsert: updates existing students by register_no without duplicate names.
        Reads columns: Register No, Name, Gender, Year, Section, Email, Mobile, CGPA, Arrears.
        """
        rows_data = []

        if filename.lower().endswith(".csv"):
            text_stream = io.StringIO(file_bytes.decode('utf-8', errors='ignore'))
            reader = csv.reader(text_stream)
            rows_data = list(reader)
        else:
            # Parse .xlsx using openpyxl
            wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
            ws = wb.active
            for row in ws.iter_rows(values_only=True):
                if any(row):  # Skip empty rows
                    rows_data.append([str(c) if c is not None else "" for c in row])

        if not rows_data:
            return {"status": "error", "message": "Spreadsheet is empty or could not be parsed."}

        # Identify Column Indices
        headers = [h.strip().lower() for h in rows_data[0]]

        def find_col_idx(candidates: List[str]) -> int:
            for idx, h in enumerate(headers):
                for cand in candidates:
                    if cand in h:
                        return idx
            return -1

        reg_idx = find_col_idx(["register", "reg no", "reg_no", "regno", "register number"])
        name_idx = find_col_idx(["name", "student name", "candidate"])
        gender_idx = find_col_idx(["gender", "sex"])
        year_idx = find_col_idx(["year", "batch"])
        sec_idx = find_col_idx(["section", "sec"])
        email_idx = find_col_idx(["email", "mail", "email address"])
        mobile_idx = find_col_idx(["mobile", "phone", "contact", "mobile number"])
        cgpa_idx = find_col_idx(["cgpa", "gpa"])
        arrear_idx = find_col_idx(["arrear", "backlog", "arrears", "active arrears"])

        if reg_idx == -1:
            return {
                "status": "error",
                "message": "Required column 'Register Number' was not found in the spreadsheet header row."
            }

        updated_count = 0
        inserted_count = 0

        for r in rows_data[1:]:
            if not r or len(r) <= reg_idx:
                continue

            reg_no = str(r[reg_idx]).strip()
            if not reg_no or reg_no.lower() in ("none", "null", ""):
                continue

            name = str(r[name_idx]).strip() if name_idx != -1 and len(r) > name_idx and r[name_idx] else "Student"
            gender = str(r[gender_idx]).strip() if gender_idx != -1 and len(r) > gender_idx and r[gender_idx] else "Male"
            year = str(r[year_idx]).strip().upper() if year_idx != -1 and len(r) > year_idx and r[year_idx] else "IV"
            sec = str(r[sec_idx]).strip().upper() if sec_idx != -1 and len(r) > sec_idx and r[sec_idx] else "A"
            email = str(r[email_idx]).strip() if email_idx != -1 and len(r) > email_idx and r[email_idx] else f"{reg_no}@psnacet.edu.in"
            mobile = str(r[mobile_idx]).strip() if mobile_idx != -1 and len(r) > mobile_idx and r[mobile_idx] else "9876543210"

            try:
                cgpa_val = float(str(r[cgpa_idx]).strip()) if cgpa_idx != -1 and len(r) > cgpa_idx and r[cgpa_idx] else 0.0
            except ValueError:
                cgpa_val = 0.0

            try:
                arrears_val = int(str(r[arrear_idx]).strip()) if arrear_idx != -1 and len(r) > arrear_idx and r[arrear_idx] else 0
            except ValueError:
                arrears_val = 0

            # Execute Smart Upsert Logic on register_no (Preserves student name without duplicate entries)
            if reg_no in STUDENTS_DB:
                STUDENTS_DB[reg_no]["gender"] = gender
                STUDENTS_DB[reg_no]["year"] = year
                STUDENTS_DB[reg_no]["section"] = sec
                STUDENTS_DB[reg_no]["email"] = email
                STUDENTS_DB[reg_no]["mobile"] = mobile
                if cgpa_val > 0:
                    STUDENTS_DB[reg_no]["cgpa"] = cgpa_val
                STUDENTS_DB[reg_no]["active_arrears"] = arrears_val
                STUDENTS_DB[reg_no]["eligibility"] = "Eligible" if arrears_val == 0 else "Not Eligible"
                updated_count += 1
            else:
                STUDENTS_DB[reg_no] = {
                    "register_no": reg_no,
                    "roll_no": f"21IT{reg_no[-3:] if len(reg_no) >= 3 else '000'}",
                    "name": name,
                    "gender": gender,
                    "department": "IT",
                    "year": year,
                    "section": sec,
                    "email": email,
                    "mobile": mobile,
                    "cgpa": cgpa_val,
                    "active_arrears": arrears_val,
                    "history_arrears": 0,
                    "cleared_arrears": 0,
                    "attendance": 95.0,
                    "is_locked": True,
                    "skills": ["Python", "SQL"],
                    "eligibility": "Eligible" if arrears_val == 0 else "Not Eligible",
                    "placement_status": "Not Placed",
                    "company": None,
                    "package_lpa": 0.0,
                    "resume_url": "#",
                    "semesters": {}
                }
                inserted_count += 1

        return {
            "status": "success",
            "message": f"Bulk Excel ingestion complete: {updated_count} existing records synchronized, {inserted_count} new students registered.",
            "updated_count": updated_count,
            "inserted_count": inserted_count,
            "total_processed": updated_count + inserted_count
        }

    @classmethod
    def generate_5tier_color_roster(cls) -> io.BytesIO:
        """
        Builds the official PSNA IT Placement Roster workbook with programmatic
        5-Tier conditional color styling across columns and cells.
        1. Emerald Green (#10B981): Student's Register Number column if Without Arrear.
        2. Crimson Red (#EF4444): Specific Failed Subject column for Current Arrear.
        3. Amber Orange (#F59E0B): Subject cell + Semester column for Previous Arrear.
        4. Soft Pastel Blue (#3B82F6): Cleared Subject + Cleared Sem column for Previous Arrear Cleared.
        5. Bright Gold / Yellow (#EAB308): Student's Register Number column for High CGPA Top Performer.
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "PSNA IT Placement Roster"

        # -------------------------------------------------------------
        # Institutional Placement Header Block
        # -------------------------------------------------------------
        ws.merge_cells("A1:M1")
        ws["A1"] = COLLEGE_NAME
        ws["A1"].font = FONT_TITLE_MAIN
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[1].height = 26

        ws.merge_cells("A2:M2")
        ws["A2"] = f"DEPARTMENT OF {DEPARTMENT} — OFFICIAL PLACEMENT ROSTER (ACADEMIC YEAR {CURRENT_YEAR})"
        ws["A2"].font = FONT_SUBTITLE
        ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[2].height = 20

        ws.merge_cells("A3:M3")
        ws["A3"] = f"{SYSTEM_TITLE} • Developed by: {DEVELOPERS} (© {CURRENT_YEAR} All Rights Reserved)"
        ws["A3"].font = Font(name="Calibri", size=9, italic=True, color="64748B")
        ws["A3"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[3].height = 18

        # Row 4 is blank spacer
        ws.row_dimensions[4].height = 8

        # -------------------------------------------------------------
        # Table Column Headers (Row 5) - 13 Columns
        # -------------------------------------------------------------
        headers = [
            "Register No", "Student Name", "Gender", "Year", "Sec", 
            "Email Address", "Mobile", "CGPA", "Active Arrears", 
            "Subject Code & Title", "Semester", "Drive Eligibility", 
            "Placement Status & Company (LPA)"
        ]

        for col_num, h_text in enumerate(headers, 1):
            cell = ws.cell(row=5, column=col_num)
            cell.value = h_text
            cell.font = FONT_HEADER_WHITE
            cell.fill = FILL_HEADER_EMERALD
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = BORDER_THIN

        ws.row_dimensions[5].height = 28

        # -------------------------------------------------------------
        # Student Data Rows with 5-Tier Color Logic (Starting Row 6)
        # -------------------------------------------------------------
        current_row = 6
        for s in STUDENTS_DB.values():
            reg_no = s["register_no"]
            name = s.get("name", "Student")
            gender = s.get("gender", "Male")
            year = s.get("year", "IV")
            sec = s.get("section", "A")
            email = s.get("email", "")
            mobile = s.get("mobile", "")
            cgpa_val = float(s.get("cgpa", 0.0))
            active_arr = int(s.get("active_arrears", 0))
            history_arr = int(s.get("history_arrears", 0))
            cleared_arr = int(s.get("cleared_arrears", 0))

            # Subject condition label & Semester label
            if active_arr > 0:
                subject_text = "IT3402 Operating Systems (RA)"
                semester_text = "Semester 4"
            elif cleared_arr > 0:
                subject_text = "IT3301 Data Structures (Cleared)"
                semester_text = "Semester 3 (Cleared)"
            elif history_arr > 0:
                subject_text = "MA3151 Matrices & Calculus (Past Arrear)"
                semester_text = "Semester 1"
            else:
                subject_text = "All Subjects Cleared"
                semester_text = "Clean Record"

            # Placement label
            placement_label = s.get("placement_status", "Eligible")
            if placement_label == "Placed":
                company_str = s.get("company", "Corporate")
                pkg_str = f"{s.get('package_lpa', 0.0)} LPA"
                placement_full = f"Placed: {company_str} ({pkg_str})"
            else:
                placement_full = placement_label

            row_values = [
                reg_no,
                name,
                gender,
                year,
                sec,
                email,
                mobile,
                f"{cgpa_val:.2f}",
                active_arr,
                subject_text,
                semester_text,
                s.get("eligibility", "Eligible"),
                placement_full
            ]

            for col_num, val in enumerate(row_values, 1):
                cell = ws.cell(row=current_row, column=col_num)
                cell.value = val
                cell.border = BORDER_THIN
                cell.alignment = Alignment(vertical="center")

                # Center align code/number columns
                if col_num in (1, 3, 4, 5, 8, 9, 11, 12):
                    cell.alignment = Alignment(horizontal="center", vertical="center")

            # ---------------------------------------------------------
            # Apply Strict 5-Tier Conditional Formatting:
            # ---------------------------------------------------------
            reg_cell = ws.cell(row=current_row, column=1)      # Column 1: Register Number
            subject_cell = ws.cell(row=current_row, column=10) # Column 10: Subject Code & Title
            sem_cell = ws.cell(row=current_row, column=11)     # Column 11: Semester

            # Rule 5: High CGPA Top Performer (>= 9.0) -> Bright Gold on Register No
            if cgpa_val >= 9.0:
                reg_cell.fill = FILL_BRIGHT_GOLD
                reg_cell.font = FONT_BLACK_BOLD

            # Rule 1: Without Arrear -> Emerald Green on Register Number (if not Gold)
            elif active_arr == 0:
                reg_cell.fill = FILL_EMERALD_GREEN
                reg_cell.font = FONT_WHITE_BOLD

            # Rule 2: Current Arrear -> Crimson Red on Specific Failed Subject
            if active_arr > 0:
                subject_cell.fill = FILL_CRIMSON_RED
                subject_cell.font = FONT_WHITE_BOLD

            # Rule 4: Previous Arrear Cleared -> Soft Pastel Blue on Subject + Semester
            elif cleared_arr > 0:
                subject_cell.fill = FILL_PASTEL_BLUE
                subject_cell.font = FONT_WHITE_BOLD
                sem_cell.fill = FILL_PASTEL_BLUE
                sem_cell.font = FONT_WHITE_BOLD

            # Rule 3: Previous Arrear -> Amber Orange on Subject + Semester
            elif history_arr > 0:
                subject_cell.fill = FILL_AMBER_ORANGE
                subject_cell.font = FONT_WHITE_BOLD
                sem_cell.fill = FILL_AMBER_ORANGE
                sem_cell.font = FONT_WHITE_BOLD

            ws.row_dimensions[current_row].height = 22
            current_row += 1

        # -------------------------------------------------------------
        # Official 5-Tier Color Indicator Legend Block at Bottom
        # -------------------------------------------------------------
        current_row += 1
        ws.cell(row=current_row, column=1, value="Official 5-Tier Color Indicator Legend:").font = Font(name="Calibri", size=10, bold=True)
        current_row += 1

        legend_items = [
            ("1. Emerald Green (#10B981)", FILL_EMERALD_GREEN, FONT_WHITE_BOLD, "Student's Register Number column if Without Arrear (Clean Record)"),
            ("2. Crimson Red (#EF4444)", FILL_CRIMSON_RED, FONT_WHITE_BOLD, "Specific Failed Subject column for Current Arrear (Immediate Attention)"),
            ("3. Amber Orange (#F59E0B)", FILL_AMBER_ORANGE, FONT_WHITE_BOLD, "Subject cell + Semester column for Previous Arrear (Historical Delay)"),
            ("4. Soft Pastel Blue (#3B82F6)", FILL_PASTEL_BLUE, FONT_WHITE_BOLD, "Cleared Subject + Cleared Sem for Previous Arrear Cleared (Recovered)"),
            ("5. Bright Gold / Yellow (#EAB308)", FILL_BRIGHT_GOLD, FONT_BLACK_BOLD, "Student's Register Number column for High CGPA Top Performer (>= 9.0)")
        ]

        for code_str, fill_pat, font_pat, desc_str in legend_items:
            color_box = ws.cell(row=current_row, column=1, value=code_str)
            color_box.fill = fill_pat
            color_box.font = font_pat
            color_box.alignment = Alignment(horizontal="center", vertical="center")
            
            ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=6)
            desc_cell = ws.cell(row=current_row, column=2, value=desc_str)
            desc_cell.font = Font(name="Calibri", size=10, italic=True)
            ws.row_dimensions[current_row].height = 20
            current_row += 1

        # -------------------------------------------------------------
        # Auto-adjust Column Widths cleanly
        # -------------------------------------------------------------
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                # Avoid measuring merged banner title cells
                if cell.row in (1, 2, 3):
                    continue
                val_str = str(cell.value or '')
                if len(val_str) > max_len:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

        # Save to memory stream
        output_stream = io.BytesIO()
        wb.save(output_stream)
        output_stream.seek(0)
        return output_stream
