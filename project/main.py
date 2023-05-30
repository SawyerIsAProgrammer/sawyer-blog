from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
# from flask_login import current_user

from .models import *
from .forms import *

main = Blueprint(name='main', import_name=__name__)


@main.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@main.route("/post/<int:index>", methods=['POST', 'GET'])
def show_post(index):
    form = CommentForm()
    requested_post = BlogPost.query.get_or_404(index)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data,
                              author_id=current_user.id,
                              blog_id=requested_post.id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash(message="You need to login first")
        return redirect(url_for("main.show_post", index=requested_post.id))
    return render_template("post.html", post=requested_post, form=form)


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/contact")
def contact():
    return render_template("contact.html")
