from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1)], render_kw={
                           "placeholder": "Your username"})
    submit = SubmitField('Register or Sign In')


class QuestionsForm(FlaskForm):
    question = StringField('Question', [validators.Length(min=1)], render_kw={
                           "placeholder": "Your question"})
    right_answer = StringField('Right answer', [validators.Length(
        min=1)], render_kw={"placeholder": "Right answer"})
    submit_new_question = SubmitField('Submit question')


class AnswersForm(FlaskForm):
    answer = StringField('Answer', [validators.Length(min=1)], render_kw={
                         "placeholder": "Your answer..."})
