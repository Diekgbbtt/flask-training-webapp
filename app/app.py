#  __init__ + routes
import secrets
from flask import Flask, redirect, render_template, session, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, login_required, current_user
"""
Flask-User comes with pre-defined routes for registration (user.register),
login (user.login), and logout (user.logout).
"""

app = Flask(__name__)

# Generate a strong, cryptographically secure secret key for session cookies

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/instance/test.db'
app.config['USER_APP_NAME'] = "ThoughtSharing"
app.config['USER_ENABLE_EMAIL'] = False
app.config['USER_ENABLE_USERNAME'] = True
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
db = SQLAlchemy(app)

# Import models after db is initialized
from domain import Domain


with app.app_context() :
    db.create_all()

from model import User
user_manager = UserManager(app, db, User)


# Here we allow unauthenticated users to access the index page.
@app.route('/')
def index():
    s, rs = Domain.get_all_thoughts()
    if not s:
        return render_template('index.html', err=rs)
    return render_template('index.html', table=rs)


@app.get('/homepage')
def home_page():
    return render_template('home_page.html')

@app.get('/memberpage')
@login_required
def member_page():
    return render_template('member_page.html', username=current_user)

@app.route('/add_thought', methods=['POST'])
@login_required
def add_thought():
    # TODO verify form data schema

    cnt = request.form.content
    s, errmsg = Domain.create_thought_username(content=cnt, username=session['username'])
    if not s:
        # TODO implement error handling
        redirect(url_for('index'), err=errmsg)
    redirect(url_for('index'))


@app.route('/delete_thought')
@login_required
# TODO verify form data schema
def delete_thought():
    tid = request.args['id']
    s, errmsg = Domain.delete_thought(tid)
    if not s:
        redirect(url_for('index'), err=errmsg)
    redirect(url_for('index'))

@app.route('/vote_thought')
@login_required
# TODO sanitize id
def vote_thought():
    tid = request.args['id']
    s, errmsg = Domain.create_vote_username(thought_id=tid, username=session['username'])
    if not s:
        redirect(url_for('index'), err=errmsg)
    redirect(url_for('index'))
