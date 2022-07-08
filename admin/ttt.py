from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,EmailField,SelectFieldBase
from wtforms.validators import InputRequired, Length, Regexp, Email, EqualTo, ValidationError

from users.models import User, UserRole
from extention import db


