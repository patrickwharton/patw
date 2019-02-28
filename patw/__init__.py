from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Configure application + database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'#os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0a2dbe5f115d5f81eeab2e75c65f98930f7b958a'
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "/login"
login_manager.login_message_category="warning"

from patw import routes
