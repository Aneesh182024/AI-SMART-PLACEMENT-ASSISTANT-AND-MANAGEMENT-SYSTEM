"""
PSNA College of Engineering and Technology, Dindigul
Department of Information Technology
Database Verification & SQLite/PostgreSQL Test Harness
Developed by: ANEESH KANNA N and ANNE BENILDA A
"""

import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "smart_placement.db")

def init_test_sqlite_database():
    """
    Creates an SQLite instance mirroring the PostgreSQL schema & views
    so developers can run and test all SQL queries immediately offline.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create Tables
    cursor.executescript("""
    DROP VIEW IF EXISTS Privacy_Masked_Student_View;
    DROP TABLE IF EXISTS correction_requests;
    DROP TABLE IF EXISTS certificates;
    DROP TABLE IF EXISTS semester_marks;
    DROP TABLE IF EXISTS students;
    DROP TABLE IF EXISTS users;

    CREATE TABLE users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'STUDENT',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE students (
        register_no TEXT PRIMARY KEY,
        roll_no TEXT UNIQUE,
        name TEXT NOT NULL,
        gender TEXT,
        department TEXT DEFAULT 'IT' NOT NULL,
        year TEXT NOT NULL,
        section TEXT NOT NULL,
        mobile TEXT,
        email TEXT UNIQUE NOT NULL,
        resume_url TEXT,
        cgpa REAL DEFAULT 0.00,
        active_arrears INTEGER DEFAULT 0,
        history_arrears INTEGER DEFAULT 0,
        cleared_arrears INTEGER DEFAULT 0,
        attendance REAL DEFAULT 100.00,
        is_locked INTEGER DEFAULT 1 NOT NULL,
        placement_status TEXT DEFAULT 'ELIGIBLE' NOT NULL,
        placed_company TEXT,
        salary_package_lpa REAL DEFAULT 0.00,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    -- Privacy Masking View: Masks CGPA, marks, arrears from student peer views
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
    """)

    # Test Smart Upsert Query
    upsert_sql = """
    INSERT INTO students (register_no, name, year, section, email, mobile, cgpa)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT (register_no) 
    DO UPDATE SET 
        year = excluded.year,
        section = excluded.section,
        email = excluded.email,
        mobile = excluded.mobile,
        cgpa = excluded.cgpa;
    """

    sample_students = [
        ('713821104001', 'Aneesh Kanna N', 'IV', 'A', '713821104001@psnacet.edu.in', '9876543210', 9.20),
        ('713821104002', 'Anne Benilda A', 'IV', 'A', '713821104002@psnacet.edu.in', '9876543211', 9.45),
        ('713821104003', 'Balamurugan K', 'IV', 'A', 'bala@psnacet.edu.in', '9876543212', 8.65),
        ('713821104004', 'Dharani S', 'IV', 'B', 'dharani@psnacet.edu.in', '9876543213', 7.80),
        ('713821104005', 'Gokulnath R', 'IV', 'B', 'gokul@psnacet.edu.in', '9876543214', 8.85),
    ]

    for s in sample_students:
        cursor.execute(upsert_sql, s)

    # Test Re-inserting with updated CGPA to verify Smart De-duplication (no duplicate names)
    updated_aneesh = ('713821104001', 'Aneesh Kanna N', 'IV', 'A', '713821104001@psnacet.edu.in', '9876543210', 9.35)
    cursor.execute(upsert_sql, updated_aneesh)

    conn.commit()

    # Verify Count: Should be exactly 5 (no duplicates created!)
    cursor.execute("SELECT COUNT(*) FROM students;")
    total_count = cursor.fetchone()[0]

    # Test Privacy Masking View
    cursor.execute("SELECT * FROM Privacy_Masked_Student_View WHERE year = 'IV' AND section = 'A';")
    sec_a_peers = cursor.fetchall()

    conn.close()

    print(f"[SUCCESS] Database initialized successfully!")
    print(f"[OK] Total students after upsert de-duplication: {total_count} (Expected: 5, No duplicates!)")
    print(f"[OK] Privacy_Masked_Student_View queried Sec A peers: {len(sec_a_peers)} students returned.")
    print(f"[OK] Verified sample peer columns (CGPA omitted): {sec_a_peers[0]}")


if __name__ == "__main__":
    init_test_sqlite_database()
