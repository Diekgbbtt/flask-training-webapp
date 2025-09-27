import sqlite3
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator
from cryptography.fernet import Fernet

# Create a base db instance for model definitions
db = SQLAlchemy()

ENCRYPTION_KEY = Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)

class Password(TypeDecorator):
    """Custom type for encrypting passwords"""
    impl = db.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return fernet.encrypt(value.encode()).decode()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return fernet.decrypt(value.encode()).decode()
        return value

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(Password(300), nullable=False)

    def __init__(self, username=None, password=None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def check_user_existence(usr, pwd=None):
        """Check if user exists, optionally with password"""
        if pwd is None:
            return User.query.filter_by(username=usr).count() == 1
        return User.query.filter_by(username=usr, password=pwd).count() == 1

    @staticmethod
    def add_user(user_data):
        """Add a new user to the database"""
        try:
            user = User(username=user_data['username'], password=user_data['password'])
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error adding user: {e}")
            return False
