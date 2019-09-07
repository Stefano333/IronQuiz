from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1)])
    submit = SubmitField('Register or Sign In')


class QuestionsForm(FlaskForm):
    question = StringField('Question', [validators.Length(min=1)])
    right_answer = StringField('Right answer', [validators.Length(min=1)])
    wrong_answer = StringField('Wrong answer', [validators.Length(min=1)])
