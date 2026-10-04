-- ==============================================================================
-- PSNA COLLEGE OF ENGINEERING AND TECHNOLOGY, DINDIGUL
-- DEPARTMENT OF INFORMATION TECHNOLOGY
-- DATABASE VIEWS: Privacy Masking & Administrative Placement Insights
-- Developed by: ANEESH KANNA N and ANNE BENILDA A
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. PRIVACY MASKING DATABASE VIEW (Student Peer Directory)
-- ------------------------------------------------------------------------------
-- Purpose: Protects student academic confidentiality. When students query 
-- the peer directory for their Year and Section, this view provides safe
-- contact parameters while strictly omitting CGPA, marks, and failure logs.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW Privacy_Masked_Student_View AS
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

COMMENT ON VIEW Privacy_Masked_Student_View IS 
'Enforces PSNA IT Department Privacy Masking Rule. Masks CGPA, marks, and arrears from student peers.';

-- ------------------------------------------------------------------------------
-- 2. PLACEMENT & ACADEMIC SUMMARY VIEW (Teacher & HOD Control Center)
-- ------------------------------------------------------------------------------
-- Purpose: Unified administrative pane summarizing placement statistics,
-- high CGPA candidates, and active backlogs across Batches & Sections A to F.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW Placement_Summary_View AS
SELECT 
    s.register_no,
    s.roll_no,
    s.name,
    s.year,
    s.section,
    s.cgpa,
    s.active_arrears,
    s.cleared_arrears,
    s.attendance,
    s.placement_status,
    s.placed_company,
    s.salary_package_lpa,
    -- Computed 5-Tier Color Indicator Code for Excel & Dashboard:
    CASE 
        WHEN s.cgpa >= 9.0 THEN 'BRIGHT_GOLD'       -- 5. High CGPA Elite
        WHEN s.active_arrears > 0 THEN 'CRIMSON_RED' -- 2. Current Arrear
        WHEN s.cleared_arrears > 0 THEN 'PASTEL_BLUE'-- 4. Previous Arrear Cleared
        WHEN s.history_arrears > 0 THEN 'AMBER_ORANGE'-- 3. Previous Arrear
        ELSE 'EMERALD_GREEN'                         -- 1. Without Arrear
    END AS visual_color_code
FROM students s;

COMMENT ON VIEW Placement_Summary_View IS 
'Unified HOD/Faculty analytics view computing 5-tier color codes and placement records.';
