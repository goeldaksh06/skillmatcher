from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from app import db
from app.models import Assessment, Question, Answer, AssessmentResult, User
from app.services.skill_service import SkillService
from app.services.ai_service import AIService

class AssessmentService:
    """Service for managing the complete assessment workflow"""
    
    def __init__(self):
        self.skill_service = SkillService()
        self.ai_service = AIService()
    
    def create_assessment(self, recruiter_id: int, title: str, required_skills: str, 
                         threshold_percentage: int = 70, description: str = None) -> Assessment:
        """Create a new assessment"""
        parsed_skills = self.skill_service.parse_recruiter_skills(required_skills)
        
        assessment = Assessment(
            title=title,
            description=description,
            required_skills=parsed_skills,
            threshold_percentage=threshold_percentage,
            recruiter_id=recruiter_id,
            status='draft',
            expires_at=datetime.utcnow() + timedelta(days=7)  # Default 7 days expiry
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        return assessment
    
    def upload_resume_and_check_eligibility(self, assessment_id: int, resume_text: str, 
                                          filename: str = None) -> Tuple[bool, Dict]:
        """Upload resume and check candidate eligibility"""
        assessment = Assessment.query.get_or_404(assessment_id)
        
        # Store resume data
        assessment.resume_text = resume_text
        assessment.resume_filename = filename
        
        # Check skill matches
        skill_matches = self.skill_service.check_required_skills_in_resume(
            resume_text, assessment.required_skills
        )
        
        # Calculate eligibility
        eligibility_data = self.skill_service.calculate_eligibility(
            skill_matches, assessment.threshold_percentage
        )
        
        # Store results
        assessment.skill_matches = skill_matches
        assessment.eligibility_data = eligibility_data
        
        if eligibility_data["eligible"]:
            assessment.status = 'active'
        else:
            assessment.status = 'rejected'
        
        db.session.commit()
        
        return eligibility_data["eligible"], eligibility_data
    
    def generate_assessment_questions(self, assessment_id: int, questions_per_skill: int = 3) -> List[Question]:
        """Generate AI questions for the assessment"""
        assessment = Assessment.query.get_or_404(assessment_id)
        
        if not assessment.eligibility_data or not assessment.eligibility_data.get("eligible"):
            raise ValueError("Cannot generate questions for ineligible candidate")
        
        # Generate questions using AI
        ai_questions = self.ai_service.generate_questions_for_skills(
            assessment.required_skills, num_questions=questions_per_skill + 2  # Generate extra for randomization
        )
        
        # Randomize and select questions
        randomized_questions = self.ai_service.randomize_questions(ai_questions, questions_per_skill)
        
        # Create Question records
        questions = []
        order_index = 0
        
        for skill, question_texts in randomized_questions.items():
            for question_text in question_texts:
                question = Question(
                    assessment_id=assessment_id,
                    skill=skill,
                    question_text=question_text,
                    question_type='text',
                    order_index=order_index
                )
                questions.append(question)
                order_index += 1
        
        # Save all questions
        db.session.add_all(questions)
        db.session.commit()
        
        return questions
    
    def submit_answer(self, question_id: int, answer_text: str, time_spent: int = None) -> Answer:
        """Submit and grade an answer"""
        question = Question.query.get_or_404(question_id)
        
        # Create answer record
        answer = Answer(
            question_id=question_id,
            assessment_id=question.assessment_id,
            answer_text=answer_text,
            time_spent_seconds=time_spent
        )
        
        # Grade the answer using AI
        try:
            score, feedback = self.ai_service.grade_answer(
                question.skill, question.question_text, answer_text
            )
            answer.ai_score = score
            answer.ai_feedback = feedback
        except Exception as e:
            print(f"Error grading answer: {e}")
            answer.ai_score = 0.0
            answer.ai_feedback = "Error occurred during grading"
        
        db.session.add(answer)
        db.session.commit()
        
        return answer
    
    def complete_assessment(self, assessment_id: int) -> AssessmentResult:
        """Complete assessment and generate final results"""
        assessment = Assessment.query.get_or_404(assessment_id)
        
        # Get all answers for this assessment
        answers = Answer.query.filter_by(assessment_id=assessment_id).all()
        
        if not answers:
            raise ValueError("No answers found for this assessment")
        
        # Calculate skill scores
        skill_scores = {}
        skill_question_counts = {}
        
        for answer in answers:
            skill = answer.question.skill
            if skill not in skill_scores:
                skill_scores[skill] = 0
                skill_question_counts[skill] = 0
            
            skill_scores[skill] += answer.ai_score or 0
            skill_question_counts[skill] += 1
        
        # Average scores per skill
        for skill in skill_scores:
            if skill_question_counts[skill] > 0:
                skill_scores[skill] = round(skill_scores[skill] / skill_question_counts[skill], 2)
        
        # Calculate overall score
        overall_score = round(sum(skill_scores.values()) / len(skill_scores), 2) if skill_scores else 0
        
        # Determine pass/fail
        is_passed = overall_score >= 6.0  # Passing score of 6/10
        
        # Identify strengths and weaknesses
        strengths = [skill for skill, score in skill_scores.items() if score >= 7.0]
        weaknesses = [skill for skill, score in skill_scores.items() if score < 6.0]
        
        # Generate recommendations
        recommendations = self.ai_service.generate_assessment_recommendations(skill_scores, overall_score)
        
        # Create result record
        result = AssessmentResult(
            assessment_id=assessment_id,
            overall_score=overall_score,
            skill_scores=skill_scores,
            total_questions=len(answers),
            total_time_seconds=sum(answer.time_spent_seconds or 0 for answer in answers),
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            is_passed=is_passed
        )
        
        # Update assessment status
        assessment.status = 'completed'
        assessment.completed_at = datetime.utcnow()
        
        db.session.add(result)
        db.session.commit()
        
        return result
    
    def get_assessment_progress(self, assessment_id: int) -> Dict:
        """Get current progress of an assessment"""
        assessment = Assessment.query.get_or_404(assessment_id)
        questions = Question.query.filter_by(assessment_id=assessment_id).order_by(Question.order_index).all()
        answers = Answer.query.filter_by(assessment_id=assessment_id).all()
        
        answered_question_ids = {answer.question_id for answer in answers}
        
        progress_data = {
            'assessment': assessment.to_dict(),
            'total_questions': len(questions),
            'answered_questions': len(answers),
            'current_question': None,
            'progress_percentage': round((len(answers) / len(questions)) * 100, 1) if questions else 0
        }
        
        # Find next unanswered question
        for question in questions:
            if question.id not in answered_question_ids:
                progress_data['current_question'] = question.to_dict()
                break
        
        return progress_data