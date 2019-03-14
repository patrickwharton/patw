# Makes plt.close() behave when you don't render a plot
# https://matplotlib.org/faq/howto_faq.html#matplotlib-in-a-web-application-server
import matplotlib
matplotlib.use('Agg')

import base64
from datetime import datetime
from flask_login import current_user
import io
from matplotlib import pyplot as plt
import pandas as pd
from patw import db, app
from patw.helpers import get_country, get_map_list
from patw.models import Polar, User
import plotly.plotly as py
import plotly.figure_factory as ff
import seaborn as sns
import sys

def get_single_map_df(username, current_map):
    user_id = User.query.filter_by(username=username).first().user_id
    df = pd.read_sql_query(f'select * from polar where user_id = {user_id} and map_name = "{current_map}"', db.session.bind, parse_dates=['date_created'])
    return df

def continents_pie(current_map=None, username=None):
    if not current_map:
        map_list = get_map_list()
        current_map = map_list[0]

    if username == 'padmin':
        name = 'Patrick'
    elif not username:
        username = name = User.get_username(current_user)

    df = get_single_map_df(username=username, current_map=current_map)

    df_all = pd.read_csv(app.root_path + '/static/all.csv')
    df_all = df_all[['alpha-2', 'region']]
    df = pd.merge(df, df_all, left_on='country_code', right_on='alpha-2', how='left').reset_index()

    df['time_spent'] = (df['end_time'] - df['start_time']) / 86400
    df['region'][df['region'].isnull()] = 'Antarctica'

    df = df.groupby(['region']).time_spent.sum().reset_index()
    df['explode'] = 0

    fig1, ax1 = plt.subplots()
    ax1.pie(df['time_spent'], labels=df['region'], autopct='%1.1f%%',\
                shadow=False, pctdistance=0.58, startangle=0, \
                explode=df['explode'], wedgeprops={"edgecolor":"k",'linewidth': \
                1.25, 'linestyle': 'solid', 'antialiased': True})

    centre_circle = plt.Circle((0,0),0.70,color='black',fc='white',linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    ax1.axis('equal')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    plt.clf()
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return 'data:image/png;base64,{}'.format(plot_url)

def time_spent_bar(current_map=None, username=None):
    if not current_map:
        map_list = get_map_list()
        current_map = map_list[0]

    if username == 'padmin':
        name = 'Patrick'
    elif not username:
        username = name = User.get_username(current_user)

    df = get_single_map_df(username=username, current_map=current_map)

    # Calculate total time spent
    df['time_spent'] = (df['end_time'] - df['start_time']) / 86400
    df = df.groupby(['country_code']).time_spent.sum().reset_index()

    # Change codes to name and sort
    df['country'] = df['country_code'].apply(get_country)
    df = df.sort_values(by=['time_spent', 'country'], ascending=[False, True])

    sns.set_style('darkgrid')
    sns.set_context("paper")

    ax = sns.barplot(x = 'country', y = 'time_spent', data = df, palette = 'bright')

    ax.set_title(f'Time {name} has spent on holiday per country')
    ax.set_ylabel("Time Spent (Days)")
    ax.set_xlabel("Country")
    for item in ax.get_xticklabels():
        item.set_rotation(90)
        item.set_ha('center')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    plt.clf()
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return 'data:image/png;base64,{}'.format(plot_url)
