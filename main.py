from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:swiss@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# app.secret_key = 'y2k'             

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(265))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body




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
            # cheese = "/blog?id=" + str(new_blog.id)
            # return redirect(cheese)
            
        else:
            return render_template('newpost.html', 
        title="Add Blog Entry", title_error=title_error, 
        body_error=body_error)



@app.route('/blog', methods=['GET'])
def blog():
    if request.args:
        blog_id = request.args("id")
        blog = Blog.query.get(blog_id)
        return render_template('blogs.html', blog=blog)
    else:
        blogs = Blog.query.all()
        return render_template('blogs.html', title="Build a Blog", blogs=blogs)
        
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        cheese = "/blog?id=" + str(new_blog.id)
        return redirect(cheese)

if __name__ == '__main__':
    app.run()