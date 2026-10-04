# 🎓 AI SMART PLACEMENT ASSISTANT AND MANAGEMENT SYSTEM
### PSNA COLLEGE OF ENGINEERING AND TECHNOLOGY, DINDIGUL
**Department of Information Technology**  
*Autonomous Institution Affiliated to Anna University | Accredited by NAAC with 'A' Grade | NBA Accredited*

---

> **© 2026 Developed by ANEESH KANNA N and ANNE BENILDA A. All Rights Reserved.**  
> *Governance & Privacy Portfolio — Academic Year 2026*

---

## 📌 Executive Summary

The **AI Smart Placement Assistant and Management System** is an enterprise-grade academic placement automation platform engineered specifically for the **Department of Information Technology at PSNA College of Engineering and Technology, Dindigul**.

The platform modernizes institutional placement workflows through **Anna University R-2022 Regulations Engine**, **Google Gemini AI natural language processing**, **PyMuPDF resume analytics**, **OpenCV certificate forensic analysis**, **Smart Excel de-duplication ingestion**, **5-tier color-coded openpyxl roster generation**, and **production SMTP Email OTP password security**.

---

## 🏛️ System Architecture

```
                       ┌────────────────────────────────────────────────────────┐
                       │                   CLIENT INTERFACE                     │
                       │   React 19 + Vite + Tailwind CSS v4 + Lucide + Recharts│
                       │         "Pearl Emerald & Aqua Pink" Design System      │
                       └───────────────────────────┬────────────────────────────┘
                                                   │ HTTPS / REST API
                                                   ▼
                       ┌────────────────────────────────────────────────────────┐
                       │                   FASTAPI API SERVER                   │
                       │           Python 3.13 + Uvicorn + Pydantic v2          │
                       │           JWT RBAC (STUDENT / TEACHER / HOD)           │
                       └─────────┬───────────────────────────────┬──────────────┘
                                 │                               │
        ┌────────────────────────┼───────────────────────────────┼────────────────────────┐
        ▼                        ▼                               ▼                        ▼
┌──────────────────┐   ┌───────────────────┐           ┌───────────────────┐    ┌──────────────────┐
│   AI AUTOMATION  │   │  ACADEMIC ENGINE  │           │   EXCEL SERVICE   │    │  EMAIL SERVICE   │
│      SUITE       │   │  Anna Univ R-2022 │           │ openpyxl / 5-Tier │    │  smtplib:587     │
├──────────────────┤   ├───────────────────┤           ├───────────────────┤    ├──────────────────┤
│• Gemini Chatbot  │   │• 163 Credit Model │           │• Smart Ingestion  │    │• STARTTLS Gmail  │
│• PyMuPDF Resume  │   │• 75% Attendance SA│           │• PostgreSQL Upsert│    │• Resend API Fallb│
│• OpenCV Forensic │   │• 45% EndSem / 50% │           │• 5-Tier Colors    │    │• 6-Digit Secrets │
│• OCR Verification│   │• Data Freezing Gt │           │• Custom Legend    │    │• 5-Min Expiry    │
└──────────────────┘   └───────────────────┘           └───────────────────┘    └──────────────────┘
        │                        │                               │                        │
        └────────────────────────┴───────────────┬───────────────┴────────────────────────┘
                                                 │
                                                 ▼
                               ┌──────────────────────────────────┐
                               │       DATABASE & PRIVACY         │
                               │        PostgreSQL 15+            │
                               │  Privacy_Masked_Student_View     │
                               │  Placement_Summary_View          │
                               │  Digital Correction Requests     │
                               └──────────────────────────────────┘
```

---

## 🌟 Core Technical Modules

### 1. 🤖 AI Automation Suite (`backend/app/ai/`)
Built with a dual-engine architecture: uses Google Gemini API (`gemini-2.0-flash` / `gemini-1.5-flash`) when configured, with an offline deterministic rule/regex NLP fallback engine.

- **Placement AI Chatbot (`chatbot_agent.py`)**:
  - Staff prompt example: *"Show me IT 4th-year Sec A students with Python skills, CGPA above 8.5, max 1 backlog, and mark them Eligible for Zoho"*.
  - Extracts structured JSON:
    ```json
    {
      "department": "IT",
      "year": "IV",
      "section": "A",
      "required_skills": ["Python"],
      "minimum_cgpa": 8.5,
      "maximum_allowed_arrears": 1,
      "action": "MARK_ELIGIBLE",
      "company": "Zoho"
    }
    ```
  - Automatically queries the student database and updates eligibility flags in a single command.

- **Resume Quality Mark Test Agent (`resume_quality_agent.py`)**:
  - Extracts raw text, layout blocks, and section hierarchies from PDF resumes using `pymupdf`.
  - Computes an objective **100-Point Scoring Rubric**:
    - **Quantifiable Metrics (30 pts)**: Regex detection of percentages, revenue, time savings, and data numbers.
    - **Action Verbs (20 pts)**: Analysis of strong engineering impact verbs (*architected, engineered, deployed, reduced, led*).
    - **Technical Skills Alignment (20 pts)**: Cloud, Web, Database, and Core Programming languages.
    - **Layout Completeness (30 pts)**: Projects, Education, Experience, Certifications, Contact details.
  - Outputs an actionable improvement checklist with prioritized suggestions.

- **Certificate Fraud Detection Agent (`cert_fraud_agent.py`)**:
  - **Error Level Analysis (ELA)**: Re-compresses candidate certificates at 90% JPEG quality to compute pixel-level compression artifact differences; flags digital copy-paste manipulation.
  - **Laplacian Edge Variance**: Detects localized blur anomalies and pasted badge artifacts.
  - **Baseline Font Misalignment**: Detects edited student names and roll numbers using bounding-box center variance.
  - Generates tamper heatmaps and classification status: `VERIFIED` vs `TAMPER_SUSPECTED`.

---

### 2. 📊 Excel Ingestion & 5-Tier Color-Coded Export Engine (`backend/app/excel_service.py`)
Powered by `openpyxl` with dynamic stream generation:

- **Smart Bulk Ingestion (`POST /api/admin/upload-excel`)**:
  - Ingests both `.xlsx` and `.csv` roster files.
  - Columns: `Register No`, `Name`, `Gender`, `Year`, `Section`, `Email`, `Mobile`, `CGPA`, `Arrears`.
  - **PostgreSQL Smart Upsert**: Updates existing student academic records (`cgpa`, `active_arrears`, `year`, `section`, `email`, `mobile`) based on `register_no` without duplicating names or generating multiple records.
- **5-Tier Color-Coded Export (`GET /api/admin/export-excel`)**:
  - Official PSNA IT Department Header Banner across Rows 1-3.
  - 13 Columns Structure: `Register No`, `Student Name`, `Gender`, `Year`, `Sec`, `Email Address`, `Mobile`, `CGPA`, `Active Arrears`, `Subject Code & Title`, `Semester`, `Drive Eligibility`, `Placement Status & Company (LPA)`.
  - **Conditional Cell Styling Rules**:
    1. **Emerald Green (`#10B981`)**: Student's *Register Number* column if Without Arrear.
    2. **Crimson Red (`#EF4444`)**: Specific *Failed Subject* column for Current Arrear (`IT3402 Operating Systems (RA)`).
    3. **Amber Orange (`#F59E0B`)**: *Subject cell* + *Semester column* for Previous Arrear (`MA3151 Matrices & Calculus` | `Semester 1`).
    4. **Soft Pastel Blue (`#3B82F6`)**: *Cleared Subject* + *Cleared Sem column* for Previous Arrear Cleared (`IT3301 Data Structures` | `Semester 3`).
    5. **Bright Gold / Yellow (`#EAB308`)**: Student's *Register Number* column for High CGPA Top Performer (`CGPA >= 9.00`).
  - Embedded legend table explaining all color codes.
  - Automated column width calculation based on maximum string lengths with padding.

---

### 3. ✉️ Production Email OTP Verification Service (`backend/app/email_service.py`)
- **Transport**: Python `smtplib` with `STARTTLS` on port 587 via `smtp.gmail.com` (Google 16-character App Passwords) with Resend API fallback.
- **Security**: Cryptographically secure 6-digit numeric OTP generated via Python's `secrets` module (`secrets.randbelow(900000) + 100000`).
- **Expiry Timer**: Enforces strict 5-minute validity window in `OTP_CACHE`.
- **Branded Email Template**:
  - Deep Emerald Green header banner (`#0D5C3A`).
  - College & Department title branding.
  - Prominent 6-digit OTP card (`38px` monospace, `letter-spacing: 12px`, `#F0FDF4` background with `#10B981` dashed border).
  - Expiry notice and security warning.
  - Attribution footer: `© 2026 Developed by ANEESH KANNA N and ANNE BENILDA A`.
- **Endpoints**:
  - `POST /api/auth/forgot-password`: Verifies user exists, generates OTP, dispatches email.
  - `POST /api/auth/verify-otp`: Validates OTP match, checks expiry, enforces $\ge 8$ char password policy with numbers/symbols, updates password hash, and invalidates OTP.

---

### 4. 📐 Anna University Regulations 2022 (CBCS) Engine (`backend/app/academic_engine.py`)
- **163 Total Degree Credit Model**:
  - Sem 1: **22.0** | Sem 2: **25.0** | Sem 3: **22.5** | Sem 4: **22.5**
  - Sem 5: **22.5** | Sem 6: **21.0** | Sem 7: **17.5** | Sem 8: **10.0**
- **Passing Requirements**:
  - **Aggregate Total Marks**: $\ge 50\%$
  - **End-Semester Examination**: $\ge 45\%$
  - If either condition is not met, the student is marked as **RA** (Re-Appearance, 0 Grade Points).
- **Shortage of Attendance (SA)**:
  - If attendance is $< 75\%$, grade is automatically overridden to **SA** (0 GP), requiring course re-enrollment.
- **Credit-Weighted Calculation Formula**:
  $$\text{GPA} = \frac{\sum (C_i \times \text{GP}_i)}{\sum C_i}, \quad \text{CGPA} = \frac{\sum (\text{Credits}_k \times \text{GPA}_k)}{\sum \text{Credits}_k}$$

---

### 5. 🛡️ Data Governance, Freezing Gate & Privacy
- **Data Freezing Rule (`is_locked = True`)**:
  - Student profiles are permanently locked after initial submission to prevent unapproved grade/arrear alterations.
- **Digital Correction Ticket Workflow**:
  - Students submit formal correction requests with proof.
  - Tutors / Faculty review, approve, or reject tickets via `POST /api/admin/review-correction`.
  - Approved requests automatically update student records.
- **Privacy-Masked Peer Directory (`GET /api/student/peers`)**:
  - Students can only view classmates in their own Year and Section.
  - **Strictly Hides**: CGPA, grades, marks, and arrear status to prevent peer stigma and protect academic confidentiality.
- **PostgreSQL Views (`database/views.sql`)**:
  - `Privacy_Masked_Student_View`: Returns only public student directory parameters.
  - `Placement_Summary_View`: Computes real-time 5-tier color indicators and placement statistics.

---

## 🎨 UI/UX Design System ("Pearl Emerald & Aqua Pink")

Built using **React 19**, **Vite**, **Tailwind CSS v4**, **Lucide Icons**, and **Recharts**:

| Token Name | Hex Code | Visual Application |
|---|---|---|
| **Canvas Background** | `#F4F7F6` | Ultra-clean pearl canvas |
| **Pearl Pink Accent** | `#FDF2F8` | Ambient badges, tags, and accent borders |
| **Card Background** | `#FFFFFF` | Cashmere bordered cards with soft drop shadows |
| **Border Neutral** | `#E2E8F0` | Subtle, clean container borders |
| **Primary Emerald** | `#0D5C3A` | Institutional action buttons, header banner |
| **Active Aqua Blue** | `#0EA5E9` | Focus rings, active tabs, secondary links |
| **Fresh Mint Green** | `#10B981` | Success states, clean record indicators |
| **Slate Charcoal** | `#1E293B` | High-contrast typography |

- **Global Institutional Header**: Displays 5 institutional logos (`PSNA`, `NBA`, `ARIIA`, `NIRF`, `NAAC 'A'`) across all views.
- **Viewport Optimization**: Strict viewport fitting ensuring developer attribution (`© 2026 Developed by ANEESH KANNA N and ANNE BENILDA A`) is immediately visible without scrolling.

---

## 🔌 API Endpoints Reference

### Authentication & Security (`/api/auth`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/auth/signup` | Public | Registers student (validates password $\ge 8$ chars, num, symbol, terms) |
| `POST` | `/api/auth/login` | Public | Authenticates credentials and issues signed JWT access token |
| `POST` | `/api/auth/forgot-password` | Public | Generates 6-digit OTP and dispatches branded email |
| `POST` | `/api/auth/verify-otp` | Public | Validates 5-min OTP, enforces strong password, resets hash |

### Academic Regulations Engine (`/api/academic`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/academic/calculate-gpa` | Authenticated | Calculates semester GPA with 45% end-sem & 75% attendance SA rules |
| `POST` | `/api/academic/calculate-cgpa` | Authenticated | Computes Anna University R-2022 credit-weighted cumulative CGPA |
| `GET` | `/api/academic/regulations` | Authenticated | Returns official R-2022 credit weights and grading scales |

### Student Portal (`/api/student`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/student/profile` | Student | Returns student academic profile and data freezing status |
| `GET` | `/api/student/peers` | Student | Section-segregated peer directory with masked CGPA/arrears |
| `POST` | `/api/student/request-correction` | Student | Submits digital permission ticket for locked data modifications |

### Faculty & HOD Control Center (`/api/admin`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/admin/roster` | Teacher / HOD | Returns complete placement roster with academic metrics |
| `POST` | `/api/admin/eligibility` | Teacher / HOD | One-click placement eligibility and company placement status |
| `POST` | `/api/admin/batch-eligibility` | Teacher / HOD | Batch eligibility update (triggered manually or by AI Chatbot) |
| `POST` | `/api/admin/upload-excel` | Teacher / HOD | Bulk spreadsheet ingestion with `register_no` de-duplication |
| `GET` | `/api/admin/export-excel` | Teacher / HOD | Streams 5-tier color-coded placement roster `.xlsx` |
| `GET` | `/api/admin/correction-requests` | Teacher / HOD | Lists pending student data correction requests |
| `POST` | `/api/admin/review-correction` | Teacher / HOD | Approves or rejects student correction requests |
| `GET` | `/api/admin/analytics` | Teacher / HOD | Returns KPI metrics and CGPA distribution chart data |

### AI Automation Suite (`/api/ai`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/ai/chatbot` | Teacher / HOD | Natural language prompt query & automated eligibility execution |
| `POST` | `/api/ai/resume-score` | Authenticated | PyMuPDF resume parser and 100-point rubric assessment |
| `POST` | `/api/ai/verify-certificate` | Authenticated | OpenCV forensic ELA & font baseline certificate inspection |

---

## 🚀 Quick Start & Installation

### Prerequisites
- **Python**: 3.11, 3.12, or 3.13
- **Node.js**: v18+ or v20+
- **npm**: v9+
- **PostgreSQL**: 15+ (Optional; in-memory store active by default)

---

### 1. Clone the Repository
```bash
git clone https://github.com/Aneesh182024/AI-SMART-PLACEMENT-ASSISTANT-AND-MANAGEMENT-SYSTEM.git
cd AI-SMART-PLACEMENT-ASSISTANT-AND-MANAGEMENT-SYSTEM
```

---

### 2. Backend API Setup
```bash
cd backend

# Create and activate virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required Python dependencies
pip install fastapi uvicorn pyjwt bcrypt openpyxl pymupdf opencv-python pytesseract pillow pydantic google-genai pytest

# Configure environment variables (Optional: for live SMTP & Gemini AI)
# Copy .env.example or set environment variables:
$env:JWT_SECRET_KEY="psna_cet_it_placement_secret_key_2026_aneesh_anne"
$env:SMTP_HOST="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_EMAIL="your_email@gmail.com"
$env:SMTP_PASSWORD="your_16_char_app_password"
$env:GEMINI_API_KEY="your_gemini_api_key"

# Run FastAPI backend server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Backend API**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

### 3. Frontend Client Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Start Vite React development server
npm run dev
```
- **Frontend URL**: `http://localhost:5173`

---

### 4. Database Setup (PostgreSQL)
```bash
cd ../database

# Execute Schema and Seed Data in PostgreSQL
psql -U postgres -d psna_placement -f schema.sql
psql -U postgres -d psna_placement -f views.sql
psql -U postgres -d psna_placement -f seed.sql

# Test in-memory / database test harness
python init_db.py
```

---

## 🧪 Automated Verification Test Suites

Run the built-in test suites to validate all system modules:

```bash
cd backend

# 1. Validate Excel Ingestion & 5-Tier Color Export Engine
python test_excel.py

# 2. Validate Production Email OTP Verification Service
python test_email_otp.py

# 3. Validate Live FastAPI API Routes
python test_routes.py
```

---

## 📁 Repository File Layout

```
AI-SMART-PLACEMENT-ASSISTANT-AND-MANAGEMENT-SYSTEM/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── chatbot_agent.py          # Gemini AI natural language filter parser
│   │   │   ├── resume_quality_agent.py   # PyMuPDF 100-point resume quality scorer
│   │   │   ├── cert_fraud_agent.py       # OpenCV Error Level Analysis & font checker
│   │   │   └── ai_router.py              # Sub-router exposing /api/ai endpoints
│   │   ├── routers/
│   │   │   ├── auth_router.py            # RBAC login, signup, and OTP endpoints
│   │   │   ├── academic_router.py        # Anna University R-2022 GPA/CGPA rules
│   │   │   ├── student_router.py         # Student profile & privacy-masked peers
│   │   │   └── admin_router.py           # Faculty control center & excel streams
│   │   ├── academic_engine.py            # Core R-2022 credit-weighted calculations
│   │   ├── auth.py                       # JWT token signing & bcrypt verification
│   │   ├── config.py                     # Institutional metadata & SMTP settings
│   │   ├── database_mock.py              # In-memory store & privacy view generator
│   │   ├── email_service.py              # Gmail SMTP / Resend & HTML template
│   │   ├── excel_service.py              # openpyxl 5-tier color coded roster engine
│   │   ├── main.py                       # FastAPI application entry point
│   │   └── models.py                     # Pydantic validation schemas
│   ├── test_email_otp.py                 # 9-point Email OTP validation suite
│   ├── test_excel.py                     # 5-tier color styling validation suite
│   └── test_routes.py                    # Live HTTP endpoint integration tests
│
├── frontend/
│   ├── public/
│   │   └── logos/                        # 5 official institutional logos
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx                # Global institutional 5-logo header
│   │   │   ├── Footer.jsx                # Developer copyright attribution banner
│   │   │   ├── OtpModal.jsx              # 6-digit OTP verification dialog
│   │   │   └── PortfolioModal.jsx        # Governance & Developer attribution
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx           # Locked to Department of IT
│   │   │   ├── AuthPage.jsx              # Role-tabbed login & signup portal
│   │   │   ├── TermsPage.jsx             # 15 institutional governance clauses
│   │   │   ├── StudentDashboard.jsx      # Student portal with Data Freezing Gate
│   │   │   └── AdminDashboard.jsx        # Faculty oversight, Recharts & 5-tier table
│   │   ├── App.jsx                       # Main application router
│   │   ├── index.css                     # Pearl Emerald & Aqua Pink tokens
│   │   └── main.jsx                      # Vite React entry point
│   ├── package.json
│   └── vite.config.js
│
├── database/
│   ├── schema.sql                        # PostgreSQL tables (users, students, etc.)
│   ├── views.sql                         # Privacy-Masked & Placement Summary views
│   ├── queries.sql                       # Documented Smart Upsert & Filter queries
│   ├── seed.sql                          # Demo students, staff, and semester marks
│   └── init_db.py                        # Database initialization script
│
└── README.md                             # Comprehensive system documentation
```

---

## 👥 Authors & Institutional Ownership

This system was designed, engineered, and developed for:

**PSNA College of Engineering and Technology, Dindigul - 624622**  
*Department of Information Technology*

- **ANEESH KANNA N** — Core Architecture, AI Engine, Backend APIs & Design Systems
- **ANNE BENILDA A** — Academic Regulations Engine, Database Governance & QA

```
© 2026 Developed by ANEESH KANNA N and ANNE BENILDA A. All Rights Reserved.
Licensed under Institutional Academic Use for PSNA CET Department of Information Technology.
```
