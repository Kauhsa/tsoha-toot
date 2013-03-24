# encoding: utf-8

import os, string
from flask import Flask, jsonify, request, session, redirect, render_template, flash, url_for, g
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, ValidationError, TextAreaField
from models import db, bcrypt, User, Tweet

def initalize_app():
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///database'),
        SECRET_KEY="top secret okay"
    )
    bcrypt.init_app(app)
    db.init_app(app)
    return app

app = initalize_app()

class LoginForm(Form):
    user_id = TextField(u'Käyttäjätunnus', [validators.Required(u'Käyttäjätunnus on pakollinen.')])
    password = PasswordField(u'Salasana', [validators.Required(u'Salasana on pakollinen.')])

class RegistrationForm(Form):
    user_id = TextField(u'Käyttäjätunnus', [
        validators.Required(u'Käyttäjätunnus on pakollinen.'),
        validators.Length(min=2, max=20, message=u'Käyttäjätunnuksen pituuden on oltava 2-20 merkkiä.')
    ])
    password = PasswordField(u'Salasana', [
        validators.Required(u'Salasana on pakollinen.'),
        validators.Length(min=8, message=u'Salasanan pituuden on oltava vähintään 8 merkkiä.')
    ])
    password_confirm = PasswordField(u'Salasana uudestaan', [
        validators.Required(u'Salasanan vahvistus on pakollinen.'),
        validators.EqualTo('password', message=u'Salasanojen täytyy täsmätä.')
    ])

    def validate_user_id(form, field):
        if any(char not in string.lowercase for char in field.data):
            raise ValidationError(u'Käyttäjätunnuksen täytyy koostua vain pienistä aakkosista a-z.')
        if User.query.get(form.user_id.data):
            raise ValidationError(u'Käyttäjätunnus on varattu.')

class TweetForm(Form):
    content = TextAreaField(u'Töötti', [validators.Required(u'Töötti on pakollinen.')])

@app.before_request
def set_logged_user():
    user_id = session.get('logged_user', None)
    g.logged_user = None
    if user_id:
        user = User.query.get(user_id)
        if user:
            g.logged_user = user

@app.context_processor
def inject_user():
    if g.logged_user:
        return {'logged_user': g.logged_user, 'logged_in': True}
    return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.user_id.data)
        if not user:
            form.user_id.errors = [u'Tuntematon käyttäjätunnus.']
        elif not user.authenticate(form.password.data):
            form.password.errors = [u'Salasana ei täsmää.']
        else:
            flash(u'Olet kirjautunut sisään!')
            session['logged_user'] = user.id
            return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_user', None)
    flash(u'Olet kirjautunut ulos!')
    return redirect(url_for('index'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(form.user_id.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        session['logged_user'] = new_user.id
        flash(u'Rekisteröityminen onnistui!')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/users/<user_id>', methods=('GET', 'POST'))
def user(user_id):
    user = User.query.get_or_404(user_id)
    tweet_form = TweetForm()

    if tweet_form.validate_on_submit() and g.logged_user:
        tweet = Tweet(g.logged_user, tweet_form.content.data)
        db.session.add(tweet)
        db.session.commit()
        tweet_form.content.data = '' # TODO: keksi siistimpi keino
        flash(u'Uusi töötti lisätty!')

    return render_template('user.html', user=user, tweet_form=tweet_form)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
