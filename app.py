from dash import Dash, dcc, html, Input, Output, callback

from layouts import layout1, layout2, home, stats
# import callbacks
import functions as func

def create_dash_app(server):
    app = Dash(__name__, suppress_callback_exceptions=True, server=server)

    league = func.connect()
    pages = [{'name': team.owners[0]['firstName'], 'fantasy_name': team.team_name, 'path':'/'+team.team_name} for team in league.teams]
    pages = [{'name':'Home', 'fantasy_name': '', 'path':'/'}, {'name':'Stats', 'fantasy_name':'', 'path':'/stats'}] + pages
    paths = ['/'+team.team_name.replace(' ','') for team in league.teams]

    app.layout = html.Div([
        html.Nav([
            html.Ul([
                html.Li(
                    dcc.Link(f"{page['name']}", href=page["path"])
                ) for page in pages
            ], className='navbar')
        ]),
        dcc.Location(id='url', refresh=False),  # Ensure this is always in the layout
        html.Div(id='page-content')
    ])


    @callback(Output('page-content', 'children'),
            Input('url', 'pathname'))
    def display_page(pathname):
        print(paths)
        # print(pathname.replace('%20', ' '))
        if pathname == '/page1':
            return layout1
        elif pathname == '/page2':
            return layout2
        elif pathname == '/':
            return home
        elif pathname.replace('%20', ' ').replace(' ', '') in paths:
            print(pathname[1:].replace('%20', ' ').replace(' ', ''))
            return func.team_dash_layout(fantasy_name=pathname[1:].replace('%20', ' ').replace(' ', ''))
        elif pathname == '/stats':
            return stats
        else:
            return '404'
    return app


if __name__ == '__main__':
    from flask import Flask
    server = Flask(__name__)
    app = create_dash_app(server)
    app.run_server(debug=True)