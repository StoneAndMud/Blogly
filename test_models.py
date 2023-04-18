from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Cleanup existing Users"""

        User.query.delete()

    def tearDown(self):
        """Cleanup any fouled transaction"""
        db.session.rollback()

    def test_greet(self):
        user = User(first_name="TestFirstName", last_name="TestLastName")
        self.assertEquals(pet.greet(), "Hi I am TestFirstName TestLastName")
