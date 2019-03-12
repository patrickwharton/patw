import base64
from flask_login import current_user
import io
from matplotlib import pyplot as plt
import pandas as pd
from patw import db
from patw.helpers import get_country
from patw.models import Polar, User
import seaborn as sns

def get_pandas_df():
    df = pd.read_sql_query(f'select * from polar where user_id = {current_user.user_id}', db.session.bind, parse_dates=['date_created'])
    return df

def time_spent_bar(df):
    img = io.BytesIO()
    '''
    Add in sum(time in country) group by country

    '''
    df['time_spent'] = df['end_time'] - df['start_time']
    
    df['country'] = df['country_code']
    sns.set_style('darkgrid')

    f, ax = plt.subplots(figsize=(12,7))
    ax = sns.barplot(x = 'country', y = 'time_spent', data = df, palette = 'bright')
    ax.set_title(f'Time {current_user.user_id} has spent on holiday per country')
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return 'data:image/png;base64,{}'.format(plot_url)

def time_spent_bar2():
    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    img = io.BytesIO()
    plt.plot(x, y)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)
