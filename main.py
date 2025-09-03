from step2_skill_verification import (
    parse_recruiter_skills,
    check_required_skills_in_resume,
    calculate_eligibility,
    generate_ai_questions_for_skills,
    get_randomized_questions,
    model  # Gemini AI model
)

def grade_answer(skill, question, candidate_answer):
    """
    Uses Gemini AI to grade a candidate's answer.
    Returns a score out of 10 and feedback.
    """
    prompt = f"""
    You are an expert technical interviewer.
    Evaluate the candidate's answer to the following question.
    
    Skill: {skill}
    Question: {question}
    Candidate Answer: {candidate_answer}
    
    Score the answer from 0 to 10, considering correctness, clarity, and completeness.
    Provide a short feedback summary.
    Format your response as:
    Score: <number>
    Feedback: <text>
    """
    
    response = model.generate_content(prompt)
    text = response.text.strip()
    
    # Parse Score and Feedback
    score_line = [line for line in text.split("\n") if line.lower().startswith("score:")]
    feedback_line = [line for line in text.split("\n") if line.lower().startswith("feedback:")]
    
    score = float(score_line[0].split(":")[1].strip()) if score_line else 0
    feedback = feedback_line[0].split(":",1)[1].strip() if feedback_line else "No feedback"
    
    return score, feedback


if __name__ == "__main__":
    # =========================
    # Step 1: Recruiter Input
    # =========================
    recruiter_input = input("Enter required skills (comma-separated): ").strip()
    if not recruiter_input:
        recruiter_input = "Python, SQL, React, Machine Learning, AI, ML"

    parsed_skills = parse_recruiter_skills(recruiter_input)

    # =========================
    # Step 2: Candidate Resume
    # =========================
    resume_text = input("\nPaste candidate resume text:\n").strip()
    if not resume_text:
        resume_text = """
        I am a Computer Science student skilled in Python, SQL, and Machine Learning.
        I have built projects using Flask, AI, and TensorFlow.
        """

    skill_matches = check_required_skills_in_resume(resume_text, parsed_skills)
    eligibility = calculate_eligibility(skill_matches, threshold=70)

    if not eligibility["eligible"]:
        print("\nCandidate does not meet the minimum skill threshold. Exiting...")
        exit()

    # =========================
    # Step 3: Generate & Randomize Questions
    # =========================
    ai_questions = generate_ai_questions_for_skills(parsed_skills, num_questions=5)
    randomized_questions = get_randomized_questions(ai_questions, num_per_skill=3)

    # =========================
    # Step 4: Candidate Answering & AI Grading
    # =========================
    candidate_scores = {}
    for skill, questions in randomized_questions.items():
        print(f"\n--- Skill: {skill} ---")
        skill_total_score = 0
        for q in questions:
            print(f"\nQuestion: {q}")
            answer = input("Your Answer: ").strip()
            score, feedback = grade_answer(skill, q, answer)
            print(f"Score: {score}/10 | Feedback: {feedback}")
            skill_total_score += score

        # Average score per skill
        candidate_scores[skill] = round(skill_total_score / len(questions), 2)

    # =========================
    # Step 5: Overall Report
    # =========================
    print("\n--- Candidate Evaluation Report ---")
    for skill, avg_score in candidate_scores.items():
        print(f"{skill}: {avg_score}/10")
    overall_score = round(sum(candidate_scores.values()) / len(candidate_scores), 2)
    print(f"\nOverall Candidate Score: {overall_score}/10")
