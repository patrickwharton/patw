from datetime import datetime
from patw import app, db
from patw.forms import RegistrationForm, LogInForm
from patw.helpers import err, allowed_file, get_map_list
from patw.models import User, Polar
from patw.time_spent import time_spent as ts
from flask import jsonify, redirect, render_template, request, flash
from flask_login import login_user, logout_user, current_user, login_required
import os
from validate_email import validate_email
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

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

@app.route("/createmap", methods=["GET", "POST"])
@login_required
def createmap():
    if request.method == "POST":
        if 'polardata' not in request.files:
            return redirect(request.url)
        file = request.files['polardata']

        if file.filename == '':
            flash('No selected file')
            return redirect("/createmap")

        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            countries, accounted_for = ts(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = []
            map_name = request.form.get('name')
            date_created = datetime.utcnow()
            if not map_name:
                map_name = datetime.utcnow()
                date_created = map_name
            elif Polar.query.filter_by(user_id=current_user.user_id, map_name=map_name).first():
                flash("You've already used that map name!", "warning")
                return redirect("/createmap")
            for country, time in countries.items():
                data.append({"id":country, "value":time})
                entry = Polar(user_id=current_user.user_id, country_code=country,
                            time_spent=time, map_name=map_name, date_created=date_created)
                db.session.add(entry)
            db.session.commit()
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect("/map")
        else:
            flash("Invalid file type")
            return redirect("/createmap")

    return render_template("createmap.html")

@app.route("/checkemail", methods=["GET"])
def emailcheck():
    """
    Checks if email is in database, if so returns 2 in JSON,
    else:
    Checks if email is a valid address, but not if the
    domain exists or if the email actually exists,
    and returns true or false in JSON format
    """
    email = request.args.get("email")
    result = User.query.filter_by(email=email).first()
    if result:
        return jsonify('used')
    return jsonify(validate_email(email))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Sign in users"""
    if current_user.is_authenticated:
        flash("Already logged in, please log out to change user", "warning")
        return redirect("/")
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Successfully logged in! Welcome back {user.username}", "success")
            if request.args.get("next"):
                return redirect(request.args.get("next"))
            else:
                return redirect("/")
        flash("Login attempt failed. Incorrect email address or password", "danger")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Log out successful.", "success")
    return redirect("/")

@app.route("/map")
@login_required
def map():
    data = []
    map_list = get_map_list()
    most_recent_map = map_list[-1]
    map_data = Polar.query.filter_by(user_id=current_user.user_id, map_name=most_recent_map)
    for entry in map_data:
        data.append({"id":entry.country_code, "value":entry.time_spent})
    return render_template("map.html", data=data, list=map_list)

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



@app.route("/<name>")
def other(name):
    return err("Still not made /"+name, 501)
