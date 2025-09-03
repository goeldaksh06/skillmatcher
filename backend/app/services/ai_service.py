import os
import random
from typing import List, Dict, Tuple
import google.generativeai as genai

class AIService:
    """Service for AI-powered question generation and answer grading"""
    
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def generate_questions_for_skills(self, skills: List[str], num_questions: int = 3) -> Dict[str, List[str]]:
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

            try:
                response = self.model.generate_content(prompt)
                
                # Split lines, clean up numbering
                questions_text = response.text.strip()
                questions = [q.strip("0123456789. ") for q in questions_text.split("\n") if q.strip()]
                
                questions_by_skill[skill] = questions[:num_questions]
            except Exception as e:
                print(f"Error generating questions for {skill}: {e}")
                # Fallback questions
                questions_by_skill[skill] = [
                    f"Explain the core concepts of {skill}",
                    f"Describe a project where you used {skill}",
                    f"What are the best practices when working with {skill}?"
                ][:num_questions]

        return questions_by_skill
    
    def randomize_questions(self, ai_questions: Dict[str, List[str]], num_per_skill: int = 3) -> Dict[str, List[str]]:
        """
        Randomize and limit number of questions per skill.
        """
        randomized_questions = {}
        for skill, questions in ai_questions.items():
            shuffled = questions.copy()
            random.shuffle(shuffled)
            randomized_questions[skill] = shuffled[:num_per_skill]
        return randomized_questions
    
    def grade_answer(self, skill: str, question: str, candidate_answer: str) -> Tuple[float, str]:
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
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Parse Score and Feedback
            score_line = [line for line in text.split("\n") if line.lower().startswith("score:")]
            feedback_line = [line for line in text.split("\n") if line.lower().startswith("feedback:")]
            
            score = float(score_line[0].split(":")[1].strip()) if score_line else 0
            feedback = feedback_line[0].split(":",1)[1].strip() if feedback_line else "No feedback available"
            
            return score, feedback
        except Exception as e:
            print(f"Error grading answer: {e}")
            return 0.0, "Error occurred during grading"
    
    def generate_assessment_recommendations(self, skill_scores: Dict[str, float], overall_score: float) -> str:
        """Generate AI-powered recommendations based on assessment results"""
        prompt = f"""
        Based on the following assessment results, provide constructive recommendations for the candidate:
        
        Overall Score: {overall_score}/10
        Skill Scores: {skill_scores}
        
        Provide specific, actionable recommendations for improvement in areas where the candidate scored below 7/10.
        Also highlight their strengths. Keep the response professional and encouraging.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return "Unable to generate recommendations at this time."