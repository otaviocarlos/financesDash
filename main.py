import i18n
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import (
    load_current_month_expenses, 
    load_transaction_data, 
    load_current_month_incoming
    )
from src.data.source import DataSource
import const


def main() -> None:

    i18n.set("locale", const.LOCALE)
    i18n.load_path.append("locale")

    datasets = {
        'transactions': DataSource(load_transaction_data()), 
        'month_expenses': DataSource(load_current_month_expenses()),
        'month_incoming': DataSource(load_current_month_incoming()),
        }


    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, datasets)
    app.run()


if __name__ == "__main__":
    main()
