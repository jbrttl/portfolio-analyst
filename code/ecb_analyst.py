import pandas as pd
from dataclasses import dataclass
from typing import List
import os

@dataclass
class ECBInterventions:
    """Class to analyze ECB's key monetrary policy instruments"""

    paths: List

    def _prog_app_acronym(self,programme):
        programme = programme.replace('.',' ')
        return "".join(word[0].upper() for word in programme.split(' '))

    def _calc_app_netdiff(self,df):
        df['diff'] = ''
        for prog in df.programme_short.unique().tolist():
            indexes = df['programme_short'].isin([prog])
            df.loc[indexes,'diff'] = df.loc[indexes,'volume'].diff()
        return df

    def _app_preprocess(self):
        """Preprocess app df"""
        app_path = [path for path in self.paths if path.startswith('APP')]
        app = pd.read_csv(os.path.join('../data/',app_path[0]),header=2)
        app = app[:86].ffill().rename(columns={'Unnamed: 0':'Year','Unnamed: 1':'Month'})
        app['Date'] = app.Year + '-' + app.Month
        app.index = app.Date
        app = app.drop(columns=['Date','Year','Month'])
        app = app.stack().reset_index()
        app = app.set_index(app['Date']).drop(columns=['Date']).rename(columns={'level_1':'programme',0:'volume'})
        app_acronyms = pd.Series(map(self._prog_app_acronym,app['programme']),name='programme_short',index=app.index)
        app = pd.concat([app,app_acronyms],axis=1)
        return app

    def get_app_netdiff(self):
        app = self._app_preprocess()
        app = self._calc_app_netdiff(app)
        return app.index, app['diff'].values, app['programme_short'].values

    def get_app_volume(self):
        app = self._app_preprocess()
        return app.index, app['volume'].values, app['programme_short'].values

    def _omo_preprocess(self):
        """Preprocess omo df"""
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
                df['Type'] = 'OTH'
            omo_list.append(df)
        omo = pd.concat(omo_list)
        omo.index=omo.t_settlement_dt
        return omo

    def _calc_omo_pctchng(self, df):
        df['pct_chng'] = ''
        for prog in df.Type.unique().tolist():
            indexes = df['Type'].isin([prog])
            df.loc[indexes,'pct_chng'] = df.loc[indexes,'t_alloted_amount'].pct_change()
        return df

    def get_omo_trends(self):
        omo = self._omo_preprocess()
        return omo.index, omo.t_alloted_amount,omo.Type

    def get_omo_pctchng(self):
        omo = self._omo_preprocess()
        omo = self._calc_omo_pctchng(omo)
        return omo.index, omo.pct_chng, omo.Type




if __name__ == '__main__':
    ecb = ECBInterventions(['APP_breakdown_history.csv','tops_ltro.csv',
                       'tops_ot.csv','tops_mro.csv'])
    ecb.get_app_netdiff()
    ecb.get_app_volume()
    ecb.get_omo_trends()
    ecb.get_omo_pctchng()
