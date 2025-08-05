from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    ma.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

def reset_db():
    """Reset database - drop and recreate all tables"""
    db.drop_all()
    db.create_all()
    print("Database reset successfully!")
