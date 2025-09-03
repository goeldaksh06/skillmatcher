import re
from typing import List, Dict

class SkillService:
    """Service for skill parsing and matching operations"""
    
    @staticmethod
    def parse_recruiter_skills(input_string: str) -> List[str]:
        """
        Parse recruiter-provided skills from a comma-separated string.
        Preserves acronyms like SQL, AI, ML in uppercase.
        """
        if not input_string:
            return []

        skills = []
        for skill in input_string.split(","):
            clean_skill = skill.strip()

            if not clean_skill:
                continue

            # If acronym (2-4 uppercase letters), preserve it
            if re.fullmatch(r"[A-Z]{2,4}", clean_skill.upper()):
                skills.append(clean_skill.upper())
            else:
                skills.append(clean_skill.title())

        return skills
    
    @staticmethod
    def check_required_skills_in_resume(resume_text: str, required_skills: List[str]) -> Dict[str, bool]:
        """
        Check if recruiter-required skills are present in the resume text.
        Uses regex with word boundaries for accurate matching.
        """
        results = {}

        for skill in required_skills:
            # Escape special chars like C++
            pattern = r"\b" + re.escape(skill) + r"\b"
            found = re.search(pattern, resume_text, flags=re.IGNORECASE) is not None
            results[skill] = found

        return results
    
    @staticmethod
    def calculate_eligibility(skill_matches: Dict[str, bool], threshold: int = 70) -> Dict:
        """
        Calculate candidate eligibility based on matched skills.
        
        Args:
            skill_matches (dict): Skill -> True/False
            threshold (int): Minimum % of skills required (default=70)
        
        Returns:
            dict: Eligibility report
        """
        total_skills = len(skill_matches)
        found_skills = sum(1 for match in skill_matches.values() if match)

        if total_skills == 0:
            match_percent = 0
        else:
            match_percent = (found_skills / total_skills) * 100

        eligible = match_percent >= threshold

        return {
            "eligible": eligible,
            "match_percent": round(match_percent, 2),
            "found_skills": found_skills,
            "total_skills": total_skills,
            "matched_skills": [skill for skill, found in skill_matches.items() if found],
            "missing_skills": [skill for skill, found in skill_matches.items() if not found]
        }