import i18n
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ...data.source import DataSource
from ...data.loader import DataSchema

from .. import ids

from datetime import date


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.TREE_MAP, "children"),
        [   
            Input(ids.DATE_PICKER, "start_date"),
            Input(ids.DATE_PICKER, "end_date"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_tree_map(
        start_date: date, end_date: date, categories: list[str]
    ) -> html.Div:
        filtered_source = source.filter(start_date=start_date, end_date=end_date, categories=categories)
        if not filtered_source.row_count:
            return html.Div(i18n.t("general.no_data"), id=ids.TREE_MAP)

        fig = px.treemap(filtered_source.get_columns([DataSchema.AMOUNT, DataSchema.CATEGORY, DataSchema.TITLE]), 
                path=[DataSchema.CATEGORY, DataSchema.TITLE],
                values=DataSchema.AMOUNT,
                title=i18n.t("charts.tree-map-title"))


        return html.Div(dcc.Graph(figure=fig), id=ids.TREE_MAP)

    return html.Div(id=ids.TREE_MAP)
