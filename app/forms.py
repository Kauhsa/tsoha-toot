# encoding: utf-8

import string
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, ValidationError, TextAreaField
from models import User


class LoginForm(Form):
    user_id = TextField(u'Käyttäjätunnus', [validators.Required(u'Käyttäjätunnus on pakollinen.')])
    password = PasswordField(u'Salasana', [validators.Required(u'Salasana on pakollinen.')])


class RegistrationForm(Form):
    user_id = TextField(u'Käyttäjätunnus', [
        validators.Required(u'Käyttäjätunnus on pakollinen.'),
        validators.Length(min=2, max=20, message=u'Käyttäjätunnuksen pituuden on oltava 2-20 merkkiä.')
    ])
    email = TextField(u'Sähköpostiosoite', [
        validators.Required(u'Sähköpostiosoite on pakollinen.'),
        validators.Length(max=254, message=u'Sähköpostiosoite on liian pitkä.'),
        validators.Email(u'Sähköpostiosoite on virheellinen.')
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
