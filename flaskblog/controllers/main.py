import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask import current_app as app
from flaskblog.models import db
from flaskblog.extensions import cache
from flaskblog.forms import (LoginForm, RegistrationForm, UpdateAccountForm, PostForm,
                             RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_mail import Message



main = Blueprint('main', __name__)

@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')

@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', title='Register', form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data )

        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".view_post"))

    return render_template("login.html", form=form)

@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", "success")

    return redirect(url_for(".home"))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@main.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@main.route("/about")
def about():
    return render_template("about.html")


# --------------------------------- Post CRUD -------------------------------------------#

@main.route("/view-all")
def view_post():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template("posts.html", posts=posts, legend = "Recent Posts ")


@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('.view_post'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('.view_post'))


@main.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

# --------------------------------- Reset Password ---------------------------------------#

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
                 {url_for('.reset_token', token=token, _external=True)}
                 If you did not make this request then simply ignore this email and no changes will be made.
                 '''
    app.mail.send(msg)


@main.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated():
        return redirect(url_for('.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #send_reset_email(user)
        flash('todo: an email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@main.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated():
        return redirect(url_for('.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Sorry, that is an invalid or expired token', 'warning')
        return redirect(url_for('.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
