
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog.models import db
from flaskblog.models import User, Post, Category

from flaskblog.posts.forms import PostForm



posts = Blueprint('posts', __name__)


# --------------------------------- Post CRUD -------------------------------------------#

@posts.route("/view-all")
def view_post():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.upvotes.desc()).paginate(page=page, per_page=5)

    return render_template("posts.html", posts=posts, legend = "Recent Posts ")


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    choicelist = [(0,"Choose One"),(1,"Exotic"),(2,"Modern classics"),(3,"Muscle cars"),(4,"Overland/4x4"),(5,"Sports car"),(6,"Corvette"),(7,"I'm looking for...")]
    form.category.choices=choicelist
    if form.validate_on_submit():
        post = Post(content=form.content.data, link=form.link.data, cat=choicelist[int(form.category.data)][1], title=form.title.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('.view_post'))
    return render_template('create_post.html', content='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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

@posts.route("/post/<int:post_id>/flag", methods=['GET', 'POST'])
@login_required
def flag_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.flag_count += 1
    db.session.commit()
    flash("Post has been flagged.", 'success')
    return redirect(url_for('.view_post'))

@posts.route("/post/<int:post_id>/upvote", methods=['GET', 'POST'])
@login_required
def upvote_post(post_id):
	post = Post.query.get_or_404(post_id)
	print(post.upvotes)
	post.upvotes += 1
	db.session.commit()
	flash('Post upvoted!', 'success')
	return redirect(url_for('.view_post'))
    
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('.view_post'))


@posts.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
