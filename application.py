import os
import helpers
from forms import RegistrationForm, LogInForm
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application + database
app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0a2dbe5f115d5f81eeab2e75c65f98930f7b958a'
from models import User
db.create_all()

# Auto reload templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Initiate session
### TODO figure out flask Session

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    if len(username) < 1:
        return jsonify(False)

    result = None ##db.execute("SELECT username FROM users WHERE username=:username", username=username)
    if not result:
        return jsonify(True)

    return jsonify(False)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register users"""
    if request.method == "GET":
        form = RegistrationForm()
        return render_template("register.html", form=form)
    email = request.get.form("email")
    return helpers.err(email, 501)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Sign in users"""
    if request.method == "GET":
        form = LogInForm()
        return render_template("login.html", form=form)
    return helpers.err("Still not made /", 501)


@app.route("/<name>")
def other(name):
    return helpers.err("Still not made /"+name, 501)

if __name__=="__main__":
        app.run(debug=True)
