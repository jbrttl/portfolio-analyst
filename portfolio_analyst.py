import yfinance as y
import pandas as pd

class TickerAnalyst(y.Ticker):
    """Simple class to collect price information for given tickers from Yahoo finance"""
    def __init__(self,ticker,multi_ticker=False):
        self.multitick = multi_ticker

        if multi_ticker == False:
            self.ticker = y.Ticker(ticker)
            self.history = pd.DataFrame(self.ticker.history(period='max')['Close'])
        elif multi_ticker == True:
            self.ticker = y.Tickers(ticker)
            self.history = pd.DataFrame(self.ticker.history(period='max')['Close'])

    def get_history(self):
        """Get hisotrical prices for a given ticker."""
        return self.history

    def get_info(self):
        """Get info on ticker."""
        return self.ticker.info

    def get_returns(self,freq='d'):
        """Calculate cummulative and periodic (daily/monthly) returns."""
        self.rets = self.history

        returns_df = pd.DataFrame([])
        returns_df.index = self.rets.index

        for col in self.rets.columns:
            if freq == 'd':
                returns_df[f'{col}_daily_ret'] = self.rets[col].pct_change()
                returns_df[f'{col}_cumul'] = ((returns_df[f'{col}_daily_ret'] + 1)).cumprod()
                return returns_df
            elif freq == 'm':
                returns_df[f'{col}_monthly_ret'] = self.rets[col].resample('M').ffill().pct_change()
                returns_df[f'{col}_cumul'] = ((returns_df[f'{col}_monthly_ret'] + 1)).cumprod()
                return returns_df

    def get_sma(self,freq=150):
        """Calculates simple moving average for a specified frequency."""
        self.sma = self.history

        sma_df = pd.DataFrame([])
        sma_df.index = self.sma.index

        for col in self.sma.columns:
            sma_df[f'{col}_sma_{freq}'] = self.sma[col].rolling(freq,min_periods=1).mean()
        return sma_df

    def get_ewm(self,alpha=0.05):
        """Calculates exponential moving average for a given alpha."""
        self.ewm = self.history

        ewm_df = pd.DataFrame([])
        ewm_df.index = self.ewm.index

        for col in self.ewm.columns:
            ewm_df[f'{col}_ewm'] = self.ewm[col].ewm(alpha=alpha,adjust=False).mean()
        return ewm_df

    def __repr__(self):
        if self.multitick == False:
            return (f'{self.__class__.__name__}'
                    f'(Ticker={self.ticker.ticker!r}, Multitick={self.multitick!r})')
        else:
            return (f'{self.__class__.__name__}'
                    f'(Tickers={self.ticker.tickers!r}, Multitick={self.multitick!r})')

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        if self.multitick == False:
            return (self.ticker.ticker, self.multitick) == (other.ticker.ticker, other.multitick)
        else:
            return (self.ticker.tickers, self.multitick) == (other.ticker.tickers, other.multitick)


if __name__ == '__main__':
    etf = Etf("BTC-USD",multi_ticker=False)
    etf.get_history()
    etf.get_returns()
    etf.get_sma()
    etf.get_ewm()
