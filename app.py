# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from models import db, User
from utils.email import mail, send_verification_email
import os

app = Flask(__name__)
# Existing configurations...

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Or your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize extensions
db.init_app(app)
mail.init_app(app)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # ... existing validation code ...

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, password=hashed_password)
            new_user.generate_verification_token()
            
            db.session.add(new_user)
            db.session.commit()
            
            # Send verification email
            send_verification_email(new_user)
            
            flash('Account created successfully! Please check your email to verify your account.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error during signup: {str(e)}")
            flash('An error occurred during signup. Please try again.', 'error')
            
    return render_template('signup.html')

@app.route('/verify-email/<token>')
def verify_email(token):
    try:
        user = User.query.filter_by(verification_token=token).first()
        
        if not user:
            flash('Invalid verification link.', 'error')
            return redirect(url_for('login'))
            
        if user.token_expiry < datetime.utcnow():
            flash('Verification link has expired. Please request a new one.', 'error')
            return redirect(url_for('login'))
            
        user.is_verified = True
        user.verification_token = None
        user.token_expiry = None
        db.session.commit()
        
        flash('Email verified successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
        
    except Exception as e:
        print(f"Error during email verification: {str(e)}")
        flash('An error occurred during verification. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                if not user.is_verified:
                    flash('Please verify your email before logging in.', 'error')
                    return render_template('login.html')
                    
                session['user_id'] = user.id
                session['email'] = user.email
                user.last_login = datetime.utcnow()
                db.session.commit()
                return redirect(url_for('index'))
            
            flash('Invalid email or password', 'error')
            
        except Exception as e:
            print(f"Error during login: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
            
    return render_template('login.html')