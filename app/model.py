
from enum import Enum, auto
from app import db
from flask_user import UserMixin
# from sqlalchemy.types import TypeDecorator
# from cryptography.fernet import Fernet

# Create a base db instance for model definitions

# ENCRYPTION_KEY = Fernet.generate_key()
# fernet = Fernet(ENCRYPTION_KEY)

# class Password(TypeDecorator):
#     """Custom type for encrypting passwords"""
#     impl = db.String

#     def process_bind_param(self, value, dialect):
#         if value is not None:
#             return fernet.encrypt(value.encode()).decode()
#         return value

#     def process_result_value(self, value, dialect):
#         if value is not None:
#             return fernet.decrypt(value.encode()).decode()
#         return value


BASE_USER = "baseuser"
OTHER = "other"

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50, collation ='NOCASE'), unique=True, nullable=False, index=True) # TODO add lowercase and stripping
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    created = db.relationship('Thought', backref='createdBy')
    voted = db.relationship('Thought', backref='voter')
    roles = db.relationship('Role', secondary='userroles')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)

class UserRoles(db.Model):
    __tablename__ = 'userroles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

class Thought(db.Model):

    __tablename__ = 'thoughts'
    
    id = db.Column(db.Integer , primary_key=True)
    content = db.Column(db.String (500), nullable=False, index=True)
    person_id = db.Column(db.Integer , db.ForeignKey('users.id'), index=True)
    votedBy = db.relationship('Vote', backref='votee')

class Vote(db.Model):
    
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer , primary_key =True)
    person_id = db.Column(db.Integer , db.ForeignKey('users.id'))
    thought_id = db.Column(db.Integer , db.ForeignKey('thoughts.id'))


    # @staticmethod
    # def check_user_existence(usr, pwd=None):
    #     """Check if user exists, optionally with password"""
    #     if pwd is None:
    #         return User.query.filter_by(username=usr).count() == 1
    #     return User.query.filter_by(username=usr, password=pwd).count() == 1

    # @staticmethod
    # def add_user(user_data):
    #     """Add a new user to the database"""
    #     try:
    #         user = User(username=user_data['username'], password=user_data['password'])
    #         db.session.add(user)
    #         db.session.commit()
    #         return True
    #     except Exception as e:
    #         db.session.rollback()
    #         print(f"Error adding user: {e}")
    #         return False
