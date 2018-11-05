from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "ssdf234223ljwe"
"""
class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False
"""
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


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

        new_post = Blog(blog_title, blog_body)
        db.session.add(new_post)
        db.session.commit()
        blog_id=new_post.id
        return redirect("/blog?id="+str(blog_id))
        #return render_template("index.html", page_title="Build a Blog", posts=posts)
    
    return render_template("newpost.html", page_title="Add a blog entry")

"""@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)
"""

"""
@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')
"""

if __name__ == '__main__':
    app.run()