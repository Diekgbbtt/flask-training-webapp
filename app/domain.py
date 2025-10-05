# backend domain logic : middleware for integration with external apps, db

from app import db, app
from model import User, Thought, Vote, BASE_USER, OTHER, Role
from flask_user import UserManager


class Domain:

    @staticmethod
    def initialise_domain():
        with app.app_context():
            db.create_all()
            roles = Role.query.all()
            if len(roles) == 0:
                db.session.add(Role(name=BASE_USER))
                db.session.add(Role(name=OTHER))
                db.session.commit()
        user_manager = UserManager(app, db, User)

    @staticmethod
    def create_user(username, password):
        try:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return True, user
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_user_by_username(username):
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                return True, user
            return False, "User not found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = User.query.get(user_id)
            if user:
                return True, user
            return False, "User not found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def update_user(user_id, updates):
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            for key, value in updates.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
            return True, user
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            db.session.delete(user)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def create_thought_userid(content, user_id):
        try:
            thought = Thought(content=content, person_id=user_id)
            db.session.add(thought)
            db.session.commit()
            return True, thought
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    @staticmethod
    def create_thought_username(content, username):
        try:
            s, rs = Domain.get_user_by_username(username)
            if not s:
                return False, rs
            s, rs = Domain.create_thought_userid(content, rs.id)
            if not s:
                return False, rs
            return True, rs
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_all_thoughts():
        try:
            thoughts = Thought.query.all()
            return True, thoughts
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_thoughts_by_user(person_id):
        try:
            thoughts = Thought.query.filter_by(person_id=person_id).all()
            return True, thoughts
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_thought_by_id(thought_id):
        try:
            thought = Thought.query.get(thought_id)
            if thought:
                return True, thought
            return False, "Thought not found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def update_thought(thought_id, content):
        try:
            thought = Thought.query.get(thought_id)
            if not thought:
                return False, "Thought not found"
            thought.content = content
            db.session.commit()
            return True, thought
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_thought(thought_id):
        try:
            thought = Thought.query.get(thought_id)
            if not thought:
                return False, "Thought not found"
            db.session.delete(thought)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def create_vote_userid(person_id, thought_id):
        try:
            vote = Vote(person_id=person_id, thought_id=thought_id)
            db.session.add(vote)
            db.session.commit()
            return True, vote
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def create_vote_username(thought_id, username):
        try:
            user = Domain.get_user_by_username(username)
            Domain.create_vote_userid(person_id=user.id, thought_id=thought_id)
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_votes_by_thought(thought_id):
        try:
            votes = Vote.query.filter_by(thought_id=thought_id).all()
            return True, votes
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_votes_by_user(person_id):
        try:
            votes = Vote.query.filter_by(person_id=person_id).all()
            return True, votes
        except Exception as e:
            return False, str(e)

    @staticmethod
    def delete_vote(person_id, thought_id):
        try:
            vote = Vote.query.filter_by(person_id=person_id, thought_id=thought_id).first()
            if not vote:
                return False, "Vote not found"
            db.session.delete(vote)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    # Alias for existing placeholder
    @staticmethod
    def get_all_user_thoughts(person_id):
        return Domain.get_thoughts_by_user(person_id)

    
    @staticmethod
    def get_role_by_name(role_name):
        try:
            role = Role.query.filter_by(name=role_name).first()
            if role:
                return True, role
            return False, "Role not found"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def add_role_to_user(user : User, role : Role):
        try:
            user.roles.append(role)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    
    @staticmethod
    def check_role(user : User, role : [BASE_USER, OTHER]):
        return user.roles == role

    
