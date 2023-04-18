from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample User"""
        User.query.delete()

        user = User(first_name="TestFirstName", last_name="TestLastName")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """cleanup any fouled transaction"""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<a href="/users/1">TestFirstName TestLastName</a>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestFirstName2", "last_name": "TestLastName2"}
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<a href="/users/1">TestFirstName TestLastName</a>", html)
