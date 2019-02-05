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


@main.route("/about")
def about():
    return render_template("about.html")




