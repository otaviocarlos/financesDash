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
        Output(ids.BUBBLE_CHART, "children"),
        [   
            Input(ids.DATE_PICKER, "start_date"),
            Input(ids.DATE_PICKER, "end_date"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_bubble_chart(
        start_date: date, end_date: date, categories: list[str]
    ) -> html.Div:
        filtered_source = source.filter(start_date=start_date, end_date=end_date, categories=categories)
        if not filtered_source.row_count:
            return html.Div(i18n.t("general.no_data"), id=ids.BUBBLE_CHART)

        fig = px.scatter(filtered_source.get_columns([DataSchema.DATE, DataSchema.AMOUNT, DataSchema.CATEGORY]), x=DataSchema.DATE, y=DataSchema.AMOUNT, 
                 size=DataSchema.AMOUNT, # Sets the size of the bubbles
                 hover_name=DataSchema.DATE, # Shows the date when you hover over a bubble
                 color=DataSchema.CATEGORY,
                 title=i18n.t("charts.bubble-chart-title"))


        return html.Div(dcc.Graph(figure=fig), id=ids.BUBBLE_CHART)

    return html.Div(id=ids.BUBBLE_CHART)
