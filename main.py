import i18n
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import load_transaction_data
from src.data.source import DataSource
import const


def main() -> None:

    i18n.set("locale", const.LOCALE)
    i18n.load_path.append("locale")

    data = load_transaction_data()
    data = DataSource(data)

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, data)
    app.run()


if __name__ == "__main__":
    main()
