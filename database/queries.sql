-- ==============================================================================
-- PSNA COLLEGE OF ENGINEERING AND TECHNOLOGY, DINDIGUL
-- DEPARTMENT OF INFORMATION TECHNOLOGY
-- CORE SQL QUERIES: Smart Upsert, Peer Lookups, and Eligibility Marking
-- Developed by: ANEESH KANNA N and ANNE BENILDA A
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. SMART UPSERT / DE-DUPLICATION QUERY (Bulk Excel Spreadsheet Ingestion)
-- ------------------------------------------------------------------------------
-- Ensures that when staff upload bulk student spreadsheets, if a student already
-- exists (identified by their unique register_no), their name is preserved and
-- their latest year, section, email, mobile, and CGPA are updated without 
-- generating duplicate rows!
-- ------------------------------------------------------------------------------
INSERT INTO students (register_no, name, year, section, email, mobile, cgpa)
VALUES ($1, $2, $3, $4, $5, $6, $7)
ON CONFLICT (register_no) 
DO UPDATE SET 
    year = EXCLUDED.year,
    section = EXCLUDED.section,
    email = EXCLUDED.email,
    mobile = EXCLUDED.mobile,
    cgpa = EXCLUDED.cgpa,
    updated_at = CURRENT_TIMESTAMP;

-- ------------------------------------------------------------------------------
-- 2. SECTION-SEGREGATED PEER DIRECTORY QUERY (Privacy Masked)
-- ------------------------------------------------------------------------------
-- Triggered when a student logs in. Shows ONLY peers from their own batch and 
-- section, while keeping CGPA, marks, and arrears completely hidden.
-- ------------------------------------------------------------------------------
SELECT 
    name, 
    register_no, 
    roll_no, 
    email, 
    mobile, 
    year, 
    section, 
    resume_url
FROM Privacy_Masked_Student_View
WHERE year = $1 AND section = $2
ORDER BY register_no ASC;

-- ------------------------------------------------------------------------------
-- 3. ONE-CLICK PLACEMENT ELIGIBILITY UPDATE QUERY
-- ------------------------------------------------------------------------------
-- Updates candidate eligibility flags and company placement records.
-- ------------------------------------------------------------------------------
UPDATE students
SET 
    placement_status = $1,
    placed_company = $2,
    salary_package_lpa = $3,
    updated_at = CURRENT_TIMESTAMP
WHERE register_no = $4;

-- ------------------------------------------------------------------------------
-- 4. BATCH ELIGIBILITY UPDATE QUERY (AI Chatbot & Staff Bulk Actions)
-- ------------------------------------------------------------------------------
UPDATE students
SET 
    placement_status = $1,
    placed_company = COALESCE($2, placed_company),
    updated_at = CURRENT_TIMESTAMP
WHERE register_no = ANY($3);

-- ------------------------------------------------------------------------------
-- 5. AI CHATBOT FILTER SQL (Dynamic Parameter Execution)
-- ------------------------------------------------------------------------------
-- Example: IT students with Python skill, CGPA > 8.5, max 1 backlog
-- ------------------------------------------------------------------------------
SELECT *
FROM Placement_Summary_View
WHERE department = 'IT'
  AND cgpa >= $1
  AND active_arrears <= $2
ORDER BY cgpa DESC;
