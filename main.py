from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "ssdf234223ljwe2"


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(60))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

#TODO FINISH THIS, ONLY COPIED IT
@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route("/blog")
def index():
    
    blog_id = request.args.get("id")
    
    if blog_id != None:
        blog_item = Blog.query.filter_by(id=blog_id).first()
        return render_template("entry.html", page_title=blog_item.title, title=blog_item.title, body=blog_item.body)

    posts = Blog.query.all()
    return render_template("index.html", page_title="Build a blog", posts=posts)

@app.route("/newpost", methods=['GET', 'POST'])
def create_new():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        if blog_title == "" or blog_body == "":
            flash("Please fill in both Title and Post fields", "error")
            return render_template('newpost.html', page_title="Add a blog entry", title=blog_title, body=blog_body)
        #TODO ADD OWNER PARAMETER TO NEW POST CONSTRUCTOR BELOW
        new_post = Blog(blog_title, blog_body)
        db.session.add(new_post)
        db.session.commit()
        blog_id=new_post.id
        return redirect("/blog?id="+str(blog_id))
        #return render_template("index.html", page_title="Build a Blog", posts=posts)
    
    return render_template("newpost.html", page_title="Add a blog entry")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['id'] = user.id
            flash("Logged in")
            return redirect('/newpost')
        elif not user:
            flash('That username does not exist, please retry or visit the signup page', 'error')
            return redirect('/login')
        elif user.password != password:
            flash('Incorrect password')
            return redirect('/login', username=username)

    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #returns welcome screen or shows any error messages
        
        username = request.form["username"]
        password = request.form["password"]
        password_retype = request.form["retype"]

        duplicate = User.query.filter_by(username=username).first()
    
        #run through potential errors
        if duplicate:
            error_name = 'That username already exists, please enter a new one'
            return render_template('signup.html', error_name=error_name)

        if username.strip() == "":
            error_name = "Please enter a Username"
            return render_template("signup.html", error_name=error_name)
    
        if len(username) < 3:
            error_name = "Please enter a Username with at least 3 characters"
            return render_template("signup.html", error_name=error_name)

        if password.strip() == "":
            error_name = "Please enter a Password"
            return render_template("signup.html", error_name=error_name, username=username)

        if password_retype.strip() == "":
            error_name = "Please retype your password"
            return render_template("signup.html", error_name=error_name, username=username)

        if password != password_retype:
            error_name = "Original password and retype do not match, please retype passwords"
            return render_template("signup.html", error_name=error_name, username=username)
        
        if len(password) < 3:
            error_name = "Please enter a password with a length of at least 3 characters"
            return render_template("signup.html", error_name=error_name, username=username)
        
        

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        return redirect('/newpost')

    
    return render_template("signup.html")


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


if __name__ == '__main__':
    app.run()