import string
from datetime import datetime, timedelta
from flask import Flask
from timesince import timesince
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask.ext.bcrypt import Bcrypt

USER_ID_CHARS = string.ascii_lowercase
PASSWORD_CHARS = string.printable

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    pw_hash = db.Column(db.String(60))

    def __init__(self, id, password):
        self.id = id
        self.pw_hash = bcrypt.generate_password_hash(password)

    def id_repr(self):
        return u'@' + self.id

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)

class Tweet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime())
    author_id = db.Column(db.String(20), db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('tweets', lazy='dynamic', order_by=timestamp.desc()))

    def __init__(self, author, content):
        self.author = author
        self.content = content
        self.timestamp = datetime.utcnow()

    def natural_timestamp(self):
        return timesince(self.timestamp)
