# encoding: utf-8

import os
from flask import Flask, jsonify, request, session, redirect, render_template, flash, url_for
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators
from models import db, bcrypt, User

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
    user_id = TextField(u'Käyttäjätunnus', validators=[validators.Required(u'Käyttäjätunnus on pakollinen.')])
    password = PasswordField(u'Salasana', validators=[validators.Required(u'Salasana on pakollinen.')])

@app.context_processor
def inject_user():
    user_id = session.get('logged_user', None)
    if user_id:
        user = User.query.get(user_id)
        if user:
            return {'user': user, 'logged_in': True}
        else:
            return {}
    return {}

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.user_id.data)
        if not user:
            form.user_id.errors = [u'Virheellinen käyttäjätunnus.']
        elif not user.authenticate(form.password.data):
            form.password.errors = [u'Virheellinen salasana.']
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

"""
@app.route('/users', methods=['POST'])
def user_add():
    json = request.json['user']
    user = User(json['id'], json['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user=user.dict()), 200
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
