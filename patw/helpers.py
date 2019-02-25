# extra functions for patw
from flask import render_template

def err(input=None, number=None):
    if not input:
        return render_template("error.html", message="Page not found... I should probably make it...", code="501")
    else:
        return render_template("error.html", message=input, code=str(number))
