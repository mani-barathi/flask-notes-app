from sqlalchemy.sql import func
from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(id):
    print("called")
    return User.query.get(id)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250))
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    notes = db.relationship('Note',backref="notes", lazy=True)

