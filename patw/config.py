# Heavily borrowed from https://realpython.com/flask-by-example-part-1-project-setup/
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '0a2dbe5f115d5f81eeab2e75c65f98930f7b958a'
    UPLOAD_FOLDER = basedir + "/static"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'#os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True

class ProductionConfig(Config):
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
