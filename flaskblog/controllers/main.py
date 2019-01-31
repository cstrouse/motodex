from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required

from flaskblog.extensions import cache
from flaskblog.forms import LoginForm
from flaskblog.models import User


posts = [
    {
        'author': 'BW Block',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Jan 31, 2019'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


main = Blueprint('main', __name__)



@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))

    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))


@main.route("/post")
@login_required
def view_post():
    return render_template("posts.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html")