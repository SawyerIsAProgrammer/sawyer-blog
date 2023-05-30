from flask import Blueprint, redirect, url_for, render_template, request, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps
import datetime

from . import login_manager
from .forms import *
from .models import *


auth = Blueprint(name='auth', import_name=__name__)


def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if hasattr(current_user, "id") and current_user.id == 1:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(user_id)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash(message="The email already exists, sign in with it instead")
            return redirect(url_for('auth.login'))
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            secured_password=generate_password_hash(password=form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.get_all_posts'))
    return render_template("register.html", form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        email_input = form.email.data
        password_input = form.password.data
        for user in db.session.query(User).all():
            if user.email == email_input:
                if check_password_hash(pwhash=user.secured_password, password=password_input):
                    login_user(user)
                    return redirect(url_for('main.get_all_posts'))
                else:
                    flash(message="Wrong password")
                    return redirect(url_for("auth.login"))
        flash(message="The email hasn't existed yet")
    return render_template("login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.get_all_posts'))


@auth.route("/new-post", methods=['GET', 'POST'])
@admin_only
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_blog_post = BlogPost(title=form.title.data,
                                 subtitle=form.subtitle.data,
                                 body=form.body.data,
                                 author=current_user,
                                 img_url=form.img_url.data,
                                 date=datetime.datetime.now().strftime("%B %d, %Y")
                                 )
        db.session.add(new_blog_post)
        db.session.commit()
        return redirect(url_for('main.get_all_posts'))
    return render_template("make-post.html", form=form, update=False)


@auth.route("/edit-post/<int:post_id>", methods=['POST', 'GET'])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for('main.show_post', index=post_id))
    return render_template("make-post.html", form=form, update=True)


@auth.route("/delete")
@admin_only
def delete_post():
    post_id = request.args.get("post_id")
    deleting_post = BlogPost.query.get_or_404(post_id)
    db.session.delete(deleting_post)
    db.session.commit()
    return redirect(url_for('main.get_all_posts'))


@auth.route("/delete_comment")
def delete_comment():
    comment = Comment.query.get_or_404(request.args.get("comment_id"))
    post_id = request.args.get("post_id")
    if hasattr(current_user, "id"):
        if current_user.id == 1 or current_user.id == comment.author.id:
            db.session.delete(comment)
            db.session.commit()
    return redirect(url_for("main.show_post", index=post_id))
