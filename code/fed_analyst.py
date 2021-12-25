import pandas as pd
from dataclasses import dataclass
from typing import List
import os

@dataclass
class FEDInterventions:
    """Class to analyze FED's asset purchase trends"""

    paths: List

    def _fed_preprocess(self):
        parse_dates=['DATE']
        fed_path = [path for path in self.paths if path == 'fed.csv']
        df = pd.read_csv(os.path.join('../data/',fed_path[0]),
                        sep=',',
                        index_col='DATE',
                        dtype={'DATE':'str','WALCL':'float'},
                        parse_dates=parse_dates)
        return df

    def get_fed_volume(self):
        fed_df = self._fed_preprocess()
        return fed_df.index, fed_df.WALCL

    def get_fed_pct(self):
        fed_df = self._fed_preprocess()
        fed_df['WALCL_pct'] = fed_df['WALCL'].pct_change()
        return fed_df.index, fed_df.WALCL_pct

    def get_fed_diff(self):
        fed_df = self._fed_preprocess()
        fed_df['WALCL_diff'] = fed_df['WALCL'].diff()
        return fed_df.index, fed_df.WALCL_diff

if __name__ == '__main__':
    FEDInterventions(['fed.csv']).get_fed_volume()
    FEDInterventions(['fed.csv']).get_fed_pct()
    FEDInterventions(['fed.csv']).get_fed_diff()
