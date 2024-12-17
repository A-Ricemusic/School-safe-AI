# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @staticmethod
    def is_valid_email(email):
        if not email or len(email) > 120:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        if not password:
            return False
        # Check minimum length
        if len(password) < 6:
            return False
        # Check for at least one number
        if not any(char.isdigit() for char in password):
            return False
        # Check for at least one letter
        if not any(char.isalpha() for char in password):
            return False
        return True
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

def init_db(app):
    """Initialize the database with all tables."""
    with app.app_context():
        try:
            # Import all models here
            import models
            
            # Drop all existing tables and create new ones
            db.drop_all()
            db.create_all()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise

def create_tables(app):
    """Create tables if they don't exist without dropping existing ones."""
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            raise