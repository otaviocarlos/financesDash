from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from .loader import GoalsSchema

from datetime import date



@dataclass
class DataSourceGoals:
    _data: pd.DataFrame

    def get_progress_df(self) -> pd.DataFrame:
        self._data['progress'] = (self._data[GoalsSchema.AMOUNT] / self._data[GoalsSchema.GOAL]) * 100
        return self._data