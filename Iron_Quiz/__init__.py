#import eventlet
from flask import Flask
from config import Config
from flask_socketio import SocketIO
# from flask_login import *
# from flask_bootstrap import Bootstrap

#eventlet.monkey_patch()
application = Flask(__name__)
application.config.from_object(Config)
# login_manager = LoginManager()

# login_manager.init_app(application)


# Bootstrap(application)

socketio = SocketIO(application)

from Iron_Quiz import application as app
from Iron_Quiz import routes

# if __name__ == '__main__':
socketio.run(app, debug=True)
# socketio.run(app, debug=True, port=8080)