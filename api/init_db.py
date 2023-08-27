from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from models import User, Phone
from app import app, db
from config import get_uri

with app.app_context():
    if not database_exists(get_uri()):
        create_database(get_uri())
    
    db.create_all()
