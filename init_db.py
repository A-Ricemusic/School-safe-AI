# init_db.py
from flask import Flask
from models import db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure instance folder exists
if not os.path.exists('instance'):
    os.makedirs('instance')

db.init_app(app)

def init_database():
    try:
        with app.app_context():
            # Drop all existing tables
            db.drop_all()
            # Create all tables
            db.create_all()
            print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    init_database()