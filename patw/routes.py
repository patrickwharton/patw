from patw import app, db
from patw.forms import RegistrationForm, LogInForm
from patw.helpers import err, login_required
from patw.models import User
from flask import jsonify, redirect, render_template, request, session, flash
import os
from validate_email import validate_email
from werkzeug.security import check_password_hash, generate_password_hash

db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    if len(username) < 2 or len(username) > 20:
        return jsonify(False)

    result = User.query.filter_by(username=username).first()
    if not result:
        return jsonify(True)
    return jsonify(False)

@app.route("/checkemail", methods=["GET"])
def emailcheck():
    """
    Checks if email has been used, if so returns 2 in JSON,
    else:
    Checks if email is a valid address, but not if the
    domain exists or if the email actually exists,
    and returns true or false in JSON format
    """
    email = request.args.get("email")
    result = User.query.filter_by(email=email).first()
    if result:
        return jsonify('2')
    return jsonify(validate_email(email))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register users"""
    form = RegistrationForm()
    if request.method == "GET":
        return render_template("register.html", form=form)

    # Server-side checks
    if not request.form.get("username"):
        return err("User must provide username", 400)
    elif not request.form.get("password"):
        return err("User must provide password", 400)
    elif not request.form.get("confirm_password"):
        return err("User must retype password", 400)
    if request.form.get("password") != request.form.get("confirm_password"):
        return err("Passwords do not match")
    if not validate_email(request.form.get("email")):
        return err("Invalid email")
    elif form.email.errors:
        return err("OK so these email validators are different. Please let me know what you entered to get here!")

    email = request.form.get("email")
    username = request.form.get("username")
    hash = generate_password_hash(request.form.get("password"))

    user = User.query.filter_by(username=username).first()
    if user:
        return err("Username already taken.")

    user = User.query.filter_by(email=email).first()
    if user:
        return err("Email address already associated with an account.")

    if form.validate_on_submit():
        user = User(username=username, email=email, hash=hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created for {username}!", "success")
    else:
        return err("How did I get here?")

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Sign in users"""
    form = LogInForm()
    if form.validate_on_submit():
        pass
    return render_template("login.html", form=form)


@app.route("/<name>")
def other(name):
    return err("Still not made /"+name, 501)
