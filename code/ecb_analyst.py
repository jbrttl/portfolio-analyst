import pandas as pd
from dataclasses import dataclass
from typing import List
import os

@dataclass
class ECBInterventions:
    """Class to analyze ECB's key monetrary policy instruments"""

    paths: List

    def prog_app_acronym(self,programme):
        programme = programme.replace('.',' ')
        return "".join(word[0].upper() for word in programme.split(' '))

    def calc_app_change(self,df):
        df['diff'] = ''
        for prog in df.programme_short.unique().tolist():
            indexes = df['programme_short'].isin([prog])
            df.loc[indexes,'diff'] = df.loc[indexes,'volume'].diff()
        return df

    def asset_purchase(self):
        app_path = [path for path in self.paths if path.startswith('APP')]
        app = pd.read_csv(os.path.join('../data/',app_path[0]),header=2)
        app = app[:86].ffill().rename(columns={'Unnamed: 0':'Year','Unnamed: 1':'Month'})
        app['Date'] = app.Year + '-' + app.Month
        app.index = app.Date
        app = app.drop(columns=['Date','Year','Month'])
        app = app.stack().reset_index()
        app = app.set_index(app['Date']).drop(columns=['Date']).rename(columns={'level_1':'programme',0:'volume'})
        app_acronyms = pd.Series(map(self.prog_app_acronym,app['programme']),name='programme_short',index=app.index)
        app = pd.concat([app,app_acronyms],axis=1)
        app = self.calc_app_change(app)
        return app.index, app['diff'].values, app['programme_short'].values

    def open_market_operations(self):
        omo_path = [path for path in self.paths if path.startswith('tops')]
        omo_list = list()
        for path in omo_path:
            df = pd.read_csv(os.path.join('../data/',path))
            df['Type'] = ''
            if '_ltro' in path:
                df['Type'] = 'LTRO'
            elif '_ot' in path:
                df['Type'] = 'OT'
            elif '_mro' in path:
                df['Type'] = 'MRO'
            else:
                pass
            omo_list.append(df)
        omo = pd.concat(omo_list)
        omo.index=omo.t_settlement_dt
        return omo.index, omo.t_alloted_amount,omo.Type
