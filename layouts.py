from dash import dcc, html, dash_table
import functions as func
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash
import plotly.graph_objects as go
import json

layout1 = html.Div([
    html.H3('Page 1'),
    dcc.Dropdown(
        {f'Page 1 - {i}': f'{i}' for i in ['New York City', 'Montreal', 'Los Angeles']},
        id='page-1-dropdown'
    ),
    html.Div(id='page-1-display-value'),
    dcc.Link('Go to Page 2', href='/page2')
])

layout2 = html.Div([
    html.H3('Page 2'),
    dcc.Dropdown(
        {f'Page 2 - {i}': f'{i}' for i in ['London', 'Berlin', 'Paris']},
        id='page-2-dropdown'
    ),
    html.Div(id='page-2-display-value'),
    dcc.Link('Go to Page 1', href='/page1')
])


# Incorporate data
rosters_df = func.get_rosters()
schedule_df = func.get_schedules()


# App layout
home = [
    # html.H1('Home Page'),
    html.Div(className='row', children='Rosters',
             style={'textAlign': 'center', 'fontSize': 30}),

    html.Div(className='row', children=[
        html.Div(className='twelve columns', children=[
            dash_table.DataTable(data=rosters_df.to_dict('records'), page_size=20, style_table={'overflowX': 'auto'})
        ])]),
    html.Br(),
    html.Div(className='row', children='Schedules', style={'textAlign': 'center', 'fontSize': 30}),
    html.Div(className='row', children=[
        html.Div(className='twelve columns', children=[
            dash_table.DataTable(data=schedule_df.to_dict('records'), page_size=20, style_table={'overflowX': 'auto'})
        ])  
    ]),
    html.Br(),
    html.Br()
]


# rest_of_season = pd.read_csv('summary_sim.csv')
conn = func.connect_db()
rest_of_season = pd.read_sql('select * from summary_sim', conn)
rest_of_season.columns = ['week', 'player', 'rating', 'score', 'score_against', 'wins', 'outscore_league']
rest_of_season_sum = rest_of_season.groupby(['player']).agg({'rating': 'last', 'score': 'sum', 'score_against': 'sum', 'wins': 'sum', 'outscore_league': 'sum'}).reset_index().round(3)
# print(rest_of_season_sum[['player','score']])
# season_summary = pd.read_csv('simulated_season_summary.csv')
season_summary = pd.read_sql('select * from simulated_season_summary', conn)
rest_of_season_sum = rest_of_season_sum.merge(season_summary[['player','division_rank','overall_rank','playoffs']], on='player', how='left').sort_values(by=['playoffs', 'overall_rank', 'rating'], ascending=False).reset_index(drop=True).round(3)
rest_of_season_sum.columns = ['Teams', 'Proj Rating (logan)', 'Proj PF', 'Proj PA', 'Proj Wins', 'Proj League Wins', 'Proj Seed (div)', 'Proj Seed (overall)', 'Playoff %']
rest_of_season_sum['Playoff %'] = rest_of_season_sum['Playoff %'] / 100
# rest_of_season_sum = rest_of_season_sum.merge(season_summary_agg[['division_rank','overall_rank','playoffs']], on='player', how='left').sort_values(by=['playoffs'], ascending=False).reset_index(drop=True).round(3)
rest_of_season_sum['Proj Rating (logan)'] = round(rest_of_season_sum['Proj Rating (logan)'] / 14,3)

stats = func.get_stats()

# with open('ratings.json', 'r') as file:
#         ratings = json.load(file)
ratings = pd.read_sql('select player, rating from summary_weekly where week = (select max(week) from summary_weekly)', conn).to_dict('records')
ratings = {item['player']:item['rating'] for item in ratings}
current_ratings = pd.DataFrame({'Teams':ratings.keys(), 'Current Rating (logan)':ratings.values()}).round(3)
# weekly_stats = pd.read_csv('summary_weekly.csv')
weekly_stats = pd.read_sql('select * from summary_weekly', conn)
current_league_wins = weekly_stats[['player','outscore_league']].groupby(by='player').agg({'outscore_league':'sum'}).reset_index()
current_league_wins.columns = ['Teams', 'League Wins']
stats = stats.merge(current_ratings, on='Teams')#.sort_values(by=[''])
stats = stats.merge(current_league_wins, on='Teams').sort_values(by=['League Wins','Current Rating (logan)','Points For'], ascending=False)
stats['Current Rating (logan)'] = round(stats['Current Rating (logan)'] / 14, 3)


seeds = pd.read_sql('select * from simulated_season_seed', conn)
seeds.loc[:, seeds.columns != 'Teams'] = seeds.loc[:, seeds.columns != 'Teams'] / 100
seeds = seeds.to_dict('records')
# Define the desired order of columns
# column_order = ['Teams'] + [str(i) for i in range(1, 11)]

# Reorder the dictionaries according to the desired order
# seeds = [{k: d[k] for k in column_order} for d in seeds]


stats = [
    html.Div(className='row', children='Stats', style={'textAlign': 'center', 'fontSize': 30}),
    html.Div(className='row', children=[
        html.Div(className='centered-table', children=[
            dash_table.DataTable(data=stats.to_dict('records'), style_table={'overflowX': 'auto', 'margin-left':'auto', 'margin-right':'auto'}, sort_action='native')
            ])
    ]),
    # html.Div(className='four columns', children=[
    #         dcc.RadioItems(options=['Wins','Losses','Points For','Points Against','Acquisitions','Playoff Pct', 'Power Ranking'], value='Points For', id='stats-radio-item')
    # ]),
    # html.Div(className='row', children=[
    #     html.Div(className='eight columns', children=[
    #         dcc.Graph(figure={}, id='stats-graph')
    #     ])
    # ]),
    html.Br(),
    html.Div(className='row', children='Projected Stats', style={'textAlign': 'center', 'fontSize': 30}),
    html.Div(className='row', children=[
        html.Div(className='centered-table', children=[
            dash_table.DataTable(rest_of_season_sum.to_dict('records'), sort_action='native')
        ])
    ]),
    html.Br(),
    html.Div(className='row', children='Projected Seeding', style={'textAlign': 'center', 'fontSize': 30}),
    html.Div(className='row', children=[
        html.Div(className='centered-table', children=[
            dash_table.DataTable(seeds, sort_action='native')
        ])
    ]),
    html.Br(),
    html.Br()
]