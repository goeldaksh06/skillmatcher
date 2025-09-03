from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Assessment, User, AssessmentResult
from app.services.assessment_service import AssessmentService

recruiter_bp = Blueprint('recruiter', __name__)
assessment_service = AssessmentService()

@recruiter_bp.route('/assessments', methods=['POST'])
@jwt_required()
def create_assessment():
    """Create a new assessment (recruiters only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.role != 'recruiter':
            return jsonify({'error': 'Only recruiters can create assessments'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title') or not data.get('required_skills'):
            return jsonify({'error': 'Title and required_skills are required'}), 400
        
        assessment = assessment_service.create_assessment(
            recruiter_id=user_id,
            title=data['title'],
            required_skills=data['required_skills'],
            threshold_percentage=data.get('threshold_percentage', 70),
            description=data.get('description')
        )
        
        return jsonify({
            'message': 'Assessment created successfully',
            'assessment': assessment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recruiter_bp.route('/assessments', methods=['GET'])
@jwt_required()
def get_assessments():
    """Get all assessments created by the recruiter"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.role != 'recruiter':
            return jsonify({'error': 'Only recruiters can view assessments'}), 403
        
        assessments = Assessment.query.filter_by(recruiter_id=user_id).all()
        
        return jsonify({
            'assessments': [assessment.to_dict() for assessment in assessments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recruiter_bp.route('/assessments/<int:assessment_id>', methods=['GET'])
@jwt_required()
def get_assessment_details():
    """Get detailed assessment information including results"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.role != 'recruiter':
            return jsonify({'error': 'Only recruiters can view assessment details'}), 403
        
        assessment = Assessment.query.filter_by(id=assessment_id, recruiter_id=user_id).first()
        if not assessment:
            return jsonify({'error': 'Assessment not found'}), 404
        
        # Get assessment result if completed
        result = AssessmentResult.query.filter_by(assessment_id=assessment_id).first()
        
        response_data = {
            'assessment': assessment.to_dict(),
            'result': result.to_dict() if result else None
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recruiter_bp.route('/assessments/<int:assessment_id>/candidates', methods=['GET'])
@jwt_required()
def get_assessment_candidates():
    """Get all candidates who have taken this assessment"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.role != 'recruiter':
            return jsonify({'error': 'Only recruiters can view candidates'}), 403
        
        assessment = Assessment.query.filter_by(id=assessment_id, recruiter_id=user_id).first()
        if not assessment:
            return jsonify({'error': 'Assessment not found'}), 404
        
        # Get all results for this assessment
        results = db.session.query(AssessmentResult, User).join(
            Assessment, AssessmentResult.assessment_id == Assessment.id
        ).join(
            User, Assessment.candidate_id == User.id
        ).filter(Assessment.id == assessment_id).all()
        
        candidates_data = []
        for result, candidate in results:
            candidates_data.append({
                'candidate': candidate.to_dict(),
                'result': result.to_dict()
            })
        
        return jsonify({
            'assessment': assessment.to_dict(),
            'candidates': candidates_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
