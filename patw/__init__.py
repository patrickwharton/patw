from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configure application + database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'#os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0a2dbe5f115d5f81eeab2e75c65f98930f7b958a'
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)


from patw import routes


# Initiate session
### TODO figure out flask Session
from flask_session import Session
