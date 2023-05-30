from . import db
from flask_login import UserMixin


class BlogPost(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("Comment", backref="post")


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    secured_password = db.Column(db.String(100), nullable=False)

    posts = db.relationship("BlogPost", backref="author")
    comments = db.relationship("Comment", backref="author")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
