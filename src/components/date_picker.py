import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids
from .dropdown_helper import to_dropdown_options
from datetime import date, datetime, timedelta

TIME_DELTA_DAYS = 300

def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.DATE_PICKER, "children"),
        [
            Input(ids.DATE_PICKER, "start_date"),
            Input(ids.DATE_PICKER, "end_date"),
        ],
    )
    def update_output(start_date: date, end_date: date) -> list[str]:
        return ''
        

    return html.Div(
        children=[
            html.H6(i18n.t("general.date_picker")),
            dcc.DatePickerRange(
                id=ids.DATE_PICKER,
                min_date_allowed=date(2014, 1, 1),
                max_date_allowed=datetime.today(),
                start_date=(datetime.today() - timedelta(days=TIME_DELTA_DAYS)).replace(day=1),
                end_date=datetime.today(),
                display_format = 'YYYY/MM/DD'
            )
        ],
    )
