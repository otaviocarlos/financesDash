from dash import Dash, html
from src.components import (
    category_dropdown,
    date_picker,
)
from src.components.charts import (
    bar_chart, 
    pie_chart,
    line_chart,
    heat_map,
    bubble_chart,
    tree_map,
    area_chart
)

from ..data.source import DataSource


def create_layout(app: Dash, source: DataSource) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    date_picker.render(app, source),
                    category_dropdown.render(app, source),
                ],
            ),
            pie_chart.render(app, source),
            tree_map.render(app, source),
            bar_chart.render(app, source),
            line_chart.render(app, source),
            heat_map.render(app, source),
            bubble_chart.render(app, source),
            area_chart.render(app, source),
        ],
    )
