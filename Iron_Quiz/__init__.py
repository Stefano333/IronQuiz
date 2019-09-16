#import eventlet
from flask import Flask
from config import Config
from flask_socketio import SocketIO

#eventlet.monkey_patch()
app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)

from Iron_Quiz import app, routes

socketio.run(app, debug=True)