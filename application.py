
import os
import helpers
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, redirect, render_template, request, session

# Configure application + database
app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Auto reload templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
    if request.method == "POST":
        return helpers.lol()
    else:
        return render_template("register.html")

@app.route("/<name>")
def other(name):
    return helpers.lol("Still not made /"+name, 501)

if __name__=="__main__":
        app.run(debug=True)
