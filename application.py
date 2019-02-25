import os
import helpers
from forms import RegistrationForm, LogInForm
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, redirect, render_template, request, session, flash
from flask_session import Session
from validate_email import validate_email
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

@app.route("/checkemail", methods=["GET"])
def emailcheck():
    """
    Checks if email is a valid address, but not if the
    domain exists or if the email actually exists,
    and returns true or false in JSON format
    """
    return jsonify(validate_email(request.args.get("email")))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register users"""
    form = RegistrationForm()
    if request.method == "GET":
        return render_template("register.html", form=form)

    # Server-side checks
    if not request.form.get("username"):
        return helpers.err("User must provide username", 400)
    elif not request.form.get("password"):
        return helpers.err("User must provide password", 400)
    elif not request.form.get("confirm_password"):
        return helpers.err("User must retype password", 400)
    if request.form.get("password") != request.form.get("confirm_password"):
        return helpers.err("Passwords do not match")
    if not validate_email(request.form.get("password")):
        return helpers.err("Invalid email")
    elif form.email.errors:
        return helpers.err("OK so these email validators are different")

    email = request.form.get("email")
    username = request.form.get("username")
    hash = generate_password_hash(request.form.get("password"))

    # Duplicate emails are still unaccounted for

    if form.validate_on_submit():
        flash(f"Account Created for {form.username.data}!", "success")
    else:
        return helpers.err("How did I get here?")

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Sign in users"""
    form = LogInForm()
    if request.method == "GET":
        return render_template("login.html", form=form)
    return helpers.err("Still not made /", 501)


@app.route("/<name>")
def other(name):
    return helpers.err("Still not made /"+name, 501)

if __name__=="__main__":
        app.run(debug=True)
