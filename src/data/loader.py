import datetime as dt
from functools import partial, reduce
from typing import Callable

import babel.dates
import i18n
import pandas as pd

from google_sheets import Sheets

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]

import const 

sheet = Sheets()

class DataSchema:
    DATE = 'date'
    CATEGORY = "category"
    TITLE = 'title'
    AMOUNT = "amount"
    TYPE = "type"
    ACCOUNT = "account"
    YEAR = 'year'
    MONTH = 'month'


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(str)
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.MONTH] = df[DataSchema.DATE].dt.month.astype(str)
    return df


def convert_date_locale(df: pd.DataFrame, locale: str) -> pd.DataFrame:
    def date_repr(date: dt.date) -> str:
        return babel.dates.format_date(date, format="MMMM", locale=locale)

    df[DataSchema.MONTH] = df[DataSchema.DATE].apply(date_repr)
    return df


def translate_category_language(df: pd.DataFrame) -> pd.DataFrame:
    def translate(category: str) -> str:
        return i18n.t(f"category.{category}")

    df[DataSchema.CATEGORY] = df[DataSchema.CATEGORY].apply(translate)
    return df

def remove_categories_from_ban_list(df: pd.DataFrame) -> pd.DataFrame:
    ban_list = [cat for cat in df[DataSchema.CATEGORY].unique() if '_' in cat]
    ban_list += ['payment', 'financing', 'charge']

    return df[~df[DataSchema.CATEGORY].isin(ban_list)].reset_index(drop=True)

def filter_date_for_this_month(df: pd.DataFrame) -> Preprocessor:
    month_first_day = dt.datetime.now().replace(day=1)
    current_date = dt.datetime.now()

    return df.query(" date >= @month_first_day and date <= @current_date ").reset_index(drop=True)

def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)

def load_transaction_data() -> pd.DataFrame:
    data = sheet.get_sheet_by_name(const.EXPENSES_SHEET)
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date')
    

    preprocessor = compose(
        create_year_column,
        create_month_column,
        partial(convert_date_locale, locale=const.LOCALE),
        remove_categories_from_ban_list
    )
    return preprocessor(data)

def load_current_month_expenses() -> pd.DataFrame:
    data = sheet.get_sheet_by_name(const.EXPENSES_SHEET)
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date')

    preprocessor = compose(
        filter_date_for_this_month,
        remove_categories_from_ban_list
    )
    return preprocessor(data)

def load_current_month_incoming() -> pd.DataFrame:
    data = sheet.get_sheet_by_name(const.INCOMING_SHEET)
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date')

    preprocessor = compose(
        filter_date_for_this_month,
        remove_categories_from_ban_list
    )
    return preprocessor(data)