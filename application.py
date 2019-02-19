from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
        app.run(debug=True)
