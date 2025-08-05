from datetime import datetime
from db import db, ma
from marshmallow import fields, validate

class Job(db.Model):
    """Job model for storing job listings"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    posting_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    job_type = db.Column(db.String(50), nullable=False, default='Full-time')
    tags = db.Column(db.Text)  # Comma-separated tags
    description = db.Column(db.Text)
    url = db.Column(db.String(500))  # Original job posting URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'
    
    def to_dict(self):
        """Convert job object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'posting_date': self.posting_date.isoformat() if self.posting_date else None,
            'job_type': self.job_type,
            'tags': self.tags.split(',') if self.tags else [],
            'description': self.description,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class JobSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for Job serialization"""
    class Meta:
        model = Job
        load_instance = False  # Return dictionaries, not model instances
        include_fk = True
    
    # Validation rules
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    company = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    location = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    job_type = fields.Str(validate=validate.OneOf(['Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary']))
    tags = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True, validate=validate.Length(max=500))

# Schema instances
job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
