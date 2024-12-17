# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import re
import secrets

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100), unique=True)
    token_expiry = db.Column(db.DateTime)
    
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
        return True
    
    def generate_verification_token(self):
        self.verification_token = secrets.token_urlsafe(32)
        # Token expires in 24 hours
        self.token_expiry = datetime.utcnow() + timedelta(hours=24)