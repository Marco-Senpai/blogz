from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:swiss@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y2k'             


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(265))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
       


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', '/']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged In")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or User does not exist', 'error')

    return render_template('blogs.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else: 
            return "<h1>Duplicate User<h1>"

    return render_template('newpost.html')

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/')


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        return render_template('newpost.html', 
        title="Add Blog Entry")
    if request.method == 'POST':    
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        title_error = ''
        body_error = ''
        if len(blog_title) < 1:
            title_error = "please add an entry"
        if len(blog_body) < 1:
            body_error = "please add a body"
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            cheese = "/blog?id=" + str(new_blog.id)
            return redirect(cheese)
        else:
            return render_template('newpost.html', 
            title="Add Blog Entry", title_error=title_error, 
            body_error=body_error)



@app.route('/blog', methods=['GET'])
def blog():
    if request.args.get("id"):
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)
        return render_template('display.html', blog=blog)
    elif request.args.get("user"):
        user_id = request.args.get("user")
        user = User.query.get(user_id)
        blogs = Blog.query.filter_by(owner=user)
        return render_template('singleUser.html', blogs=blogs)
    else:
        blogs = Blog.query.all()
        return render_template('blogs.html', title="Blogz", blogs=blogs)
        

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', title="Blogz", users=users)


# @app.route('/delete-blog', methods=['blog_id'])
# def delete_blog():

#     blog_id = int(request.form['blog_id'])
#     blog = Blog.query.get(blog_id)
#     db.session.add(blog)
#     db.session.commit()
#     cheese = "/blog?id=" + str(new_blog.id)
#     return redirect(cheese)


if __name__ == '__main__':
    app.run()