import i18n
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ...data.source import DataSource
from ...data.loader import DataSchema

from .. import ids

from datetime import date


def render(app: Dash, source: DataSource) -> html.Div:
    # BUG: it should add the year to the month vizualization, so that two months of different years wont be overlaped
    @app.callback(
        Output(ids.HEAT_MAP, "children"),
        [   
            Input(ids.DATE_PICKER, "start_date"),
            Input(ids.DATE_PICKER, "end_date"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_heat_map(
        start_date: date, end_date: date, categories: list[str]
    ) -> html.Div:
        filtered_source = source.filter(start_date=start_date, end_date=end_date, categories=categories)
        if not filtered_source.row_count:
            return html.Div(i18n.t("general.no_data"), id=ids.HEAT_MAP)
        
        grouped_df = filtered_source.group_data([DataSchema.CATEGORY, DataSchema.MONTH])

        heatmap_data = grouped_df.pivot(index=DataSchema.CATEGORY, columns=DataSchema.MONTH, values=DataSchema.AMOUNT)

        fig = px.imshow(heatmap_data, 
                labels=dict(x=DataSchema.MONTH, y=DataSchema.CATEGORY, color=DataSchema.AMOUNT),
                x=heatmap_data.columns,
                y=heatmap_data.index, 
                title=i18n.t("charts.heat-map-title"))
        


        return html.Div(dcc.Graph(figure=fig), id=ids.HEAT_MAP)

    return html.Div(id=ids.HEAT_MAP)
