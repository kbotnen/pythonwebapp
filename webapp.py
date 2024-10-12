from flask import Flask

from flask import request

from flask import render_template

from flask import redirect, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


with app.app_context(): db.create_all()


@app.get("/")
def index():
    post_list = db.session.query(Post).all()
    return render_template('index.html', post_list=post_list)


@app.post("/add")
def add():
    title = request.form.get("title")
    new_post = Post(title=title, complete=False)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for("index"))


@app.get("/update/<int:post_id>")
def update(post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first()
    post.complete = not post.complete
    db.session.commit()
    return redirect(url_for("index"))


@app.get("/delete/<int:post_id>")
def delete(post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("index"))


@app.get('/about')
def about():
    return 'The about page'

