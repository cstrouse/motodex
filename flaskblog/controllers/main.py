from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flaskblog.extensions import cache

main = Blueprint('main', __name__)



@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/about")
def about():
    return render_template("about.html")




