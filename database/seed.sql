-- ==============================================================================
-- PSNA COLLEGE OF ENGINEERING AND TECHNOLOGY, DINDIGUL
-- DEPARTMENT OF INFORMATION TECHNOLOGY
-- DATABASE SEED DATA: IT Batches (2023-2027, Sections A to F) & Staff Users
-- Developed by: ANEESH KANNA N and ANNE BENILDA A
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. SEED USERS (Student, Tutor, Class Incharge, HOD)
-- ------------------------------------------------------------------------------
-- Default Passwords:
-- Student: Student@123
-- Teacher: Teacher@123
-- HOD:     Hod@123
-- ------------------------------------------------------------------------------
INSERT INTO users (id, email, phone, password_hash, role) VALUES
-- Student Accounts
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', '713821104001@psnacet.edu.in', '9876543210', '$2b$12$eK8W.P..MockPassStudentHash2026', 'STUDENT'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', '713821104002@psnacet.edu.in', '9876543211', '$2b$12$eK8W.P..MockPassStudentHash2026', 'STUDENT'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', '713821104003@psnacet.edu.in', '9876543212', '$2b$12$eK8W.P..MockPassStudentHash2026', 'STUDENT'),
-- Faculty / Tutors / Class Incharges
('b1eebc99-9c0b-4ef8-bb6d-6bb9bd380b21', 'staff@psnacet.edu.in', '9876543219', '$2b$12$eK8W.P..MockPassStaffHash2026', 'TEACHER'),
('b1eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'tutor.it.a@psnacet.edu.in', '9876543220', '$2b$12$eK8W.P..MockPassStaffHash2026', 'TEACHER'),
('b1eebc99-9c0b-4ef8-bb6d-6bb9bd380b23', 'class.incharge.iv@psnacet.edu.in', '9876543221', '$2b$12$eK8W.P..MockPassStaffHash2026', 'TEACHER'),
-- Head of Department (HOD)
('c2eebc99-9c0b-4ef8-bb6d-6bb9bd380c31', 'hod.it@psnacet.edu.in', '9876543200', '$2b$12$eK8W.P..MockPassHODHash2026', 'HOD')
ON CONFLICT (email) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 2. SEED STUDENTS (Batches Across Sections A through F)
-- ------------------------------------------------------------------------------
INSERT INTO students (
    register_no, roll_no, name, gender, department, year, section, 
    mobile, email, resume_url, cgpa, active_arrears, history_arrears, 
    cleared_arrears, attendance, is_locked, placement_status, placed_company, salary_package_lpa
) VALUES
-- SECTION A (4th Year, Batch 2023-2027)
('713821104001', '21IT001', 'Aneesh Kanna N', 'Male', 'IT', 'IV', 'A', '9876543210', '713821104001@psnacet.edu.in', '/resumes/713821104001_resume.pdf', 9.20, 0, 0, 0, 96.5, TRUE, 'PLACED', 'TCS Digital', 7.50),
('713821104002', '21IT002', 'Anne Benilda A', 'Female', 'IT', 'IV', 'A', '9876543211', '713821104002@psnacet.edu.in', '/resumes/713821104002_resume.pdf', 9.45, 0, 0, 0, 98.0, TRUE, 'PLACED', 'Zoho Corporation', 9.00),
('713821104003', '21IT003', 'Balamurugan K', 'Male', 'IT', 'IV', 'A', '9876543212', 'bala@psnacet.edu.in', '/resumes/713821104003_resume.pdf', 8.65, 0, 1, 1, 92.0, TRUE, 'ELIGIBLE', 'Cognizant', 4.50),

-- SECTION B (4th Year)
('713821104004', '21IT004', 'Dharani S', 'Female', 'IT', 'IV', 'B', '9876543213', 'dharani@psnacet.edu.in', '/resumes/713821104004_resume.pdf', 7.80, 1, 1, 0, 88.0, TRUE, 'NOT_ELIGIBLE', NULL, 0.00),
('713821104005', '21IT005', 'Gokulnath R', 'Male', 'IT', 'IV', 'B', '9876543214', 'gokul@psnacet.edu.in', '/resumes/713821104005_resume.pdf', 8.85, 0, 0, 0, 95.0, TRUE, 'ELIGIBLE', 'Hexaware', 5.00),

-- SECTION C (4th Year)
('713821104006', '21IT006', 'Harini M', 'Female', 'IT', 'IV', 'C', '9876543215', 'harini@psnacet.edu.in', '/resumes/713821104006_resume.pdf', 8.40, 0, 1, 1, 91.0, TRUE, 'ELIGIBLE', 'Wipro', 4.00),
('713821104007', '21IT007', 'Irfan Khan S', 'Male', 'IT', 'IV', 'C', '9876543216', 'irfan@psnacet.edu.in', '/resumes/713821104007_resume.pdf', 8.92, 0, 0, 0, 94.0, TRUE, 'PLACED', 'Infosys Specialist', 6.50),

-- SECTION D (3rd Year, Batch 2024-2028)
('713822104001', '22IT001', 'Kavitha P', 'Female', 'IT', 'III', 'D', '9876543217', 'kavitha@psnacet.edu.in', '/resumes/713822104001_resume.pdf', 8.75, 0, 0, 0, 93.5, TRUE, 'ELIGIBLE', NULL, 0.00),

-- SECTION E (2nd Year, Batch 2025-2029)
('713823104001', '23IT001', 'Manoj Kumar V', 'Male', 'IT', 'II', 'E', '9876543218', 'manoj@psnacet.edu.in', '/resumes/713823104001_resume.pdf', 8.30, 0, 0, 0, 90.0, TRUE, 'ELIGIBLE', NULL, 0.00),

-- SECTION F (1st Year, Batch 2026-2030)
('713824104001', '24IT001', 'Naveen Raj T', 'Male', 'IT', 'I', 'F', '9876543222', 'naveen@psnacet.edu.in', '/resumes/713824104001_resume.pdf', 8.50, 0, 0, 0, 96.0, TRUE, 'ELIGIBLE', NULL, 0.00)
ON CONFLICT (register_no) DO UPDATE SET
    cgpa = EXCLUDED.cgpa,
    placement_status = EXCLUDED.placement_status,
    placed_company = EXCLUDED.placed_company;

-- ------------------------------------------------------------------------------
-- 3. SEED SEMESTER MARKS (Anna University R-2022 Official Credits)
-- ------------------------------------------------------------------------------
-- Sem 1: 22, Sem 2: 25, Sem 3: 22.5, Sem 4: 22.5, Sem 5: 22.5, Sem 6: 21
-- ------------------------------------------------------------------------------
INSERT INTO semester_marks (register_no, semester_num, gpa, credits_earned, total_semester_credits, active_arrears, attendance_percentage) VALUES
('713821104001', 1, 9.00, 22.0, 22.0, 0, 98.0),
('713821104001', 2, 9.15, 25.0, 25.0, 0, 97.5),
('713821104001', 3, 9.20, 22.5, 22.5, 0, 95.0),
('713821104001', 4, 9.30, 22.5, 22.5, 0, 96.0),
('713821104001', 5, 9.25, 22.5, 22.5, 0, 94.5),
('713821104001', 6, 9.30, 21.0, 21.0, 0, 98.0),

('713821104002', 1, 9.20, 22.0, 22.0, 0, 99.0),
('713821104002', 2, 9.40, 25.0, 25.0, 0, 98.5),
('713821104002', 3, 9.50, 22.5, 22.5, 0, 97.0),
('713821104002', 4, 9.60, 22.5, 22.5, 0, 99.0),
('713821104002', 5, 9.45, 22.5, 22.5, 0, 98.0),
('713821104002', 6, 9.55, 21.0, 21.0, 0, 98.5)
ON CONFLICT (register_no, semester_num) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 4. SEED CERTIFICATES (NPTEL, GATE, AWS)
-- ------------------------------------------------------------------------------
INSERT INTO certificates (register_no, cert_title, file_url, ai_verification_status, ai_confidence_score, ai_audit_remarks, tutor_approved) VALUES
('713821104001', 'NPTEL Cloud Computing & Distributed Systems', '/certs/713821104001_nptel.pdf', 'VERIFIED', 99.80, 'Cryptographic font alignment and seal match official IIT Kharagpur template.', TRUE),
('713821104002', 'AWS Certified Solutions Architect Associate', '/certs/713821104002_aws.pdf', 'VERIFIED', 99.90, 'Digital verification badge confirmed via Amazon Web Services credential registry.', TRUE),
('713821104004', 'GATE 2026 Score Card', '/certs/713821104004_gate.pdf', 'TAMPER_SUSPECTED', 72.40, 'Warning: Baseline font misalignment and image pixel noise anomaly detected on candidate name.', FALSE);

-- ------------------------------------------------------------------------------
-- 5. SEED DIGITAL CORRECTION REQUESTS (Data Freezing Gate)
-- ------------------------------------------------------------------------------
INSERT INTO correction_requests (register_no, requested_field, new_value, reason, status, reviewed_by, tutor_remarks, reviewed_at) VALUES
('713821104001', 'cgpa', '9.25', 'Cleared revaluation for Semester 5 Machine Learning course with A+ grade.', 'APPROVED', 'Dr. S. Karthik (Tutor)', 'Revaluation marks verified with official Anna University portal.', CURRENT_TIMESTAMP),
('713821104003', 'mobile', '9876543299', 'Updated primary placement contact number for corporate HR communication.', 'PENDING', NULL, NULL, NULL);
