import i18n
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ...data.source_goals import DataSourceGoals
import dash_bootstrap_components as dbc

from ...data.loader import GoalsSchema

from .. import ids

import plotly.graph_objs as go

from datetime import date, timedelta, datetime

import const

def render(app: Dash, source: DataSourceGoals) -> html.Div:
    @app.callback(
        Output(ids.SHOW_GOALS, "children"),
        [   
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_show_goals(_) -> html.Div:
        
        proress_df = source.get_progress_df()

        today = datetime.today()
        observation_message = i18n.t("general.goal_warning_message")

        return html.Div(# style={'display': 'flex', 'flexDirection': 'row'},
                        children=[
                            html.Div([
                            html.H3(title),
                            dbc.Progress(
                                id=f'progress-bar-{index}',
                                value=progress,
                                max=100,
                                style={'width': '80%'}
                            ),
                            html.Div(f'{amount} / {goal}: {progress:.2f} %'),
                            html.Div(
                                children=[html.H4('' if abs(today - last_updated).days <= const.DAYS_TRESHOLD_FOR_GOAL_WARNING else observation_message,
                                                  style={'color': 'red'})])
                        ]) for index, (title, amount, goal, last_updated, progress) in proress_df.iterrows()
                ])

    return html.Div(id=ids.SHOW_GOALS)