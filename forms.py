from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Email, ValidationError, Length,
                                EqualTo)

from models import User


def email_exists(form, field):
    """This checks the database to see if a user's email already exists
    in the database. If so a ValidationError is raised."""
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('A User with that email already exists.')


class RegisterForm(Form):
    """This is the form users use to register."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    """This is the form that user's login with."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
