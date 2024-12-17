# utils/email.py
from flask_mail import Mail, Message
from flask import current_app, url_for

mail = Mail()

def send_verification_email(user):
    verification_url = url_for(
        'verify_email',
        token=user.verification_token,
        _external=True
    )
    
    msg = Message(
        'Verify your School Safe AI account',
        sender='noreply@schoolsafeai.com',
        recipients=[user.email]
    )
    
    msg.body = f'''Please verify your email address by clicking the following link:
{verification_url}

This link will expire in 24 hours.

If you did not create an account, please ignore this email.
'''
    
    msg.html = f'''
    <h1>Welcome to School Safe AI!</h1>
    <p>Please verify your email address by clicking the following link:</p>
    <p><a href="{verification_url}">Verify Email Address</a></p>
    <p>This link will expire in 24 hours.</p>
    <p>If you did not create an account, please ignore this email.</p>
    '''
    
    mail.send(msg)