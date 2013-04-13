import re
import string
from datetime import datetime
from sqlalchemy import or_
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

USER_ID_CHARS = string.ascii_lowercase
PASSWORD_CHARS = string.printable

db = SQLAlchemy()
bcrypt = Bcrypt()


follows = db.Table('follows',
                   db.Column('follower_id', db.String(20), db.ForeignKey('user.id')),
                   db.Column('followed_id', db.String(20), db.ForeignKey('user.id')))

mentions = db.Table('mentions',
                    db.Column('tweet_id', db.Integer(), db.ForeignKey('tweet.id')),
                    db.Column('user_id', db.String(20), db.ForeignKey('user.id')))

taggings = db.Table('taggings',
                    db.Column('tweet_id', db.Integer(), db.ForeignKey('tweet.id')),
                    db.Column('tag_id', db.String(140), db.ForeignKey('tag.id')))


class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(254))
    pw_hash = db.Column(db.String(60))
    following = db.relationship('User',
                                secondary=follows,
                                backref='followers',
                                primaryjoin=id == follows.c.follower_id,
                                secondaryjoin=id == follows.c.followed_id)

    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.pw_hash = bcrypt.generate_password_hash(password)

    def id_repr(self):
        return u'@' + self.id

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)

    def does_follow(self, user):
        return user in self.following

    def wall(self):
        # TODO: can be optimized to single query methinks
        following_set = set(user.id for user in self.following)
        return Tweet.query.filter(or_(Tweet.author_id.in_(following_set), Tweet.mentions.contains(self)))\
                          .order_by(Tweet.timestamp.desc()).limit(10).all()


class Tweet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime())
    author_id = db.Column(db.String(20), db.ForeignKey('user.id'))
    author = db.relationship('User',
                             backref=db.backref('tweets',
                                                lazy='dynamic',
                                                order_by=timestamp.desc()))
    mentions = db.relationship('User',
                               secondary=mentions,
                               backref='mentioned_in')
    tags = db.relationship('Tag',
                           secondary=taggings,
                           backref=db.backref('tweets',
                                              order_by=timestamp.desc()))

    def _parse_mentions(self):
        return [user.lower() for user in re.findall(r'@([a-zA-Z]+)', self.content)]

    def _parse_tags(self):
        return [tag.lower() for tag in re.findall(r'#([a-zA-Z0-9_]+)', self.content)]

    def __init__(self, author, content):
        self.author = author
        self.content = content
        self.timestamp = datetime.utcnow()

        for user_id in self._parse_mentions():
            user = User.query.get(user_id)
            if user:
                self.mentions.append(user)

        for tag_id in self._parse_tags():
            tag = Tag.query.get(tag_id)
            if not tag:
                tag = Tag(tag_id)
                db.session.add(tag)
            self.tags.append(tag)


class Tag(db.Model):
    id = db.Column(db.String(140), primary_key=True)

    def __init__(self, id):
        self.id = id
