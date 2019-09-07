import os
basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_dir = 'sqlite:///' + os.path.join(basedir, 'app.db')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-word'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or sqlite_dir
    SQLALCHEMY_TRACK_MODIFICATIONS = False
