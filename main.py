from Iron_Quiz import app

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from Iron_Quiz import app
# from flask import render_template, request, flash, redirect, url_for
# from forms import LoginForm, QuestionsForm
# from config import Config

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


# @app.route('/', methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm()

#     if request.method == 'POST':
#         if login_form.validate_on_submit():
#             username = login_form.username.data
#             print(username)
#             if username == 'admin':
#                 return redirect(url_for('admin'))
#             else:
#                 return redirect(url_for('user'))
#     return render_template('login.html', form=login_form)


# @app.route('/admin')
# def admin():
#     question_form = QuestionsForm()
#     return render_template('admin.html', question_form=question_form)
