# 🗄️ PostgreSQL Database Guide & Setup
**PSNA College of Engineering and Technology, Dindigul**  
*AI SMART PLACEMENT ASSISTANT AND MANAGEMENT SYSTEM*  
*Developed by ANEESH KANNA N and ANNE BENILDA A*

---

## 📁 Database Files Overview:

1. **`schema.sql`** — Complete PostgreSQL DDL (Tables: `users`, `students`, `semester_marks`, `certificates`, `correction_requests`, ENUMs, and Foreign Key constraints).
2. **`views.sql`** — Contains `Privacy_Masked_Student_View` (masks CGPA and arrears for peer lookups) and `Placement_Summary_View` (5-tier color codes for staff).
3. **`queries.sql`** — Production SQL query collection including the **Smart Upsert / De-duplication Query**.
4. **`seed.sql`** — Realistic IT department student records across Batches 2023–2027 and Sections A through F, plus faculty accounts.
5. **`init_db.py`** — Python test harness validating table creation, upsert de-duplication, and privacy view queries.

---

## 🚀 How to Run in PostgreSQL (Neon / Supabase / Render / Local):

### Option A: Using Neon.tech or Supabase SQL Editor (Fastest)
1. Open your **Neon Console** or **Supabase Dashboard**.
2. Go to **SQL Editor**.
3. Copy and run [`database/schema.sql`](file:///e:/project/smart%20placement/database/schema.sql).
4. Copy and run [`database/views.sql`](file:///e:/project/smart%20placement/database/views.sql).
5. Copy and run [`database/seed.sql`](file:///e:/project/smart%20placement/database/seed.sql).

### Option B: Using psql Command Line
```bash
psql "postgresql://user:password@ep-db.us-east-2.aws.neon.tech/smart_placement?sslmode=require" -f database/schema.sql
psql "postgresql://user:password@ep-db.us-east-2.aws.neon.tech/smart_placement?sslmode=require" -f database/views.sql
psql "postgresql://user:password@ep-db.us-east-2.aws.neon.tech/smart_placement?sslmode=require" -f database/seed.sql
```

---

## 🔄 Smart Upsert / De-Duplication Logic:

```sql
INSERT INTO students (register_no, name, year, section, email, mobile, cgpa)
VALUES ($1, $2, $3, $4, $5, $6, $7)
ON CONFLICT (register_no) 
DO UPDATE SET 
    year = EXCLUDED.year,
    section = EXCLUDED.section,
    email = EXCLUDED.email,
    mobile = EXCLUDED.mobile,
    cgpa = EXCLUDED.cgpa;
```
* **Benefit:** When uploading bulk Excel spreadsheets, existing students are updated seamlessly without creating duplicate student names or duplicate rows.

---

## 🛡️ Privacy Masking Rule:

```sql
CREATE VIEW Privacy_Masked_Student_View AS
SELECT 
    name, 
    register_no, 
    roll_no, 
    email, 
    mobile, 
    year, 
    section, 
    resume_url 
FROM students;
```
* **Benefit:** When students browse their Year and Section peers, they can only view contact details. Sensitive fields like `cgpa`, `active_arrears`, and failed subjects are excluded at the database level!
