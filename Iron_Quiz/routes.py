from Iron_Quiz import app
from flask import render_template, request, flash, redirect, url_for, session
from Iron_Quiz.forms import LoginForm, QuestionsForm, AnswersForm
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from Iron_Quiz.dbconfig import get_user, get_current_question, insert_new_question, book_answer


@app.route('/')
def home():
    logged_in = session.get('logged_in')
    logged_user = session.get('username')

    if not logged_in:
        return redirect(url_for('login'))
    elif logged_in and logged_user:
        if logged_user == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('quiz'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        if login_form.validate_on_submit():
            session['logged_in'] = True
            username = session['username'] = login_form.username.data

            if username == 'admin':
                return redirect(url_for('admin'))
            else:
                get_user(username)
                return redirect(url_for('quiz'))
    return render_template('login.html', form=login_form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    current_question = get_current_question()
    question_form = QuestionsForm()

    if request.method == 'POST':
        if question_form.validate_on_submit():
            insert_new_question(question_form.question.data,
                                question_form.right_answer.data, question_form.wrong_answer.data)

            return redirect(url_for('admin'))

    if current_question:
        return render_template('admin.html', current_question=current_question)
    return render_template('admin.html', question_form=question_form)


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    current_question_id = get_current_question()['id']
    logged_user = session.get('username')

    if request.method == 'POST':
        book_answer(logged_user, current_question_id)

    return render_template('quiz.html')
