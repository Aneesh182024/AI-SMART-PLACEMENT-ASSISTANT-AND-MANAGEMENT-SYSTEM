import pymupdf # PyMuPDF
import re
from typing import Dict, List, Tuple
import io

class ResumeQualityScorerAgent:
    """
    Resume Quality Mark Test Agent for PSNA IT Department.
    Uses PyMuPDF to extract text patterns and evaluates against a 100-point rubric:
    1. Quantifiable Impact & Metrics (30 points)
    2. Action Verbs & Project Descriptions (20 points)
    3. Technical Skill Relevance (20 points)
    4. Layout, Formatting & Contact Structure (30 points)
    """

    ACTION_VERBS = [
        "architected", "developed", "engineered", "implemented", "optimized",
        "deployed", "designed", "constructed", "built", "accelerated",
        "automated", "spearheaded", "orchestrated", "integrated", "reduced",
        "increased", "enhanced", "resolved", "managed", "collaborated"
    ]

    TECH_KEYWORDS = [
        "python", "java", "c++", "c", "react", "fastapi", "django", "node.js",
        "sql", "postgresql", "mongodb", "machine learning", "deep learning",
        "docker", "kubernetes", "aws", "azure", "cloud", "git", "linux", "html", "css"
    ]

    @classmethod
    def extract_text_from_pdf(cls, file_bytes: bytes) -> str:
        """Extracts plain text from raw PDF bytes using PyMuPDF."""
        try:
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            full_text = []
            for page in doc:
                full_text.append(page.get_text())
            doc.close()
            return "\n".join(full_text)
        except Exception as e:
            return ""

    @classmethod
    def evaluate_resume(cls, resume_text: str) -> Dict:
        """
        Evaluates extracted resume text out of 100 points and produces
        actionable feedback checklists.
        """
        lower = resume_text.lower()
        checklist = []

        # -------------------------------------------------------------
        # Category 1: Quantifiable Impact & Metrics (30 points max)
        # -------------------------------------------------------------
        # Check for numbers, percentages (%), multipliers (2x, 3x), benchmarks
        metric_matches = re.findall(r'\b(?:\d+%(?:\.\d+)?|\d+x|\$\d+|\b\d+\s*(?:users|requests|ms|seconds|fps|lpa|stars|accuracy|latency)\b)', lower)
        numbers_count = len(re.findall(r'\b\d{2,}\b', lower))
        
        metrics_score = 0
        if len(metric_matches) >= 3 or numbers_count >= 5:
            metrics_score = 30
            checklist.append({
                "category": "Quantifiable Metrics",
                "status": "PASS",
                "message": f"Excellent quantifiable impact detected ({len(metric_matches)} metric markers found, e.g. performance percentages / user scales)."
            })
        elif len(metric_matches) >= 1 or numbers_count >= 2:
            metrics_score = 18
            checklist.append({
                "category": "Quantifiable Metrics",
                "status": "WARN",
                "message": "Moderate metric indicators detected. Suggestion: Add more numeric impact statements to your project descriptions (e.g. 'Reduced API latency by 35%')."
            })
        else:
            metrics_score = 8
            checklist.append({
                "category": "Quantifiable Metrics",
                "status": "FAIL",
                "message": "Missing quantifiable achievements! Always include numbers, percentages, or scale metrics in bullet points."
            })

        # -------------------------------------------------------------
        # Category 2: Action Verbs & Project Descriptions (20 points max)
        # -------------------------------------------------------------
        found_verbs = [v for v in cls.ACTION_VERBS if re.search(rf'\b{v}\b', lower)]
        verbs_score = 0
        if len(found_verbs) >= 5:
            verbs_score = 20
            checklist.append({
                "category": "Action Verbs",
                "status": "PASS",
                "message": f"Strong engineering action verbs used ({', '.join(found_verbs[:4])})."
            })
        elif len(found_verbs) >= 2:
            verbs_score = 13
            checklist.append({
                "category": "Action Verbs",
                "status": "WARN",
                "message": f"Only a few action verbs identified ({', '.join(found_verbs)}). Replace passive phrases like 'worked on' or 'helped with' with active verbs like 'Architected' or 'Optimized'."
            })
        else:
            verbs_score = 6
            checklist.append({
                "category": "Action Verbs",
                "status": "FAIL",
                "message": "Weak action verbs detected. Begin each project bullet point with strong technical action verbs."
            })

        # -------------------------------------------------------------
        # Category 3: Technical Skill Stack Relevance (20 points max)
        # -------------------------------------------------------------
        found_skills = [s for s in cls.TECH_KEYWORDS if re.search(rf'\b{re.escape(s)}\b', lower)]
        skills_score = 0
        if len(found_skills) >= 6:
            skills_score = 20
            checklist.append({
                "category": "Technical Depth",
                "status": "PASS",
                "message": f"Comprehensive modern technical stack detected ({len(found_skills)} skills matched)."
            })
        elif len(found_skills) >= 3:
            skills_score = 14
            checklist.append({
                "category": "Technical Depth",
                "status": "WARN",
                "message": f"Found core skills ({', '.join(found_skills)}). Consider highlighting complementary databases, cloud tools, or testing frameworks."
            })
        else:
            skills_score = 8
            checklist.append({
                "category": "Technical Depth",
                "status": "FAIL",
                "message": "Limited technical keywords detected. Ensure programming languages, libraries, and frameworks are explicitly categorized."
            })

        # -------------------------------------------------------------
        # Category 4: Layout, Formatting & Contact Structure (30 points max)
        # -------------------------------------------------------------
        has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+', lower))
        has_phone = bool(re.search(r'\b(?:\+?\d{1,3}[- ]?)?\d{10}\b', lower))
        has_github = bool("github" in lower or "linkedin" in lower)
        has_sections = bool("education" in lower and "project" in lower)

        structure_score = 0
        if has_email: structure_score += 7
        if has_phone: structure_score += 7
        if has_github: structure_score += 8
        if has_sections: structure_score += 8

        if structure_score >= 26:
            checklist.append({
                "category": "Layout & Structure",
                "status": "PASS",
                "message": "Clear reverse-chronological structure with complete contact info and portfolio/GitHub links."
            })
        else:
            checklist.append({
                "category": "Layout & Structure",
                "status": "WARN",
                "message": "Missing key structural headers or professional links. Ensure GitHub, LinkedIn, and phone contacts are prominent."
            })

        # Final Score Calculation
        total_score = min(100, metrics_score + verbs_score + skills_score + structure_score)

        return {
            "overall_score": total_score,
            "max_score": 100,
            "score_breakdown": {
                "quantifiable_metrics": {"score": metrics_score, "max": 30},
                "action_verbs": {"score": verbs_score, "max": 20},
                "technical_skills": {"score": skills_score, "max": 20},
                "layout_and_structure": {"score": structure_score, "max": 30}
            },
            "identified_skills": found_skills,
            "identified_verbs": found_verbs,
            "checklist": checklist,
            "placement_readiness": "EXCELLENT" if total_score >= 85 else ("GOOD" if total_score >= 70 else "NEEDS_IMPROVEMENT")
        }
