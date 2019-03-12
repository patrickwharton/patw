import base64
from flask_login import current_user
import io
from matplotlib import pyplot as plt
import pandas as pd
from patw import db
from patw.helpers import get_country, get_map_list
from patw.models import Polar, User
import seaborn as sns
import sys

def get_pandas_df(username=None):
    if not username:
        df = pd.read_sql_query(f'select * from polar where user_id = {current_user.user_id}', db.session.bind, parse_dates=['date_created'])
    else:
        user_id = User.query.filter_by(username=username).first().user_id
        df = pd.read_sql_query(f'select * from polar where user_id = {user_id}', db.session.bind, parse_dates=['date_created'])
    return df

def time_spent_bar(df, current_map=None, username=None):
    img = io.BytesIO()
    '''
    Add in sum(time in country) group by country

    '''
    if not current_map:
        map_list = get_map_list()
        current_map = map_list[0]
    # Removes values from other maps
    df = df[df.map_name == current_map]

    # Calculate total time spent
    df['time_spent'] = (df['end_time'] - df['start_time']) / 86400
    df = df.groupby(['country_code']).time_spent.sum().reset_index()

    # Change codes to name and sort
    df['country'] = df['country_code'].apply(get_country)
    df = df.sort_values(by=['time_spent', 'country'], ascending=[False, True])

    sns.set_style('darkgrid')
    sns.set_context("paper")

    ax = sns.barplot(x = 'country', y = 'time_spent', data = df, palette = 'bright')
    if username == 'padmin':
        username = 'Patrick'
    elif not username:
        username = User.get_username(current_user)
    ax.set_title(f'Time {username} has spent on holiday per country')
    ax.set_ylabel("Time Spent (Days)")
    ax.set_xlabel("Country")
    for item in ax.get_xticklabels():
        item.set_rotation(90)
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0.5)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return 'data:image/png;base64,{}'.format(plot_url)
