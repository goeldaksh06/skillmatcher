from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Assessment, Question, Answer, User
from app.services.assessment_service import AssessmentService
from app.services.file_service import FileService

assessment_bp = Blueprint('assessment', __name__)
assessment_service = AssessmentService()
file_service = FileService()

@assessment_bp.route('/start/<int:assessment_id>', methods=['POST'])
@jwt_required()
def start_assessment():
    """Start an assessment by uploading resume and checking eligibility"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        assessment = Assessment.query.get_or_404(assessment_id)
        
        # Check if assessment is available
        if assessment.status != 'draft':
            return jsonify({'error': 'Assessment is not available'}), 400
        
        # Handle file upload or text input
        resume_text = ""
        filename = None
        
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            if file and file.filename:
                success, message, file_path = file_service.save_uploaded_file(
                    file, current_app.config['UPLOAD_FOLDER']
                )
                
                if not success:
                    return jsonify({'error': message}), 400
                
                # Parse the uploaded file
                parse_success, resume_text = file_service.parse_resume_file(file_path)
                if not parse_success:
                    return jsonify({'error': resume_text}), 400
                
                filename = file.filename
        else:
            # Text input
            data = request.get_json()
            resume_text = data.get('resume_text', '')
        
        if not resume_text.strip():
            return jsonify({'error': 'Resume text or file is required'}), 400
        
        # Check eligibility
        eligible, eligibility_data = assessment_service.upload_resume_and_check_eligibility(
            assessment_id, resume_text, filename
        )
        
        if not eligible:
            return jsonify({
                'eligible': False,
                'eligibility_data': eligibility_data,
                'message': 'You do not meet the minimum skill requirements for this assessment'
            }), 200
        
        # Assign candidate to assessment
        assessment.candidate_id = user_id
        assessment.started_at = db.func.now()
        db.session.commit()
        
        # Generate questions
        questions = assessment_service.generate_assessment_questions(assessment_id)
        
        return jsonify({
            'eligible': True,
            'eligibility_data': eligibility_data,
            'message': 'Assessment started successfully',
            'assessment': assessment.to_dict(),
            'total_questions': len(questions)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@assessment_bp.route('/progress/<int:assessment_id>', methods=['GET'])
@jwt_required()
def get_progress():
    """Get current assessment progress"""
    try:
        user_id = get_jwt_identity()
        
        assessment = Assessment.query.get_or_404(assessment_id)
        
        # Verify user has access to this assessment
        if assessment.candidate_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        progress = assessment_service.get_assessment_progress(assessment_id)
        
        return jsonify(progress), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assessment_bp.route('/question/<int:question_id>/answer', methods=['POST'])
@jwt_required()
def submit_answer():
    """Submit an answer to a question"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('answer_text'):
            return jsonify({'error': 'Answer text is required'}), 400
        
        question = Question.query.get_or_404(question_id)
        assessment = Assessment.query.get_or_404(question.assessment_id)
        
        # Verify user has access to this assessment
        if assessment.candidate_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Check if already answered
        existing_answer = Answer.query.filter_by(
            question_id=question_id, 
            assessment_id=question.assessment_id
        ).first()
        
        if existing_answer:
            return jsonify({'error': 'Question already answered'}), 400
        
        # Submit and grade answer
        answer = assessment_service.submit_answer(
            question_id, 
            data['answer_text'], 
            data.get('time_spent_seconds')
        )
        
        return jsonify({
            'message': 'Answer submitted successfully',
            'answer': answer.to_dict(),
            'score': answer.ai_score,
            'feedback': answer.ai_feedback
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@assessment_bp.route('/complete/<int:assessment_id>', methods=['POST'])
@jwt_required()
def complete_assessment():
    """Complete the assessment and generate final results"""
    try:
        user_id = get_jwt_identity()
        
        assessment = Assessment.query.get_or_404(assessment_id)
        
        # Verify user has access to this assessment
        if assessment.candidate_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Check if all questions are answered
        total_questions = Question.query.filter_by(assessment_id=assessment_id).count()
        answered_questions = Answer.query.filter_by(assessment_id=assessment_id).count()
        
        if answered_questions < total_questions:
            return jsonify({
                'error': f'Please answer all questions. {answered_questions}/{total_questions} completed'
            }), 400
        
        # Generate final results
        result = assessment_service.complete_assessment(assessment_id)
        
        return jsonify({
            'message': 'Assessment completed successfully',
            'result': result.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@assessment_bp.route('/public/<int:assessment_id>', methods=['GET'])
def get_public_assessment():
    """Get public assessment information (for candidates to view before starting)"""
    try:
        assessment = Assessment.query.get_or_404(assessment_id)
        
        # Only show public information
        public_data = {
            'id': assessment.id,
            'title': assessment.title,
            'description': assessment.description,
            'required_skills': assessment.required_skills,
            'threshold_percentage': assessment.threshold_percentage,
            'status': assessment.status
        }
        
        return jsonify({
            'assessment': public_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
