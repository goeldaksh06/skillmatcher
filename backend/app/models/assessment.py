from datetime import datetime
from app import db
import json

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.JSON, nullable=False)  # List of skills
    threshold_percentage = db.Column(db.Integer, default=70)
    
    # Foreign keys
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Assessment metadata
    status = db.Column(db.String(20), default='draft')  # draft, active, completed, expired
    resume_text = db.Column(db.Text)
    resume_filename = db.Column(db.String(255))
    skill_matches = db.Column(db.JSON)  # Skill matching results
    eligibility_data = db.Column(db.JSON)  # Eligibility calculation results
    
    # Timing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    
    # Relationships
    questions = db.relationship('Question', backref='assessment', lazy=True, cascade='all, delete-orphan')
    results = db.relationship('AssessmentResult', backref='assessment', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'required_skills': self.required_skills,
            'threshold_percentage': self.threshold_percentage,
            'recruiter_id': self.recruiter_id,
            'candidate_id': self.candidate_id,
            'status': self.status,
            'resume_filename': self.resume_filename,
            'skill_matches': self.skill_matches,
            'eligibility_data': self.eligibility_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='text')  # text, multiple_choice, code
    options = db.Column(db.JSON)  # For multiple choice questions
    correct_answer = db.Column(db.Text)  # For auto-grading
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    order_index = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    answers = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'skill': self.skill,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'options': self.options,
            'difficulty': self.difficulty,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat()
        }

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    
    # AI Grading Results
    ai_score = db.Column(db.Float)  # Score from 0-10
    ai_feedback = db.Column(db.Text)
    
    # Timing
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent_seconds = db.Column(db.Integer)  # Time spent on this question
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'assessment_id': self.assessment_id,
            'answer_text': self.answer_text,
            'ai_score': self.ai_score,
            'ai_feedback': self.ai_feedback,
            'answered_at': self.answered_at.isoformat(),
            'time_spent_seconds': self.time_spent_seconds
        }

class AssessmentResult(db.Model):
    __tablename__ = 'assessment_results'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    
    # Overall Results
    overall_score = db.Column(db.Float, nullable=False)  # Average score across all skills
    skill_scores = db.Column(db.JSON, nullable=False)  # {skill: score} mapping
    total_questions = db.Column(db.Integer, nullable=False)
    total_time_seconds = db.Column(db.Integer)
    
    # Detailed Analysis
    strengths = db.Column(db.JSON)  # List of strong skills
    weaknesses = db.Column(db.JSON)  # List of weak skills
    recommendations = db.Column(db.Text)  # AI-generated recommendations
    
    # Status
    is_passed = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'overall_score': self.overall_score,
            'skill_scores': self.skill_scores,
            'total_questions': self.total_questions,
            'total_time_seconds': self.total_time_seconds,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'recommendations': self.recommendations,
            'is_passed': self.is_passed,
            'created_at': self.created_at.isoformat()
        }