# init_db.py
from app import app
from models import init_db

if __name__ == "__main__":
    init_db(app)