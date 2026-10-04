from typing import List, Dict, Tuple
from app.config import R2022_SEMESTER_CREDITS
from app.models import SubjectMarkInput

class AnnaUniversityR2022Engine:
    """
    Official Anna University R-2022 CBCS Regulations Calculation Engine
    Structured for PSNA College of Engineering and Technology (IT Dept).
    """

    @staticmethod
    def evaluate_subject(
        internal_marks: float,
        end_sem_marks: float,
        attendance_percentage: float = 100.0,
        end_sem_max: float = 100.0
    ) -> Tuple[str, int, str]:
        """
        Evaluates a single course under Anna University R-2022 rules.
        Returns: (Letter Grade, Grade Point, Status Remark)
        """
        # Rule 1: Attendance Gate (< 75% -> Automatic SA Override)
        if attendance_percentage < 75.0:
            return "SA", 0, "Shortage of Attendance (SA Override - 0 GP)"

        # Calculate Total Percentage
        # End sem scaled to 100 for threshold check
        end_sem_scaled = (end_sem_marks / end_sem_max) * 100.0 if end_sem_max != 100.0 else end_sem_marks
        total_score = internal_marks + end_sem_marks

        # Rule 2: Passing Gate Thresholds
        # Must secure:
        # a) Overall aggregate >= 50%
        # b) End-Semester examination baseline >= 45%
        if total_score < 50.0 or end_sem_scaled < 45.0:
            return "RA", 0, "Re-Appearance Arrear (RA - Failed passing threshold)"

        # Rule 3: 10-Point Grade Point (GP) Scale Mapping
        if 91.0 <= total_score <= 100.0:
            return "O", 10, "Outstanding"
        elif 81.0 <= total_score <= 90.0:
            return "A+", 9, "Excellent"
        elif 71.0 <= total_score <= 80.0:
            return "A", 8, "Very Good"
        elif 61.0 <= total_score <= 70.0:
            return "B+", 7, "Good"
        elif 50.0 <= total_score <= 60.0:
            return "B", 6, "Average"
        else:
            return "RA", 0, "Re-Appearance Arrear"

    @classmethod
    def calculate_semester_gpa(cls, semester_num: int, subjects: List[SubjectMarkInput]) -> Dict:
        """
        Calculates Semester GPA:
        GPA = SUM(Course Credits * Grade Points Got) / SUM(Total Credits in that Semester)
        """
        total_registered_credits = 0.0
        total_earned_credits = 0.0
        weighted_grade_points = 0.0
        active_arrears = 0
        evaluated_subjects = []

        for sub in subjects:
            grade, gp, remark = cls.evaluate_subject(
                internal_marks=sub.internal_marks,
                end_sem_marks=sub.end_sem_marks,
                attendance_percentage=sub.attendance_percentage
            )

            total_registered_credits += sub.credits
            weighted_grade_points += (sub.credits * gp)

            if gp > 0:
                total_earned_credits += sub.credits
            else:
                active_arrears += 1

            evaluated_subjects.append({
                "subject_code": sub.subject_code,
                "subject_name": sub.subject_name,
                "credits": sub.credits,
                "letter_grade": grade,
                "grade_point": gp,
                "status_remark": remark,
                "is_cleared": gp > 0
            })

        # Calculate weighted GPA
        official_sem_credits = R2022_SEMESTER_CREDITS.get(semester_num, total_registered_credits)
        divisor = total_registered_credits if total_registered_credits > 0 else official_sem_credits
        gpa = round(weighted_grade_points / divisor, 2) if divisor > 0 else 0.0

        return {
            "semester_num": semester_num,
            "semester_gpa": gpa,
            "total_registered_credits": total_registered_credits,
            "total_earned_credits": total_earned_credits,
            "official_r2022_credits": official_sem_credits,
            "active_arrears_in_sem": active_arrears,
            "subjects_breakdown": evaluated_subjects
        }

    @classmethod
    def calculate_cumulative_cgpa(cls, semester_results: Dict[int, Dict]) -> Dict:
        """
        Calculates Cumulative CGPA across completed terms:
        CGPA = SUM(Credits of All Cleared Courses * Grade Points Got) / SUM(Total Cleared Credits Overall)
        """
        total_cleared_quality_points = 0.0
        total_cleared_credits = 0.0
        total_arrears = 0

        for sem_num, data in semester_results.items():
            sem_credits = data.get("official_credits", R2022_SEMESTER_CREDITS.get(int(sem_num), 22.0))
            sem_gpa = data.get("gpa", 0.0)
            arrears = data.get("arrears", 0)

            total_arrears += arrears
            total_cleared_quality_points += (sem_credits * sem_gpa)
            total_cleared_credits += sem_credits

        cgpa = round(total_cleared_quality_points / total_cleared_credits, 2) if total_cleared_credits > 0 else 0.0

        # Yearly Weighted Analytics (Sem 1+2 = Year 1, etc.)
        year_1_gpa = None
        if 1 in semester_results and 2 in semester_results:
            c1, c2 = R2022_SEMESTER_CREDITS[1], R2022_SEMESTER_CREDITS[2]
            g1, g2 = semester_results[1].get("gpa", 0.0), semester_results[2].get("gpa", 0.0)
            year_1_gpa = round(((c1 * g1) + (c2 * g2)) / (c1 + c2), 2)

        return {
            "cumulative_cgpa": cgpa,
            "total_cleared_credits": total_cleared_credits,
            "total_arrears_count": total_arrears,
            "year_1_weighted_gpa": year_1_gpa,
            "is_all_clear": total_arrears == 0
        }
