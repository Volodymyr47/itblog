from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Regexp, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField

from users.models import User, UserRole
from extention import db


def get_role_names():
    return db.session.query(UserRole).filter_by(is_active=True)


class AdminRegisterForm(FlaskForm):

    username = StringField(
        validators=[
            InputRequired(),
            Length(min=3, max=100, message='Please provide a valid name'),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                'Usernames must have only letters, ' 'numbers, dots or underscores',),
        ])
    email = EmailField(validators=[InputRequired(), Email(), Length(min=5, max=100)])
    rolename = QuerySelectField(query_factory=get_role_names, allow_blank=True,
                                validators=[InputRequired()], blank_text='Select user role...')
    passwd = PasswordField(validators=[InputRequired(), Length(min=1, max=100)])
    passwd_confirm = PasswordField(
        validators=[
            InputRequired(),
            Length(min=1, max=100),
            EqualTo('passwd', message='Passwords must match !'),
        ]
    )

    def validate_email(self, email):
        if db.session.query(User).filter_by(email=email.data).first():
            raise ValidationError('Email already registered!')

    def validate_username(self, username):
        if db.session.query(User).filter_by(username=username.data).first():
            raise ValidationError('The username already exist!')


class AdminLoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=100)])
    passwd = PasswordField(validators=[InputRequired(), Length(min=1, max=100)])


# class passwd_forgot(FlaskForm):
#     email = StringField(validators=[InputRequired(), Email(), Length(min=5, max=100)])
#
#     def send_passwd_forgot(self, email):
#         sender = user_app.mail
#         try:
#             user_app.mail.send_message('Mail Reset', email,
#                              "Please, go to the link ro reset your password!. Don't replay to this message",
#                              sender, user_app.datetime.utcnow())
#             return 'Message sended successful'
#         except Exception as err:
#             return f'Sending message error: {err}'


