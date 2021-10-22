from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from functools import wraps

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQL("sqlite:///falcon.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    posts = db.execute("SELECT * FROM posts ORDER BY id DESC")

    return render_template("index.html", posts=posts)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return "<strong>Username Required!</strong>"
        
        password = request.form.get("password")
        if not password:
            return "<strong>Password Required!</strong>"
        
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return "<strong>Password Required!</strong>"

        if password != confirmation:
            return "<strong>Passwords must match!</strong>"

        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password)
            return redirect('/')
        except:
            return "<strong>Username already Registered!</strong>"

    else:
        return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return "<strong>Username Required!</strong>", 403
        password = request.form.get("password")
        if not password:
            return "<strong>Password Required!</strong>", 403
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or (rows[0]['password'] != password):
            return "<strong>Invalid Username or Password!</strong>"

        session["user_id"] = rows[0]["id"]

        return redirect("/")
        

    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/posts')
@login_required
def posts():
    user_id = session["user_id"]
    posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY id DESC", user_id)

    return render_template("posts.html", posts=posts)

@app.route('/add', methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        user_id = session["user_id"]
        name = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]

        title = request.form.get("title")
        if not title:
            return "<strong>Title Required!</strong>"
        
        text = request.form.get("text")
        if not text:
            return "<strong>Enter some text to post!</strong>"
        
        try:
            db.execute("INSERT INTO posts (user_id, name, title, text) VALUES (?, ?, ?, ?)", user_id, name, title, text)
            return redirect('/posts')
        except:
            return "<strong>Unable to post!</strong>"
    
    else:
        return render_template("add.html")

@app.route('/delete', methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        id = request.form.get("id")
        if not id:
            return "<strong>Id Required!</strong>"
        
        user_id = session["user_id"]
        user_id_post = db.execute("SELECT user_id FROM posts WHERE id = ?", id)
        if not user_id_post:
            return "<strong>Enter a valid Id!</strong>"
        
        a = int(user_id)
        b = int(user_id_post[0]["user_id"])


        if a == b:
            db.execute("DELETE FROM posts WHERE id = ?", id)
            return redirect("/")
        else:
            return "<strong>You cannot delete a Post!</strong>"

    else:
        return render_template("delete.html")
