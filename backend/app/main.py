from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import COLLEGE_NAME, DEPARTMENT, SYSTEM_TITLE, DEVELOPERS, CURRENT_YEAR
from app.routers import auth_router, academic_router, student_router, admin_router
from app.ai import ai_router

app = FastAPI(
    title=f"PSNA CET - {SYSTEM_TITLE}",
    description=(
        f"Backend API server for {COLLEGE_NAME} ({DEPARTMENT} Department). "
        f"Developed by {DEVELOPERS}. Implements Role-Based Access Control (RBAC), "
        f"Anna University R-2022 CBCS regulations engine, Data Freezing Gate, "
        f"and Privacy Masking Database Views."
    ),
    version="1.0.0"
)

# Configure CORS for Frontend React / Next.js integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Open for local development & production Vercel frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Sub-Routers
app.include_router(auth_router.router)
app.include_router(academic_router.router)
app.include_router(student_router.router)
app.include_router(admin_router.router)
app.include_router(ai_router.router)


@app.get("/", tags=["System Information"])
def root():
    return {
        "institution": COLLEGE_NAME,
        "department": DEPARTMENT,
        "system": SYSTEM_TITLE,
        "developers": DEVELOPERS,
        "copyright": f"© {CURRENT_YEAR} Developed by {DEVELOPERS}. All Rights Reserved.",
        "status": "ONLINE",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }

@app.get("/health", tags=["System Information"])
def health_check():
    return {"status": "healthy", "service": "PSNA Placement API Engine"}
