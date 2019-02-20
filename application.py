
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

@app.route("/register")
def register():
    return helpers.lol()

@app.route("/<name>")
def other(name):
    return helpers.lol("Still not made /"+name, 501)

if __name__=="__main__":
        app.run(debug=True)
