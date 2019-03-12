import os
from patw import app, db
from patw.forms import RegistrationForm, LogInForm
from patw.helpers import LABEL_LIST, add_map, allowed_file, err, get_map_data, get_map_list, label_maker, save_file
from patw.models import User, Polar
from flask import Markup, jsonify, redirect, render_template, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from validate_email import validate_email
from werkzeug.security import check_password_hash, generate_password_hash


db.create_all()
# TEMPORARY # Creates admin profile and initialises Patrick's Map
if not User.query.filter_by(username="padmin").first():
    admin = User(username="padmin", email="padmin",
                hash=generate_password_hash(app.config['SECRET_KEY']))
    db.session.add(admin)
    db.session.commit()
    file_location = app.root_path + "/static/admin_data.zip"
    admin = User.query.filter_by(username="padmin").first()
    add_map(file_location, map_name='admin', user_id=admin.user_id)


@app.route("/")
def index():
    return render_template("index.html", loginform = LogInForm())

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
            file_location = save_file(file)
            error = add_map(file_location)
            os.remove(file_location)
            if error == 0:
                return redirect("/map")
            else:
                flash(f"Error {error}: Please select a valid Polarsteps .zip file.", "danger")
                return redirect("/createmap")
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

@app.route("/history")
@login_required
def history():
    user = User.query.filter_by(user_id=current_user.user_id).first()
    map_data = user.map_data
    if not map_data:
        flash(Markup("You don't seem to have any maps yet, so here's one I made earlier! <a href='/createmap' class='alert-link'>Click here to make your own!</a>"), "info")
        return redirect("/patricksmap")
    return render_template("history.html", data=map_data)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Sign in users"""
    if current_user.is_authenticated:
        flash("Already logged in, please log out to change user", "warning")
        return redirect("/")
    loginform = LogInForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and check_password_hash(user.hash, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            flash(f"Successfully logged in. Welcome back {user.username}!", "success")
            if request.args.get("next"):
                return redirect(request.args.get("next"))
            else:
                return redirect("/")
        flash("Login attempt failed. Incorrect email address or password", "danger")

    return render_template("login.html", loginform=loginform)

@app.route("/logout")
def logout():
    logout_user()
    flash("Log out successful.", "success")
    return redirect("/")

@app.route("/map", methods=["GET", "POST"])
@login_required
def map():
    map_list = get_map_list()
    if not map_list:
        flash(Markup("You don't seem to have any maps yet, so here's one I made earlier! <a href='/createmap' class='alert-link'>Click here to make your own!</a>"), "info")
        return redirect("/patricksmap")
    if request.args.get('m'):
        map_name = request.args.get('m')
        if map_name not in map_list:
            flash(f"You don't have a map called {map_name}!", "warning")
            map_name = map_list[0]
    else:
        map_name = map_list[0]

    if request.args.get('l'):
        label = request.args.get('l')
        if label not in LABEL_LIST:
            flash(f"{label} is not a supported time period.", "warning")
            label = 'Days'
    else:
        label = 'Days'

    data = get_map_data(current_user.user_id, map_name)
    data = label_maker(data)
    if len(map_list) == 1:
        map_list = []
    return render_template("map.html", data=data, map_list=map_list,
                current_map=map_name, label=label, label_list=LABEL_LIST)

@app.route("/patricksmap")
def patricksmap():
    if request.args.get('l'):
        label = request.args.get('l')
        if label not in LABEL_LIST:
            flash(f"{label} is not a supported time period.", "warning")
            label = 'Days'
    else:
        label = 'Days'
    data = get_map_data(User.query.filter_by(username='padmin').first().user_id, 'admin')
    data = label_maker(data)
    return render_template("map.html", loginform = LogInForm(), data=data, patrick=True, label=label, label_list=LABEL_LIST)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register users"""
    form = RegistrationForm()
    if request.method == "GET":
        return render_template("register.html", form=form, loginform = LogInForm())

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
        flash(Markup(f"Account Created for {username}!<a href='/login' class='alert-link'> Click here to Log In</a>"), "success")
    else:
        return err("How did I get here?")

    return redirect("/")



@app.route("/<name>")
def other(name):
    return err()
