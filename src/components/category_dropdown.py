import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids
from .dropdown_helper import to_dropdown_options


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "value"),
        [   
            Input(ids.DATE_PICKER, "start_date"),
            Input(ids.DATE_PICKER, "end_date"),
            Input(ids.SELECT_ALL_CATEGORIES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_categories(start_date, end_date, _: int) -> list[str]:
        return source.filter(start_date=start_date, end_date=end_date).unique_categories

    return html.Div(
        children=[
            html.H6(i18n.t("general.category")),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN,
                options=to_dropdown_options(source.unique_categories),
                value=source.unique_categories,
                multi=True,
                placeholder=i18n.t("general.select"),
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.SELECT_ALL_CATEGORIES_BUTTON,
                n_clicks=0,
            ),
        ],
    )
