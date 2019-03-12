# extra functions for patw
from datapackage import Package
from datetime import datetime
from flask import flash, render_template, redirect, request
from flask_login import current_user
import os
from patw import app, db
from patw.forms import LogInForm
from patw.models import Polar
from patw.time_spent import time_spent as ts
from werkzeug.utils import secure_filename

LABEL_LIST = ['Seconds', 'Days', 'Hours', 'Weeks', 'Years']
FLAGS_URL = 'https://raw.githubusercontent.com/hjnilsson/country-flags/master/png250px/'
FLAGS_SUFFIX = '.png'

def add_map(file_location, map_name=None, user_id=None):
    try:
        countries, _, breakdown = ts(file_location)
    except TypeError:
        return 1
    data = []
    date_created = datetime.utcnow()
    if not user_id:
        user_id = current_user.user_id

    if not map_name:
        map_name = request.form.get('name')

    if not map_name:
        map_name = str(date_created)[:19]

    if Polar.query.filter_by(user_id=user_id, map_name=map_name).first():
        flash("You've already used that map name!", "warning")
        return redirect("/createmap")

    for entry in breakdown:
        polar = Polar(user_id=user_id, country_code=entry[0],
                    start_time=entry[1], end_time=entry[2], map_name=map_name,
                    date_created=date_created)
        db.session.add(polar)
    db.session.commit()
    return 0

def allowed_file(filename):
    """
    obtained from http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
    """
    ALLOWED_EXTENSIONS = set(['zip'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def err(input=None, number=404):
    if not input:
        return render_template("error.html", message="I should probably make it...", code=str(number), loginform = LogInForm())
    else:
        return render_template("error.html", message=input, code=str(number), loginform = LogInForm())

package = Package('https://datahub.io/core/country-list/datapackage.json')

def get_country(code):
    '''
    Takes in a 2 letter ISO country code string and returns the country name
    If country code is invalid returns None
    '''
    if code == 'VA':
        return 'Vatican City'
    elif code == 'CZ':
        return 'Czechia'
    elif code == 'MK':
        return 'North Macedonia'

    list = package.resources[1].read()
    for entry in list:
        if entry[1] == code:
            return entry[0]
    return None

def get_code(country):
    '''
    Takes in a country name string and returns the 2 letter ISO country code
    If country name is spelt worng or invalid returns None
    '''
    list = package.resources[1].read()
    for entry in list:
        if entry[0] == country:
            return entry[1]
    return None

def get_flag_url(input):
    if type(input) != str:
        return None
    if len(input) != 2:
        input = get_code(input)

    return FLAGS_URL + input.lower() + FLAGS_SUFFIX

def get_map_data(user_id, map_name):
    data = []
    temp = {}
    map_data = Polar.query.filter_by(user_id=user_id, map_name=map_name)

    for entry in map_data:
        try:
            temp[entry.country_code] += (entry.end_time - entry.start_time)
        except KeyError:
            temp[entry.country_code] = (entry.end_time - entry.start_time)
    for country, value in temp.items():
        data.append({"id":country, "value":value})
    return data

def get_map_list():
    maps = Polar.query.filter_by(user_id=current_user.user_id
                ).group_by(Polar.map_name).order_by(Polar.date_created.desc()).all()
    list = []

    for map in maps:
        list.append(map.map_name)
    return list

def label_maker(data):
    for entry in data:
            entry['seconds_label'] = ": {:,} seconds".format(entry['value'])
            value = int(entry['value'])/3600
            entry['hours_label'] = ": {:,.0f} hours".format(value)
            value = value/24
            entry['days_label'] = ": {:,.1f} days".format(value)
            value = value/7
            entry['weeks_label'] = ": {:,.1f} weeks".format(value)
            # https://www.grc.nasa.gov/www/k-12/Numbers/Math/Mathematical_Thinking/calendar_calculations.htm
            value = int(entry['value'])/31556926
            entry['years_label'] = ": {:,.2f} years".format(value)
    return data

def save_file(file):
    filename = secure_filename(file.filename)
    file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_location)
    return file_location
