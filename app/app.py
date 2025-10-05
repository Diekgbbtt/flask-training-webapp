#  __init__ + routes
import secrets
import logging
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, current_user, roles_required, user_registered

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
app.config['USER_UNAUTHORIZED_ENDPOINT'] = 'error'

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)
# Import models after db is initialized
from domain import Domain, BASE_USER, OTHER
Domain.initialise_domain()


@app.route('/')
def index():
    s, rs = Domain.get_all_thoughts()
    if not s:
        return render_template('index.html', err=rs)
    return render_template('index.html', table=rs)

# Here we allow unauthenticated users to access the index page.
@app.get('/index')
def home_page():
    return render_template('home_page.html')

@app.get('/error')
def error():
    msg = request.args.get('msg') if hasattr(request.args, "msg") else "You are not authorized to access this page"
    return render_template('error.html', message=msg)

@user_registered.connect_via(app)
def _user_registers_assign_roles_hok(sender, user, **kwargs):
    s, rs = Domain.get_role_by_name(BASE_USER)
    if not s:
        return redirect(url_for('error'))
    s, rs = Domain.add_role_to_user(user, rs)
    if not s:
        return redirect(url_for('error'))

@app.get('/memberpage')
@login_required
def member_page():
    return render_template('member_page.html', username=current_user.username)

@app.route('/add_thought', methods=['POST'])
@login_required
@roles_required(BASE_USER)
def add_thought():
    # TODO verify form data schema
    cnt = request.form['thought']
    s, errmsg = Domain.create_thought_username(content=cnt, username=current_user.username)
    if not s:
        # TODO implement error handling
        return redirect(url_for('error'))
    return redirect(url_for('index'))


@app.route('/delete_thought')
@login_required
@roles_required(BASE_USER)
# TODO verify form data schema
def delete_thought():
    tid = request.args['id']
    s, errmsg = Domain.delete_thought(tid)
    if not s:
        return redirect(url_for('error'))
    redirect(url_for('index'))

@app.route('/vote_thought')
@login_required
@roles_required(BASE_USER)
# TODO sanitize id
def vote_thought():
    tid = request.args['id']
    s, errmsg = Domain.create_vote_username(thought_id=tid, username=current_user.username)
    if not s:
        return redirect(url_for('error'))
    redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
