from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField
from wtforms.validators import InputRequired


class NewComment(FlaskForm):
    comment_text = TextAreaField(validators=[InputRequired()])
    id = IntegerField()
    level = IntegerField()


class Rating(FlaskForm):
    rating = IntegerField()






