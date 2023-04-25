"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    tags = Tag.query.all()
    return render_template('posts/form.j2', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user=user,
        tags=tags)

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
    tags = Tag.query.all()
    return render_template('posts/edit.j2', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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

# Routes for Tags


@app.route('/tags')
def list_tags():
    """Show a list of tags"""
    tags = Tag.query.all()
    return render_template(f"/tags/tags.j2", tags=tags)


@app.route('/tags/new')
def new_tags_form():
    """shows form for new tag"""
    posts = Post.query.all()
    return render_template('/tags/form.j2', posts=posts)


@app.route('/tags/new', methods=["POST"])
def new_tag():
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """"show details on specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/details.j2', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """show form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('/tags/edit.j2', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")
    return redirect('/tags')
