# extra functions for patw
from flask import render_template
from flask_login import current_user
from patw.models import Polar

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['zip'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def err(input=None, number=None):
    if not input:
        return render_template("error.html", message="Page not found... I should probably make it...", code="501")
    else:
        return render_template("error.html", message=input, code=str(number))

def get_map_list():
    maps = Polar.query.filter_by(user_id=current_user.user_id
                ).group_by(Polar.map_name).order_by(Polar.date_created).all()
    list = []
    for map in maps:
        list.append(map.map_name)
    return list
