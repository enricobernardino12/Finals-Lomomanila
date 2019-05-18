import flask_sqlalchemy
from flask_login import UserMixin
from datetime import datetime
from time import time
db = flask_sqlalchemy.SQLAlchemy()



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    birthdate = db.Column(db.DateTime)
    instagram_account = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    favecam = db.Column(db.String(100))
    faveroll = db.Column(db.String(100))
    favesubject = db.Column(db.String(200))
    posts = db.relationship('Post', backref='author', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

