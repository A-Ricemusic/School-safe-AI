# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from openai import OpenAI
from models import db, User
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'password')  # Better to use environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Ensure the instance folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

# Initialize OpenAI client
client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY', '')
)

# Read system card
try:
    with open("system_card.txt", "r") as file:
        system = file.read()
except FileNotFoundError:
    system = "You are a helpful AI assistant."
    print("Warning: system_card.txt not found. Using default system message.")

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Validate email format
            if not User.is_valid_email(email):
                flash('Please enter a valid email address')
                return render_template('signup.html')

            # Validate password
            if not User.validate_password(password):
                flash('Password must be at least 6 characters long')
                return render_template('signup.html')

            if password != confirm_password:
                flash('Passwords do not match')
                return render_template('signup.html')

            if User.query.filter_by(email=email).first():
                flash('Email already registered')
                return render_template('signup.html')

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please login.')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error during signup: {str(e)}")
            flash('An error occurred during signup. Please try again.')
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['email'] = user.email
                
                # Update last login time
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                return redirect(url_for('index'))
            
            flash('Invalid email or password')
            
        except Exception as e:
            print(f"Error during login: {str(e)}")
            flash('An error occurred. Please try again.')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/generate", methods=["POST"])
def generate():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        data = request.get_json()
        user_message = data["message"]
        history = data["history"]

        messages = [{"role": "system", "content": system}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2000,
            n=1,
            temperature=0,
        )
        
        ai_message = response.choices[0].message.content
        return jsonify(ai_message)
        
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return jsonify({'error': 'Failed to generate response'}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created if they didn't exist!")
    app.run(debug=True)