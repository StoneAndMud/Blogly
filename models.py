"""Models for Blogly."""
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

    @ classmethod
    def get_by_X(cls, x):
        return cls.query.filter_by(x=x).all()

    def greet(self):
        return f"Hi I am {self.first_name} {self.last_name}"
