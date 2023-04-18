"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_image_url = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
    db.app = app
    db.init_app(app)


# Models Go Below:
class User(db.Model):
    """Site User"""
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id} first name= {u.first_name} last name={u.last_name} image url={default_image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False, unique=True)
    last_name = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, nullable=True)

    def greet(self):
        return f"Hi I am {self.first_name} {self.last_name}"


class Post(db.Model):
    """User Post"""
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<Post id={p.id} Post title={p.title} Post content={p.content} Post created_at={p.created_at} Post User id={p.user_id}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts')

    @property
    def nice_datetime(self):
        """Formatted Date"""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
