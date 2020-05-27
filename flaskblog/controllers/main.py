from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


@main.route("/about")
def about():
    return render_template("about.html")




