from flask import Blueprint, request, jsonify
from sqlalchemy import or_, desc, asc
from db import db
from models.job import Job, job_schema, jobs_schema
from marshmallow import ValidationError
from datetime import datetime

# Create Blueprint
job_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@job_bp.route('', methods=['GET'])
def get_jobs():
    """Get all jobs with optional filtering and sorting"""
    try:
        # Start with base query
        query = Job.query
        
        # Apply filters
        job_type = request.args.get('job_type')
        location = request.args.get('location')
        tag = request.args.get('tag')
        search = request.args.get('search')
        
        if job_type:
            query = query.filter(Job.job_type == job_type)
        
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        
        if tag:
            query = query.filter(Job.tags.ilike(f'%{tag}%'))
        
        if search:
            query = query.filter(
                or_(
                    Job.title.ilike(f'%{search}%'),
                    Job.company.ilike(f'%{search}%'),
                    Job.description.ilike(f'%{search}%')
                )
            )
        
        # Apply sorting
        sort_by = request.args.get('sort', 'posting_date_desc')
        
        if sort_by == 'posting_date_desc':
            query = query.order_by(desc(Job.posting_date))
        elif sort_by == 'posting_date_asc':
            query = query.order_by(asc(Job.posting_date))
        elif sort_by == 'title_asc':
            query = query.order_by(asc(Job.title))
        elif sort_by == 'title_desc':
            query = query.order_by(desc(Job.title))
        elif sort_by == 'company_asc':
            query = query.order_by(asc(Job.company))
        elif sort_by == 'company_desc':
            query = query.order_by(desc(Job.company))
        
        # Execute query
        jobs = query.all()
        
        # Serialize and return
        result = jobs_schema.dump(jobs)
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching jobs: {str(e)}'
        }), 500

@job_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a single job by ID"""
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({
                'success': False,
                'message': 'Job not found'
            }), 404
        
        result = job_schema.dump(job)
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching job: {str(e)}'
        }), 500

@job_bp.route('', methods=['POST'])
def create_job():
    """Create a new job"""
    try:
        # Validate input data - this now returns a dictionary
        job_data = job_schema.load(request.json)

        # Create new job from dictionary
        new_job = Job(**job_data)
        db.session.add(new_job)
        db.session.commit()

        result = job_schema.dump(new_job)
        return jsonify({
            'success': True,
            'message': 'Job created successfully',
            'data': result
        }), 201

    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': 'Validation error',
            'errors': e.messages
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating job: {str(e)}'
        }), 500

@job_bp.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Update an existing job"""
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({
                'success': False,
                'message': 'Job not found'
            }), 404

        # Validate input data - this now returns a dictionary
        job_data = job_schema.load(request.json, partial=True)

        # Update job fields
        for key, value in job_data.items():
            if hasattr(job, key) and key not in ['id', 'created_at']:
                setattr(job, key, value)

        job.updated_at = datetime.utcnow()
        db.session.commit()

        result = job_schema.dump(job)
        return jsonify({
            'success': True,
            'message': 'Job updated successfully',
            'data': result
        }), 200

    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': 'Validation error',
            'errors': e.messages
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating job: {str(e)}'
        }), 500

@job_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job"""
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({
                'success': False,
                'message': 'Job not found'
            }), 404

        db.session.delete(job)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Job deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting job: {str(e)}'
        }), 500

@job_bp.route('/stats', methods=['GET'])
def get_job_stats():
    """Get job statistics"""
    try:
        total_jobs = Job.query.count()
        job_types = db.session.query(Job.job_type, db.func.count(Job.id)).group_by(Job.job_type).all()

        return jsonify({
            'success': True,
            'data': {
                'total_jobs': total_jobs,
                'job_types': dict(job_types)
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching stats: {str(e)}'
        }), 500
