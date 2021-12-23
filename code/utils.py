from dataclasses import dataclass
import pandas as pd

@dataclass
class Dateconvert:
    """Common utility functions for both central bank and ticker data"""

    indx: pd.DatetimeIndex

    def to_year_month(self):
        return self.indx.to_series().dt.strftime('%Y-%B').to_list()
