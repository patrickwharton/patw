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

def continents_gantt(current_map=None, username=None):
    img = io.BytesIO()

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

    # df['time_spent'] = (df['end_time'] - df['start_time']) / 86400
    df['region'][df['region'].isnull()] = 'Antarctica'
    df.rename(index=str, columns={'region':'Task'})
    df['Start'] = df['start_time'].apply(datetime.utcfromtimestamp)
    df['Finish'] = df['end_time'].apply(datetime.utcfromtimestamp)
    df['Start'] = df['Start'].apply(datetime.date)
    df['Finish'] = df['Finish'].apply(datetime.date)
    df['country'] = df['country_code'].apply(get_country)

    print(df.head(), file=sys.stderr)
    #df = df.groupby(['region']).time_spent.sum().reset_index()
    fig = ff.create_gantt(df, index_col='country',
                      showgrid_x=True, showgrid_y=True)
    py.iplot(fig, filename='cont_gantt', world_readable=True)


    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return 'data:image/png;base64,{}'.format(plot_url)

def time_spent_bar(current_map=None, username=None):
    img = io.BytesIO()

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
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0.5)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return 'data:image/png;base64,{}'.format(plot_url)
