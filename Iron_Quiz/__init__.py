#import eventlet
from flask import Flask
from config import Config
# import flask_login
from flask_socketio import SocketIO
# from flask_bootstrap import Bootstrap
from Iron_Quiz.quiz_status import Quiz

#eventlet.monkey_patch()
application = Flask(__name__)
application.config.from_object(Config)

# login_manager = flask_login.LoginManager()
# login_manager.init_app(application)


# Bootstrap(application)

socketio = SocketIO(application)

from Iron_Quiz import application as app
from Iron_Quiz import routes

# if __name__ == '__main__':
socketio.run(app, debug=True, host='0.0.0.0')
# socketio.run(app, debug=True, port=8080)
