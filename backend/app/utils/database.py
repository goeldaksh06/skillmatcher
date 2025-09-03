from app import db
from app.models import User, Assessment

def init_db():
    """Initialize database tables"""
    db.create_all()
    print("Database tables created successfully!")

def create_sample_data():
    """Create sample data for testing"""
    # Create sample recruiter
    recruiter = User.query.filter_by(email='recruiter@example.com').first()
    if not recruiter:
        recruiter = User(
            email='recruiter@example.com',
            first_name='John',
            last_name='Recruiter',
            role='recruiter'
        )
        recruiter.set_password('password123')
        db.session.add(recruiter)
    
    # Create sample candidate
    candidate = User.query.filter_by(email='candidate@example.com').first()
    if not candidate:
        candidate = User(
            email='candidate@example.com',
            first_name='Jane',
            last_name='Developer',
            role='candidate'
        )
        candidate.set_password('password123')
        db.session.add(candidate)
    
    db.session.commit()
    
    # Create sample assessment
    sample_assessment = Assessment.query.filter_by(title='Python Developer Assessment').first()
    if not sample_assessment:
        sample_assessment = Assessment(
            title='Python Developer Assessment',
            description='Comprehensive assessment for Python developers',
            required_skills=['Python', 'SQL', 'Flask', 'REST API'],
            threshold_percentage=70,
            recruiter_id=recruiter.id,
            status='draft'
        )
        db.session.add(sample_assessment)
        db.session.commit()
    
    print("Sample data created successfully!")
    print(f"Recruiter: recruiter@example.com / password123")
    print(f"Candidate: candidate@example.com / password123")
    print(f"Sample Assessment ID: {sample_assessment.id}")