from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from ..data.loader import DataSchema
from .loader import DataSchema
from datetime import date

@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter(
        self,
        start_date: date,
        end_date: date,
        categories: Optional[list[str]] = None,
    ) -> DataSource:

        if categories is None:
            categories = self.unique_categories
        filtered_data = self._data.query(
            " date >= @start_date and date <= @end_date and category in @categories"
        )
        
        return DataSource(filtered_data)
    
    def select_date_range(self, start_date, end_date) -> pd.DataFrame:
        # filtered_data = self._data.query(
        #     " category == 'casa' "
        # )

        return DataSource(self._data)


    def create_pivot_table(self) -> pd.DataFrame:
        pt = self._data.pivot_table(
            values=DataSchema.AMOUNT,
            index=[DataSchema.CATEGORY],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        )
        return pt.reset_index().sort_values(DataSchema.AMOUNT, ascending=False)
    
    def group_data(self, columns: list) -> pd.DataFrame:

        columns_to_group = columns
        columns_to_filter = columns + [DataSchema.AMOUNT] 

        return self._data[columns_to_filter].groupby(columns_to_group).sum().reset_index()
    
    def get_columns(self, columns: list) -> pd.DataFrame:
        return self._data[columns]

    @property
    def row_count(self) -> int:
        return self._data.shape[0]

    @property
    def all_years(self) -> list[str]:
        return self._data[DataSchema.YEAR].tolist()

    @property
    def all_months(self) -> list[str]:
        return self._data[DataSchema.MONTH].tolist()

    @property
    def all_categories(self) -> list[str]:
        return self._data[DataSchema.CATEGORY].tolist()

    @property
    def all_amounts(self) -> list[str]:
        return self._data[DataSchema.AMOUNT].tolist()

    @property
    def unique_years(self) -> list[str]:
        return sorted(set(self.all_years), key=int)

    @property
    def unique_months(self) -> list[str]:
        return sorted(set(self.all_months))

    @property
    def unique_categories(self) -> list[str]:
        return sorted(set(self.all_categories))
