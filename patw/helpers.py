# extra functions for patw
from flask import redirect, render_template, request, session
from functools import wraps


def err(input=None, number=None):
    if not input:
        return render_template("error.html", message="Page not found... I should probably make it...", code="501")
    else:
        return render_template("error.html", message=input, code=str(number))

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
