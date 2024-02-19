import i18n
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import (
    load_current_month_expenses, 
    load_transaction_data, 
    load_current_month_incoming,
    load_goals_data
    )
from src.data.source import DataSource
import const
from src.data.source_goals import DataSourceGoals


def main() -> None:

    i18n.set("locale", const.LOCALE)
    i18n.load_path.append("locale")
    i18n.set('file_format', 'json')

    datasets = {
        'transactions': DataSource(load_transaction_data()), 
        'month_expenses': DataSource(load_current_month_expenses()),
        'month_incoming': DataSource(load_current_month_incoming()),
        'goals': DataSourceGoals(load_goals_data())
        }


    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, datasets)
    app.run()


if __name__ == "__main__":
    main()
