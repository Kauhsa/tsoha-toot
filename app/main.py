# encoding: utf-8

import os
from flask import Flask, session, redirect, render_template, flash, url_for, g
from flaskext.gravatar import Gravatar
from models import db, bcrypt, User, Tweet
from forms import LoginForm, RegistrationForm, TweetForm


def initalize_app():
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///database'),
        SECRET_KEY="top secret okay"
    )
    bcrypt.init_app(app)
    db.init_app(app)
    Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False)
    return app

app = initalize_app()


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
        new_user = User(form.user_id.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        session['logged_user'] = new_user.id
        flash(u'Rekisteröityminen onnistui!')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/user/<user_id>', methods=('GET', 'POST'))
def user(user_id):
    user = User.query.get_or_404(user_id)
    tweet_form = TweetForm()

    if tweet_form.validate_on_submit() and g.logged_user:
        tweet = Tweet(g.logged_user, tweet_form.content.data)
        db.session.add(tweet)
        db.session.commit()
        tweet_form.content.data = ''  # TODO: keksi siistimpi keino
        flash(u'Uusi töötti lisätty!')

    return render_template('user.html', user=user, tweet_form=tweet_form)


@app.route('/follow/<user_id>', methods=('GET',))
def follow(user_id):
    user = User.query.get_or_404(user_id)

    if user in g.logged_user.following:
        flash(u'Seuraat jo tätä käyttäjää!')
    elif g.logged_user == user:
        flash(u'Et voi seurata itseäsi!')
    else:
        g.logged_user.following.append(user)
        db.session.add(g.logged_user)
        db.session.commit()
        flash(u'Käyttäjä %s lisätty seurattujen listalle!' % user.id_repr())

    return redirect(url_for('user', user_id=user_id))


@app.route('/unfollow/<user_id>', methods=('GET',))
def unfollow(user_id):
    user = User.query.get_or_404(user_id)

    if user not in g.logged_user.following:
        flash(u'Et seuraa tätä käyttäjää!')
    else:
        g.logged_user.following.remove(user)
        db.session.add(g.logged_user)
        db.session.commit()
        flash(u'Käyttäjän %s seuraaminen lopetettu!' % user.id_repr())

    return redirect(url_for('user', user_id=user_id))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
