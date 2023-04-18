"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "bloglyiscool21123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()


@app.route('/')
def root():
    return redirect("/users")


@app.route('/users')
def list_users():
    """Shows users list"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('/users/users.j2', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('users/form.j2')


@app.route('/users/new', methods=["POST"])
def create_user():

    new_user = User(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image_url=request.form["image_url"] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single User"""
    user = User.query.get_or_404(user_id)
    return render_template('users/details.j2', user=user)


@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.j2', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# Routes for Posts


@app.route('/users/<int:user_id>/posts/new')
def post_new_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('posts/form.j2', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details about a single Post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/details.j2', post=post)


@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.j2', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")

    return redirect(f"/users/{post.user_id}")
