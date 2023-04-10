"""Seed file to make sample data for users db"""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isnt empty, empty it
User.query.delete()

# Add Users
peter = User(first_name='Peter', last_name='Smith')
jon = User(first_name='Jon', last_name='Jacob')
andrew = User(first_name='Andrew', last_name='Smith')
jessica = User(first_name='Jessica', last_name='Hope')

# Add new objets to session, so they'll persis
db.session.add(peter)
db.session.add(jon)
db.session.add(andrew)
db.session.add(jessica)

# Commit--otherwise, this never gets saved!
db.session.commit()
