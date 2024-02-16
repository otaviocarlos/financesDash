from dash import Dash, html
import i18n
from src.components import (
    category_dropdown,
    date_picker,
)
from src.components.charts import (
    bar_chart, 
    pie_chart,
    heat_map,
    bubble_chart,
    tree_map,
)

from src.components.overview_charts import (
    balance
)

from ..data.source import DataSource
from typing import List


def create_layout(app: Dash, sources: List[DataSource]) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="current-month-charts",
                # style={'display': 'flex', 'flexDirection': 'row'},
                children=[
                    html.H1(i18n.t("general.balance_title"), style={'color': 'black'}),
                    balance.render(app, sources['month_expenses'], sources['month_incoming'])
                ]
            ),
            html.Hr(),
            html.Div(
                className="filters",
                children=[
                    html.H1(i18n.t("general.expenses_charts"), style={'color': 'black'}),
                    date_picker.render(app, sources['transactions']),
                    category_dropdown.render(app, sources['transactions']),
                ],
            ),
            
            html.Div(
                className="expenses-charts",
                children=[
                    pie_chart.render(app, sources['transactions']),
                    tree_map.render(app, sources['transactions']),
                    bar_chart.render(app, sources['transactions']),
                    heat_map.render(app, sources['transactions']),
                    bubble_chart.render(app, sources['transactions']),
                ]
            ),
            html.Hr(),
        ],
    )
