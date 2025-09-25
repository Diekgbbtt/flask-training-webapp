from flask import Flask, render_template

app = Flask(__name__)

class Person:
    def __init__(self,name,password) -> None:
        self._name = name
        self._password = password
        self._created = set()
        self._voted = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,n):
        self._name = n

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,p):
        self._password = p

    @property
    def created(self):
        return self._created

    def addcreated(self,t):
        self._created.add(t)
        t._createdBy = self

    def removecreated(self,t):
        self._created.remove(t)
        del t._createdBy

    @property
    def voted(self):
        return self._voted

    def addvoted(self,t):
        self._voted.append(t)
        t._votedBy.append(self)

    def removevoted(self,t):
        self._voted.remove(t)
        t._votedBy.remove(self)


class Thought:
    ids = 0
    def __init__(self,content) -> None:
        self._id = Thought.ids
        Thought.ids = Thought.ids+1
        self._content = content
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


persons = set()    
thoughts = []

# Here we allow unauthenticated users to access the index page.
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    pass    

@app.route('/register', methods=['POST'])
def register():
    pass

@app.route('/add_thought', methods=['POST'])
def add_thought():
    pass

@app.route('/delete_thought')
def delete_thought():
    pass

@app.route('/vote_thought')
def vote_thought():
    pass


