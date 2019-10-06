from Iron_Quiz import app, socketio
from flask import render_template, request, flash, redirect, url_for, session
from Iron_Quiz.forms import LoginForm, QuestionsForm, AnswersForm
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from Iron_Quiz.dbconfig import *
from werkzeug.datastructures import ImmutableMultiDict
from Iron_Quiz.quiz_status import QuizStatus, Quiz

room = {}


def reload_client_sessions(*args: str):
    if not args:
        active_clients = {user: sid['sid']
                          for (user, sid) in room.items() if user != "admin"}
        for user, sid in active_clients.items():
            socketio.emit('reloadClient', room=sid)
        print("reload all clients: {}".format(active_clients))
    else:
        print("reload some clients")
        for username in args:
            sid = room[username]['sid']
            socketio.emit('reloadClient', room=sid)
            print("user: {}".format(username))


@app.route('/')
def home():
    logged_in = session.get('logged_in')
    logged_user = session.get('username')

    if not logged_in and not logged_user:
        return redirect(url_for('login'))
    elif logged_in and logged_user:
        if logged_user == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('quiz'))


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

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
                add_new_user(username)
                return redirect(url_for('quiz'))
    return render_template('login.html', form=login_form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    question_form = QuestionsForm()
    logged_user = session.get('username')
    quiz_session = Quiz()
    # status = QuizStatus.NO_QUESTION
    data = {}

    try:
        current_question = get_current_question()['data']

    except KeyError:
        current_question = {}

    if request.method == 'POST':
        if question_form.validate_on_submit():
            insert_new_question(question_form.question.data,
                                question_form.right_answer.data, question_form.wrong_answer.data)

            reload_client_sessions()

            # status = QuizStatus.USER_CAN_BOOK
            status = quiz_session.get_status(current_question)

            return redirect(url_for('admin'))

    if current_question:
        current_question_id = current_question['id']
        status = quiz_session.get_status(current_question)
        current_booking = current_booking_to_deal(current_question_id)[
            'data']

        if current_booking:
            current_booking_placement = current_booking['placement']
            current_booker = current_booking['booker']
            current_booker_can_answer = current_booking['can_answer']
            current_booker_did_answer = current_booking['did_answer']
            checked_answer = current_booking['checked_answer']
            current_booker_did_win = current_booking['did_win']

            if current_booker and not current_booker_can_answer:
                status = quiz_session.get_status(current_question, current_booker, current_booker_can_answer,
                                                 current_booker_did_answer, checked_answer, current_booker_did_win)
                # show the first user in queue for answer and button to allow him

            elif current_booker_can_answer and not current_booker_did_answer:
                status = quiz_session.get_status(current_question)
                # show question and message "waiting for answer" by

            elif current_booker_did_answer and not checked_answer:
                status = quiz_session.get_status(current_question)
                # show question, right answer and user's answer

            elif checked_answer and current_booker_did_win:
                status = quiz_session.get_status(current_question)
                # go to user_won page

            elif checked_answer and not current_booker_did_win:
                status = quiz_session.get_status(current_question)

        data['current_question'], data['current_booking'] = current_question, current_booking
        data['status'], data['logged_user'] = status, logged_user

        return render_template('admin.html', data=data, quiz_status_list=QuizStatus)
        # return render_template('admin.html', current_question=current_question)

    data['logged_user'] = logged_user

    return render_template('admin.html', question_form=question_form, data=data)

#
@app.route('/admin/allow_answer/<int:booking_id>', methods=['POST'])
def allow_user_to_answer(booking_id: int):
    user_can_answer(booking_id)
    current_booker = get_current_booker(booking_id)['data']['booker']

    reload_client_sessions(current_booker)

    return redirect(url_for('admin'))

#
@app.route('/admin/validate_answer/<int:booking_id>', methods=['POST'])
def answer_validated(booking_id: int):
    if request.method == 'POST':
        # user_won = True if request.form.to_dict(
        #     Flat=True)['right_answer'] else False
        if request.form.to_dict()['answer'] == "right":
            user_won = True
        else:
            user_won = False

        validate_answer(booking_id, user_won)

        if user_won:
            reload_client_sessions()
        else:
            current_booker = get_current_booker(booking_id)['data']['booker']
            next_booker = get_next_booker(booking_id)['data']['booker']

            if next_booker:
                reload_client_sessions(current_booker, next_booker)
            else:
                reload_client_sessions(current_booker)

    return redirect(url_for('admin'))


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('socketIsConnected')
def socket_is_connected():
    logged_user = session['username']

    room[logged_user] = {'sid': request.sid}


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    answer_form = AnswersForm()
    quiz = {}
    user_booking_status = {}
    current_question_id = 0

    logged_user = session.get('username')
    status = QuizStatus.NO_QUESTION

    try:
        current_question = get_current_question()['data']
        current_question_id = current_question['id']
        user_booking_status = booking_status(
            logged_user, current_question_id)['data']
        status = QuizStatus.USER_CAN_BOOK
    except KeyError:
        print("there's a problem: {}".format(current_question))
        pass

    if request.method == 'POST':
        # form_data = request.form.to_dict(flat=False)
        if not user_booking_status:
            book_answer(logged_user, current_question_id)

            user_booking_status = booking_status(
                logged_user, current_question_id)['data']

            reload_client_sessions('admin')

            return redirect(url_for('quiz'))

    print("user_booking_status: {}".format(user_booking_status))
    print("current question id: {}".format(current_question_id))

    if user_booking_status:
        booked_answer, can_answer = user_booking_status['booked_answer'], user_booking_status['can_answer']
        did_answer, checked_answer = user_booking_status[
            'did_answer'], user_booking_status['checked_answer']
        did_win, booking_id = user_booking_status['did_win'], user_booking_status['id']

        if booked_answer and not can_answer:  # not post
            status = QuizStatus.USER_WAITING_ALLOWANCE_TO_ANSWER

            flash('Wait for your turn', 'hint')

        elif can_answer and not did_answer:  # not post
            quiz['current_question'] = get_current_question()['data']

            status = QuizStatus.USER_CAN_ANSWER
            # show question and let user to input answer

        elif did_answer and not checked_answer:
            status = QuizStatus.USER_WAITING_VALIDATION

            flash('Wait for answer validation', 'hint')

        # elif checked_answer and did_win:
        #     status = QuizStatus.USER_WON

        #     flash('You won!', 'hint')

        elif checked_answer and not did_win:
            status = QuizStatus.USER_LOST

            flash('Your answer was not right!', 'hint')

        quiz['user_booking_status'], quiz['answer_form'] = user_booking_status, answer_form
    else:
        if not current_question and get_winner(current_question_id, logged_user)['data']:
            status = QuizStatus.USER_WON

            flash('You won!', 'hint')

    quiz['status'], quiz['logged_user'] = status, logged_user

    return render_template('quiz.html', quiz=quiz, quiz_status_list=QuizStatus)


@app.route('/quiz/submit_answer/<int:booking_id>', methods=['POST'])
def allow_answered(booking_id: int):
    answer = request.form.to_dict(flat=True)['answer']

    user_answered(booking_id, answer)
    print("sono qui")

    reload_client_sessions('admin')

    return redirect(url_for('quiz'))
