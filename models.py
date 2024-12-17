# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import secrets  # For generating verification tokens

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
    
    def generate_verification_token(self):
        self.verification_token = secrets.token_urlsafe(32)
        # Token expires in 24 hours
        self.token_expiry = datetime.utcnow() + timedelta(hours=24)