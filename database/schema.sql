-- ==============================================================================
-- PSNA COLLEGE OF ENGINEERING AND TECHNOLOGY, DINDIGUL
-- DEPARTMENT OF INFORMATION TECHNOLOGY
-- AI SMART PLACEMENT ASSISTANT AND MANAGEMENT SYSTEM
-- Database Schema: PostgreSQL 14+ / Neon / Supabase
-- Developed by: ANEESH KANNA N and ANNE BENILDA A
-- ==============================================================================

-- Enable UUID extension for cryptographic user IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing views and tables if rebuilding
DROP VIEW IF EXISTS Privacy_Masked_Student_View CASCADE;
DROP VIEW IF EXISTS Placement_Summary_View CASCADE;
DROP TABLE IF EXISTS correction_requests CASCADE;
DROP TABLE IF EXISTS certificates CASCADE;
DROP TABLE IF EXISTS semester_marks CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TYPE IF EXISTS user_role_enum CASCADE;
DROP TYPE IF EXISTS placement_status_enum CASCADE;
DROP TYPE IF EXISTS cert_status_enum CASCADE;
DROP TYPE IF EXISTS request_status_enum CASCADE;

-- ------------------------------------------------------------------------------
-- ENUM TYPES
-- ------------------------------------------------------------------------------
CREATE TYPE user_role_enum AS ENUM ('STUDENT', 'TEACHER', 'HOD');
CREATE TYPE placement_status_enum AS ENUM ('NOT_ELIGIBLE', 'ELIGIBLE', 'PLACED');
CREATE TYPE cert_status_enum AS ENUM ('VERIFIED', 'TAMPER_SUSPECTED');
CREATE TYPE request_status_enum AS ENUM ('PENDING', 'APPROVED', 'REJECTED');

-- ------------------------------------------------------------------------------
-- 1. USERS TABLE (Authentication & Role-Based Access Control)
-- ------------------------------------------------------------------------------
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    role user_role_enum NOT NULL DEFAULT 'STUDENT',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ------------------------------------------------------------------------------
-- 2. STUDENTS TABLE (Master Profile, Academics & Placement Tracking)
-- ------------------------------------------------------------------------------
CREATE TABLE students (
    register_no VARCHAR(20) PRIMARY KEY,
    roll_no VARCHAR(20) UNIQUE,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    department VARCHAR(50) DEFAULT 'IT' NOT NULL,
    year VARCHAR(5) NOT NULL CHECK (year IN ('I', 'II', 'III', 'IV')),
    section VARCHAR(5) NOT NULL CHECK (section IN ('A', 'B', 'C', 'D', 'E', 'F')),
    mobile VARCHAR(20),
    email VARCHAR(255) UNIQUE NOT NULL,
    resume_url VARCHAR(500),
    cgpa NUMERIC(4, 2) DEFAULT 0.00 CHECK (cgpa >= 0.00 AND cgpa <= 10.00),
    active_arrears INT DEFAULT 0 CHECK (active_arrears >= 0),
    history_arrears INT DEFAULT 0 CHECK (history_arrears >= 0),
    cleared_arrears INT DEFAULT 0 CHECK (cleared_arrears >= 0),
    attendance NUMERIC(5, 2) DEFAULT 100.00 CHECK (attendance >= 0.00 AND attendance <= 100.00),
    is_locked BOOLEAN DEFAULT TRUE NOT NULL, -- Data Freezing Gate Rule
    placement_status placement_status_enum DEFAULT 'ELIGIBLE' NOT NULL,
    placed_company VARCHAR(255),
    salary_package_lpa NUMERIC(5, 2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_students_year_sec ON students(year, section);
CREATE INDEX idx_students_placement ON students(placement_status);
CREATE INDEX idx_students_cgpa ON students(cgpa);

-- ------------------------------------------------------------------------------
-- 3. SEMESTER MARKS TABLE (Anna University R-2022 Course Evaluations)
-- ------------------------------------------------------------------------------
CREATE TABLE semester_marks (
    id SERIAL PRIMARY KEY,
    register_no VARCHAR(20) NOT NULL REFERENCES students(register_no) ON DELETE CASCADE,
    semester_num INT NOT NULL CHECK (semester_num >= 1 AND semester_num <= 8),
    gpa NUMERIC(4, 2) NOT NULL CHECK (gpa >= 0.00 AND gpa <= 10.00),
    credits_earned NUMERIC(4, 1) NOT NULL,
    total_semester_credits NUMERIC(4, 1) NOT NULL,
    active_arrears INT DEFAULT 0,
    attendance_percentage NUMERIC(5, 2) DEFAULT 100.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (register_no, semester_num)
);

CREATE INDEX idx_sem_marks_reg_no ON semester_marks(register_no);

-- ------------------------------------------------------------------------------
-- 4. CERTIFICATES TABLE (AI Tamper & Fraud Detection)
-- ------------------------------------------------------------------------------
CREATE TABLE certificates (
    id SERIAL PRIMARY KEY,
    register_no VARCHAR(20) NOT NULL REFERENCES students(register_no) ON DELETE CASCADE,
    cert_title VARCHAR(255) NOT NULL, -- e.g. NPTEL Cloud Computing, GATE 2026
    file_url VARCHAR(500) NOT NULL,
    ai_verification_status cert_status_enum DEFAULT 'VERIFIED' NOT NULL,
    ai_confidence_score NUMERIC(5, 2) DEFAULT 99.00,
    ai_audit_remarks TEXT,
    tutor_approved BOOLEAN DEFAULT FALSE,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_certs_reg_no ON certificates(register_no);
CREATE INDEX idx_certs_status ON certificates(ai_verification_status);

-- ------------------------------------------------------------------------------
-- 5. CORRECTION REQUESTS TABLE (Data Freezing Gate & Permission Workflow)
-- ------------------------------------------------------------------------------
CREATE TABLE correction_requests (
    id SERIAL PRIMARY KEY,
    register_no VARCHAR(20) NOT NULL REFERENCES students(register_no) ON DELETE CASCADE,
    requested_field VARCHAR(100) NOT NULL, -- 'cgpa', 'sem_gpa', 'name', 'attendance'
    new_value VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    status request_status_enum DEFAULT 'PENDING' NOT NULL,
    reviewed_by VARCHAR(255),
    tutor_remarks TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_corr_reg_no ON correction_requests(register_no);
CREATE INDEX idx_corr_status ON correction_requests(status);
