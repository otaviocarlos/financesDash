import i18n
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ...data.source import DataSource
from .. import ids

from datetime import date

def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.PIE_CHART, "children"),
        [   
            Input(ids.DATE_PICKER, "start_date"),
            Input(ids.DATE_PICKER, "end_date"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_pie_chart(
        start_date: date, end_date: date, categories: list[str]
    ) -> html.Div:
        filtered_source = source.filter(start_date=start_date, end_date=end_date, categories=categories)
        if not filtered_source.row_count:
            return html.Div(i18n.t("general.no_data"), id=ids.PIE_CHART)

        pie = go.Pie(
            labels=filtered_source.all_categories,
            values=filtered_source.all_amounts,
            hole=0.5,
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")

        return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)

    return html.Div(id=ids.PIE_CHART)
