from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from openai import OpenAI


app = Flask(__name__)
app.secret_key = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
client = OpenAI(
api_key = "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"
)
# Read the content of the "system_card.txt" file
with open("system_card.txt", "r") as file:
    system = file.read()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            flash('Signup failed')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

# Define the route for generating a response using the OpenAI API
# The route accepts POST requests
@app.route("/generate", methods=["POST"])
def generate():
    # Get the data from the incoming request in JSON format
    data = request.get_json()
    # Extract the user message and conversation history from the request data
    user_message = data["message"]
    history = data["history"]

    # Create a list of message dictionaries for the OpenAI API
    messages = [{"role": "system", "content": system}]
    # Append the system message from the "system_card.txt" file
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Call the OpenAI API to generate a response using the gpt-4 
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=2000,
        n=1,
        temperature=0,
    )
    # Extract the generated AI message from the response
    ai_message = response.choices[0].message.content
   
    # Return the AI message as a JSON response
    return jsonify(ai_message)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
