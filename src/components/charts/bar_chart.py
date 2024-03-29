import i18n
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ...data.loader import DataSchema
from ...data.source import DataSource
from .. import ids
from datetime import date

def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [   
            Input(ids.DATE_PICKER, "start_date"),
            Input(ids.DATE_PICKER, "end_date"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(
        start_date: date, end_date: date, categories: list[str]
    ) -> html.Div:
        filtered_source = source.filter(start_date=start_date, end_date=end_date, categories=categories)
        if not filtered_source.row_count:
            return html.Div(i18n.t("general.no_data"), id=ids.BAR_CHART)

        fig = px.bar(
            filtered_source.create_pivot_table(),
            x=DataSchema.CATEGORY,
            y=DataSchema.AMOUNT,
            color=DataSchema.CATEGORY,
            labels={
                "category": i18n.t("general.category"),
                "amount": i18n.t("general.amount"),
            },
            title=i18n.t("charts.bar-chart-title")
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
