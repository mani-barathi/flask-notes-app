from sqlalchemy.sql import func
from . import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250))
    email = db.Column(db.Text)
    password = db.Column(db.Text)
