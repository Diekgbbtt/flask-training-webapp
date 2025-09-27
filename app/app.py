import secrets
from flask import Flask, redirect, render_template, session, request, url_for
from utilities.util import is_client_authn, validate_user_data
from model.orm import db, User

app = Flask(__name__)

# Generate a strong, cryptographically secure secret key for session cookies
app.secret_key = secrets.token_urlsafe(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app/test.db'

# Initialize the database with the app
db.init_app(app)

# TODO - verify dicrepancies between persistent layer and classes modelling structurs
# with app.app_context():
#     db.create_all()


class Thought:
    ids = 0
    def __init__(self,content) -> None:
        self._id = Thought.ids
        Thought.ids = Thought.ids+1
        self._createdBy = None
        self._votedBy = []
    
    @property
    def id(self):
        return self._id

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self,c):
        self._content = c

    @property
    def createdBy(self):
        return self._createdBy

    @createdBy.setter
    def createdBy(self,p):
        self._createdBy = p
        p._created.add(self)

    @createdBy.deleter
    def createdBy(self):
        if self._createdBy != None:
            self._createdBy._created.remove(self)
        del self._createdBy

    @property
    def votedBy(self):
        return self._votedBy

    def addvotedBy(self,p):
        self._votedBy.append(p)
        p._voted.append(self)

    def removevotedBy(self,p):
        self._votedBy.remove(p)
        p._voted.remove(self)



# Here we allow unauthenticated users to access the index page.
@app.route('/')
def index():
    return render_template('index.html')

@app.get('/login')
def login():
    # check if user already authenticated checking for cookie in request if so redict to index

    if is_client_authn():
        return render_template('index.html')

    # not authenticated, return auth html page with form
    return render_template('login.html')

@app.post('/login')
def post_login_details():

    # check if request present a valid session cookie, user already authenicated - return index
    if is_client_authn():
        return redirect(url_for('index'))

    # not authenticated, process form data - always verify the validity of the form before processing, check presence of username and password fields
    if not validate_user_data(request.form) :
        return render_template('login.html', invalid_input=True)
        
    # in the User DB table check for entry with the username passed throguh the form field 'username' with ORM module
    if not User.check_user_existence(usr=request.form.usernmame, pwd=request.form.password) :
        return render_template('login.html', wrong_credential=True)
    
    # set a session, return index page with cookies
    session['username'] = request.form.username
    return render_template('index.html')

    # if password is wrong, return render_template('login.html', wrong_credential=true)
    # if there is no User table entry with tha username return render_tempalte('login.html', wrong_credential=true)
    # if the request does not have required fields return rendere_template('login.hmtl', wrong_request=true)


@app.route('/logout', methods=['POST'])
def logout():
    if is_client_authn():
        session.clear()
    # here check for user existence in db should be addes
    return render_template('index.html')



@app.route('/register', methods=['POST'])
def register():
       # check if request present a valid session cookie, user already authenicated - return index
    if is_client_authn():
        return redirect(url_for(('index')))

    # not authenticated, process form data - always verify the validity of the form before processing, check presence of username and password fields
    if not validate_user_data(request.form) :
        return render_template('login.html', invalid_input=True)
        
    # in the User DB table check for entry with the username passed throguh the form field 'username' with ORM module
    if not User.check_user_existence(usr=request.form.usernmame, pwd=request.form.password) :
        return render_template('login.html', wrong_username=True)

    # add user to db table and create session
    User.add_user(request.form)
    session['username'] = request.form.username
    return redirect(url_for('index'))

@app.route('/add_thought', methods=['POST'])
def add_thought():
    pass

@app.route('/delete_thought')
def delete_thought():
    pass

@app.route('/vote_thought')
def vote_thought():
    pass
