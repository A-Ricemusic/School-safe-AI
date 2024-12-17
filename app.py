# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from openai import OpenAI
from models import db, User, init_db
import os

app = Flask(__name__)
app.secret_key = 'password'  # In production, use a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Ensure the instance folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

# ... (rest of your routes and code)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)