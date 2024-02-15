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
        Output(ids.LINE_CHART, "children"),
        [   
            Input(ids.DATE_PICKER, "start_date"),
            Input(ids.DATE_PICKER, "end_date"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_line_chart(
        start_date: date, end_date: date, categories: list[str]
    ) -> html.Div:
        filtered_source = source.filter(start_date=start_date, end_date=end_date, categories=categories)
        if not filtered_source.row_count:
            return html.Div(i18n.t("general.no_data"), id=ids.LINE_CHART)
        
        grouped_df = filtered_source.group_data([DataSchema.CATEGORY, DataSchema.MONTH])

        grouped_df = grouped_df.sort_values(by=DataSchema.MONTH)
      
        fig = px.line(grouped_df, x=DataSchema.MONTH, y=DataSchema.AMOUNT, color=DataSchema.CATEGORY, title=i18n.t("charts.line-chart-title"))

        return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART)

    return html.Div(id=ids.LINE_CHART)
