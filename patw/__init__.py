from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
# Configure application + database


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "/login"
login_manager.login_message_category="warning"

from patw import routes
