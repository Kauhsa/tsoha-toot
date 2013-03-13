import string
from flask import Flask
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
        password = self.validate_password(password)
        self.id = id
        self.pw_hash = bcrypt.generate_password_hash(password)

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)

    def validate_password(self, password):
        assert len(password) > 9
        assert all(char in PASSWORD_CHARS for char in password)
        return password

    @validates('id')
    def validate_id(self, key, id):
        assert len(id) > 2
        assert all(char in USER_ID_CHARS for char in id)
        return id
