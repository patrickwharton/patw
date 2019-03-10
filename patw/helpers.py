# extra functions for patw
from datetime import datetime
from flask import render_template, redirect, request
from flask_login import current_user
import os
from patw import app, db
from patw.models import Polar
from patw.time_spent import time_spent as ts
from werkzeug.utils import secure_filename

def add_map(file_location, map_name=None, user_id=None):
    countries, accounted_for = ts(file_location)
    data = []

    if not user_id:
        user_id = current_user.user_id

    if not map_name:
        map_name = request.form.get('name')

    if not map_name:
        map_name = datetime.utcnow()
        date_created = map_name
    else:
        date_created = datetime.utcnow()

    if Polar.query.filter_by(user_id=user_id, map_name=map_name).first():
        flash("You've already used that map name!", "warning")
        return redirect("/createmap")

    for country, time in countries.items():
        data.append({"id":country, "value":time})
        entry = Polar(user_id=user_id, country_code=country,
                    time_spent=time, map_name=map_name, date_created=date_created)
        db.session.add(entry)
    db.session.commit()

def save_file(file):
    filename = secure_filename(file.filename)
    file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_location)
    return file_location

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['zip'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def err(input=None, number=None):
    if not input:
        return render_template("error.html", message="Page not found... I should probably make it...", code="501")
    else:
        return render_template("error.html", message=input, code=str(number))

def get_map_data(user_id, map_name):
    data = []
    map_data = Polar.query.filter_by(user_id=user_id, map_name=map_name)

    for entry in map_data:
        data.append({"id":entry.country_code, "value":entry.time_spent})
    return data

def get_map_list():
    maps = Polar.query.filter_by(user_id=current_user.user_id
                ).group_by(Polar.map_name).order_by(Polar.date_created).all()
    list = []

    for map in maps:
        list.append(map.map_name)
    return list
