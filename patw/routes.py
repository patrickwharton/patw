from patw import app, db
from patw.forms import RegistrationForm, LogInForm
from patw.helpers import add_map, allowed_file, err, get_map_data, get_map_list
from patw.models import User, Polar
from flask import jsonify, redirect, render_template, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from validate_email import validate_email
from werkzeug.security import check_password_hash, generate_password_hash


db.create_all()
if not User.query.filter_by(username="admin").first():
    admin = User(username="admin", email="admin", hash=generate_password_hash("p"))
    db.session.add(admin)
    db.session.commit()


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
            add_map(file)
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
    map_list = get_map_list()
    if not map_list:
        flash("You don't seem to have any maps yet, here's one I made earlier!", "info")
        return redirect("/patricksmap")
    most_recent_map = map_list[-1]
    data = get_map_data(current_user.user_id, most_recent_map)
    return render_template("map.html", data=data, list=map_list)

@app.route("/patricksmap")
def patricksmap():
    data = get_map_data(User.query.filter_by(username='admin').first().user_id, 'admin')
    return render_template("map.html", data=data, patrick=True)

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
