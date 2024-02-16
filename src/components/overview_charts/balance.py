import i18n
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ...data.source import DataSource
from ...data.loader import DataSchema

from .. import ids

from datetime import date

def render(app: Dash, source_expenses: DataSource, source_income: DataSource) -> html.Div:
    @app.callback(
        Output(ids.SHOW_BALANCE, "children"),
        [   
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_show_balance(_) -> html.Div:
        
        total_expenses = source_expenses.sum_expenses()
        total_income = source_income.sum_expenses()
        net_income = total_income - total_expenses

        # Determine color based on the comparison
        color_balance = 'red' if total_expenses >= total_income else 'green'

        return html.Div(style={'display': 'flex', 'flexDirection': 'row'},
                      children=[
                          html.Div(style={'flex': 1},
                                   children=[
                                        html.H4(i18n.t("general.current_balance") + f': ${total_expenses} / ${total_income}',
                                                style={'color': color_balance}),
                                        html.H4(i18n.t("general.net_income") + f': ${net_income}',
                                                style={'color': color_balance}),
                                        html.H4(i18n.t("general.expense_count") + f': {source_expenses.row_count}',
                                            style={'color': 'blue'}),
                                   ]),
                      ])


    return html.Div(id=ids.SHOW_BALANCE)