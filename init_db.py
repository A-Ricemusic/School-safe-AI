# init_db.py
from flask import Flask
from models import db
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ensure instance folder exists
    if not os.path.exists('instance'):
        os.makedirs('instance')

    db.init_app(app)
    return app

def init_database():
    try:
        app = create_app()
        with app.app_context():
            # Import all models here to ensure they're registered
            from models import User
            
            print("Dropping all tables...")
            db.drop_all()
            print("Creating all tables...")
            db.create_all()
            
            # Verify tables were created
            tables = db.engine.table_names()
            if 'users' in tables:
                print(f"Database initialized successfully! Tables created: {tables}")
            else:
                raise Exception("Users table was not created properly")
                
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    init_database()