# backend domain logic : middleware for integration with external apps, self.db

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from model import User, Thought, Vote, BASE_USER, OTHER, Role
from flask_user import UserManager
from cedar.authz import SecurityException, EntitySerializer, CedarClient


POLICY_PATH = "./cedar/main.cedar"
SCHEMA_PATH = "./cedar/main.cedarschema"


class Domain:

    def __init__(self, app=None, db=None):
        if db:
            self.db = db
        self.initialise_domain(app=app)
        self.initialise_cedar()

    
    def initialise_domain(self, app):
        if app and self.db:
            with app.app_context():
                self.db.create_all()
                roles = Role.query.all()
                if len(roles) == 0:
                    self.db.session.add(Role(name=BASE_USER))
                    self.db.session.add(Role(name=OTHER))
                    self.db.session.commit()
            self.user_manager = UserManager(app, self.db, User)

    
    def initialise_cedar(self):
        serializer = EntitySerializer()
        with open(POLICY_PATH, "r", encoding="utf-8") as policy_file:
            policies = policy_file.read()
            try:
                with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
                    schema = schema_file.read()
                    self.cedar = CedarClient(policies, serializer, schema, verbose = True)
            except FileNotFoundError:
                schema = None
    
    
    
    def create_user(self, username, password):
        try:
            user = User(username=username, password=password)
            self.db.session.add(user)
            self.db.session.commit()
            return True, user
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)

    
    def get_user_by_username(self, username):
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                return True, user
            return False, "User not found"
        except Exception as e:
            return False, str(e)

    
    def get_user_by_id(self, user_id):
        try:
            user = User.query.get(user_id)
            if user:
                return True, user
            return False, "User not found"
        except Exception as e:
            return False, str(e)

    
    def update_user(self, user_id, updates):
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            for key, value in updates.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.db.session.commit()
            return True, user
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)

    
    def delete_user(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            self.db.session.delete(user)
            self.db.session.commit()
            return True, ""
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)

    def create_thought_userid(self, content, user):
        try:
            thought = Thought(content=content, person=user.id)
            thought.createdBy = user
            if hasattr(self, 'cedar'):
                self.cedar.assert_allowed(principal=user, action="createThought", resource=Thought)
            if self.db:
                self.db.session.add(thought)
                self.db.session.commit()
            return True, thought
        except SecurityException as se:
            if self.db:
                self.db.session.rollback()
            raise se
        
    
    def create_thought_username(self, content, user):
        try:
            s, rs = Domain.get_user_by_username(user.username)
            if not s:
                return False, rs
            s, rs = Domain.create_thought_userid(content, user.id)
            if not s:
                return False, rs
            return True, rs
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)

    
    def get_all_thoughts():
        try:
            thoughts = Thought.query.all()
            return True, thoughts
        except Exception as e:
            return False, str(e)

    
    def get_thoughts_by_user(person_id):
        try:
            thoughts = Thought.query.filter_by(user=person_id).all()
            return True, thoughts
        except Exception as e:
            return False, str(e)

    
    def get_thought_by_id(self, thought_id):
        try:
            thought = Thought.query.get(thought_id)
            if thought:
                return True, thought
            return False, "Thought not found"
        except Exception as e:
            return False, str(e)

    
    def update_thought(self, thought_id, content):
        try:
            thought = Thought.query.get(thought_id)
            if not thought:
                return False, "Thought not found"
            thought.content = content
            self.db.session.commit()
            return True, thought
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)

    
    def delete_thought(self, thought_id):
        try:
            thought = Thought.query.get(thought_id)
            if not thought:
                return False, "Thought not found"
            self.db.session.delete(thought)
            self.db.session.commit()
            return True, ""
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)

    
    def create_vote_userid(self, person_id, thought_id):
        try:
            vote = Vote(user=person_id, thought=thought_id)
            self.db.session.add(vote)
            self.db.session.commit()
            return True, vote
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)
    
    
    def create_vote_username(self, thought_id, username):
        try:
            user = Domain.get_user_by_username(username)
            Domain.create_vote_userid(user=user.id, thought=thought_id)
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)

    
    def get_votes_by_thought(thought_id):
        try:
            votes = Vote.query.filter_by(thought=thought_id).all()
            return True, votes
        except Exception as e:
            return False, str(e)

    
    def get_votes_by_user(person_id):
        try:
            votes = Vote.query.filter_by(user=person_id).all()
            return True, votes
        except Exception as e:
            return False, str(e)

    
    def delete_vote(self, person_id, thought_id):
        try:
            vote = Vote.query.filter_by(user=person_id, thought=thought_id).first()
            if not vote:
                return False, "Vote not found"
            self.db.session.delete(vote)
            self.db.session.commit()
            return True, ""
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)

    # Alias for existing placeholder
    
    def get_all_user_thoughts(self, person_id):
        return self.get_thoughts_by_user(person_id)

    
    
    def get_role_by_name(role_name):
        try:
            role = Role.query.filter_by(name=role_name).first()
            if role:
                return True, role
            return False, "Role not found"
        except Exception as e:
            return False, str(e)

    
    def add_role_to_user(self, user : User, role : Role):
        try:
            user.roles.append(role)
            self.db.session.commit()
            return True, ""
        except Exception as e:
            self.db.session.rollback()
            return False, str(e)

    
    
    def check_role(user : User, role : [BASE_USER, OTHER]):
        return user.roles == role

    
