from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from openai import OpenAI
import re

app = Flask(__name__)
app.secret_key = 'password'  # In production, use a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
client = OpenAI(
    api_key = ""  # Add your OpenAI API key here
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<User {self.email}>'

# Email validation function
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Read the content of the "system_card.txt" file
try:
    with open("system_card.txt", "r") as file:
        system = file.read()
except FileNotFoundError:
    system = "You are a helpful AI assistant."
    print("Warning: system_card.txt not found. Using default system message.")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Validate email format
            if not is_valid_email(email):
                flash('Please enter a valid email address')
                return render_template('signup.html')

            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match')
                return render_template('signup.html')

            # Check if email already exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered')
                return render_template('signup.html')

            # Validate password length
            if len(password) < 6:
                flash('Password must be at least 6 characters long')
                return render_template('signup.html')

            # Create new user
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

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
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

# Create database tables
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)