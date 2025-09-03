import re
import os
import google.generativeai as genai

# ================================
# Skill Parsing & Eligibility Logic
# ================================

def parse_recruiter_skills(input_string: str):
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


def check_required_skills_in_resume(resume_text: str, required_skills: list):
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


def calculate_eligibility(skill_matches: dict, threshold: int = 70):
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
        "total_skills": total_skills
    }

# ================================
# Gemini AI Setup
# ================================

api_key = os.environ.get("GEMINI_API_KEY")
print("Loaded GEMINI_API_KEY:", api_key[:6], "...", api_key[-6:])
if not api_key:
    raise ValueError("⚠️ GEMINI_API_KEY not set. Run `setx GEMINI_API_KEY your_key` first.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ================================
# AI Question Generation
# ================================

def generate_ai_questions_for_skills(skills, num_questions=3):
    """
    Generate interview questions for each skill using Gemini AI.
    
    Args:
        skills (list): List of skills (e.g., ["Python", "SQL"]).
        num_questions (int): Number of questions per skill.
    
    Returns:
        dict: { "Python": ["Q1", "Q2", ...], "SQL": ["Q1", "Q2", ...] }
    """
    questions_by_skill = {}

    for skill in skills:
        prompt = f"""
        Generate {num_questions} interview questions to test a candidate's practical
        knowledge in {skill}. Mix beginner, intermediate, and advanced difficulty.
        Only return the questions as a numbered list.
        """

        response = model.generate_content(prompt)

        # Split lines, clean up numbering
        questions_text = response.text.strip()
        questions = [q.strip("0123456789. ") for q in questions_text.split("\n") if q.strip()]

        questions_by_skill[skill] = questions[:num_questions]

    return questions_by_skill

import random

def get_randomized_questions(ai_questions, num_per_skill=3):
    """
    Randomize and limit number of questions per skill.
    """
    randomized_questions = {}
    for skill, questions in ai_questions.items():
        shuffled = questions.copy()
        random.shuffle(shuffled)
        randomized_questions[skill] = shuffled[:num_per_skill]
    return randomized_questions

