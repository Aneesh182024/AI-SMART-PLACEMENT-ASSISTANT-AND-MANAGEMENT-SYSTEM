# 🚀 Real-World Production Deployment Guide
### AI SMART PLACEMENT ASSISTANT AND MANAGEMENT SYSTEM
**PSNA College of Engineering and Technology, Dindigul — Department of Information Technology**  
*Developed by ANEESH KANNA N and ANNE BENILDA A (© 2026)*

---

To deploy the **Frontend**, **Backend API**, and **PostgreSQL Database** so students, faculty, and placement officers can access the system over the internet, follow either of the two industry-standard deployment methods below:

---

## 🏆 Method 1: Cloud-Native Deployment (Recommended — Free & Production Ready)

This is the standard modern setup used by universities and tech organizations. Each tier is deployed on dedicated, managed cloud infrastructure with automatic HTTPS/SSL and global CDN acceleration.

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│         FRONTEND CLIENT         │       │           BACKEND API           │       │       POSTGRESQL DATABASE       │
│             Vercel              │ ────▶ │          Render / Railway       │ ────▶ │        Supabase / Neon          │
│   (React 19 + Vite + Tailwind)  │ HTTPS │       (FastAPI + Python 3.13)   │ SQL   │    (Tables + Views + Seeds)     │
│   https://psna-placement.vercel │       │  https://psna-api.onrender.com  │       │   Managed PostgreSQL 15+        │
└─────────────────────────────────┘       └─────────────────────────────────┘       └─────────────────────────────────┘
```

---

### Step 1: Deploy PostgreSQL Database (via Supabase or Neon.tech)

1. **Sign Up**:
   - Go to [Supabase](https://supabase.com) (or [Neon.tech](https://neon.tech)) and create a free account.
2. **Create New Project**:
   - Project Name: `psna-placement-db`
   - Database Password: Create a strong password (save it safely).
   - Region: Select nearest region (e.g. `Singapore` or `Mumbai` for India).
3. **Run Database Migrations**:
   - In the Supabase/Neon dashboard, open the **SQL Editor**.
   - Copy and paste the contents of `database/schema.sql`, then click **Run**.
   - Copy and paste `database/views.sql`, then click **Run**.
   - Copy and paste `database/seed.sql`, then click **Run**.
4. **Copy Database Connection String**:
   - Navigate to **Project Settings** ➔ **Database** ➔ **Connection URI**.
   - Copy the URI: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres`

---

### Step 2: Deploy Backend API (via Render.com)

1. **Sign Up on Render**:
   - Visit [Render.com](https://render.com) and log in with your GitHub account.
2. **Create a New Web Service**:
   - Click **New +** ➔ **Web Service**.
   - Connect your GitHub repository: `AI-SMART-PLACEMENT-ASSISTANT-AND-MANAGEMENT-SYSTEM`.
3. **Configure Settings**:
   - **Name**: `psna-placement-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
4. **Add Environment Variables**:
   Under **Environment Variables**, add:
   | Key | Value | Description |
   |---|---|---|
   | `DATABASE_URL` | `postgresql://postgres:...` | Your Supabase/Neon connection string |
   | `JWT_SECRET_KEY` | `psna_cet_it_placement_secret_key_2026_aneesh_anne` | Secret for signing JWT tokens |
   | `SMTP_HOST` | `smtp.gmail.com` | Gmail SMTP server |
   | `SMTP_PORT` | `587` | STARTTLS port |
   | `SMTP_EMAIL` | `your_official_email@gmail.com` | Institutional sender email |
   | `SMTP_PASSWORD` | `xxxx xxxx xxxx xxxx` | 16-character Google App Password |
   | `GEMINI_API_KEY` | `AIzaSy...` | (Optional) Google Gemini API Key |
5. **Deploy**:
   - Click **Create Web Service**.
   - Render will build dependencies and provide a live URL, e.g.:
     `https://psna-placement-api.onrender.com`
   - Verify health: `https://psna-placement-api.onrender.com/health`
   - View live API docs: `https://psna-placement-api.onrender.com/docs`

---

### Step 3: Deploy Frontend Client (via Vercel)

1. **Sign Up on Vercel**:
   - Visit [Vercel.com](https://vercel.com) and sign in with GitHub.
2. **Import Repository**:
   - Click **Add New...** ➔ **Project**.
   - Select `AI-SMART-PLACEMENT-ASSISTANT-AND-MANAGEMENT-SYSTEM`.
3. **Configure Build Settings**:
   - **Root Directory**: Click *Edit* and select `frontend`.
   - **Framework Preset**: `Vite` (automatically detected).
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. **Set Production Environment Variable**:
   Under **Environment Variables**, add:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://psna-placement-api.onrender.com` (Your live Render backend URL from Step 2 without a trailing slash).
5. **Deploy**:
   - Click **Deploy**.
   - Within 60 seconds, Vercel will build and assign a global production domain, e.g.:
     `https://psna-placement-assistant.vercel.app`
   - The included `vercel.json` automatically manages client-side SPA routing (`/login`, `/student`, `/admin`, `/terms`).

---

## 🏢 Method 2: Campus Physical Server / Single VPS (Docker Compose)

If PSNA College has a dedicated Linux server (Ubuntu 22.04 / 24.04 LTS) in the IT Department Data Center or an AWS EC2 instance:

### 1. Prerequisites on the Server
```bash
sudo apt update && sudo apt install -y docker.io docker-compose git
sudo systemctl enable --now docker
```

### 2. Clone and Launch
```bash
git clone https://github.com/Aneesh182024/AI-SMART-PLACEMENT-ASSISTANT-AND-MANAGEMENT-SYSTEM.git
cd AI-SMART-PLACEMENT-ASSISTANT-AND-MANAGEMENT-SYSTEM

# (Optional) Create .env with your Gmail App Password & Gemini Key
nano .env
```

### 3. Launch Entire Full-Stack Application
```bash
# Builds and starts Database, Backend API, and Frontend Nginx in background
docker compose up -d --build
```

### 4. Verify Services
```bash
docker compose ps
```
- **Frontend Portal**: `http://<server-ip-or-domain>` (Port 80)
- **Backend API**: `http://<server-ip-or-domain>:8000` (Port 8000)
- **Interactive Docs**: `http://<server-ip-or-domain>:8000/docs`
- **PostgreSQL Database**: Port 5432 with persistent storage volume (`postgres_data`).

---

## 🔒 Post-Deployment Security Checklist

1. **Google App Passwords for Email**:
   - Enable 2-Step Verification on your Gmail account.
   - Go to **Security** ➔ **2-Step Verification** ➔ **App passwords**.
   - Create a 16-character password named `PSNA Placement` and set it as `SMTP_PASSWORD`.
2. **CORS Allow Origins**:
   - In `backend/app/main.py`, CORS is already configured to accept all incoming frontend URLs or you can restrict `allow_origins` to your specific Vercel domain (`https://psna-placement-assistant.vercel.app`).
3. **Data Freezing Gate**:
   - The Data Freezing rule (`is_locked = True`) is permanently enabled by default to safeguard academic integrity.
