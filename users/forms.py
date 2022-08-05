from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Regexp, Email, EqualTo, ValidationError

from .models import User
from extention import db


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(min=3, max=100, message='Please provide a valid name'),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                'Usernames must have only letters, ' 'numbers, dots or underscores',),
        ])
    email = StringField(validators=[InputRequired(), Email(), Length(min=5, max=100)])
    passwd = PasswordField(validators=[InputRequired(), Length(min=1, max=100)])
    passwd_confirm = PasswordField(
                    validators=[
                                InputRequired(),
                                Length(min=1, max=100),
                                EqualTo('passwd', message='Passwords must match!'),
                                ]
                    )

    def validate_email(self, email):
        if db.session.query(User).filter_by(email=email.data).first(): #User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered!')

    def validate_username(self, username):
        if db.session.query(User).filter_by(username=username.data).first(): #User.query.filter_by(username=username.data).first():
            raise ValidationError('The username already exist!')


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(min=5, max=100)])
    passwd = PasswordField(validators=[InputRequired(), Length(min=1, max=100)])


class PasswdForgotForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(min=5, max=100)])


class PasswdRecover(FlaskForm):
    passwd = PasswordField(validators=[InputRequired(), Length(min=1, max=100)])
    passwd_confirm = PasswordField(
        validators=[
            InputRequired(),
            Length(min=1, max=100),
            EqualTo('passwd', message='Passwords must match!'),
        ]
    )



