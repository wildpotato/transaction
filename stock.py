import yfinance as yf

from transaction import Transaction

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.transactions = []
        self.current_price = 0.0
        self.current_asset = 0.0
        self.capital_invested = 0.0
        self.accumulated_gain = 0.0
        self.dividends_earned = 0.0
        self.position = 0
        self.total_gain = 0

    def __repr__(self):
        return "%r" %self.ticker

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, ticker):
        if not isinstance(ticker, str):
            raise TypeError('Expected a string')
        if len(ticker) > 5:
            raise ValueError('Ticker too long, limit is 5 characters')
        self._ticker = ticker

    def addTransaction(self, date, action, price, volume):
        t = Transaction(date, action, price, volume)
        self.transactions.append(t)
        if t.action == 'B':
            self.capital_invested += t.price * t.volume
            self.position += t.volume
        elif t.action == 'S':
            self.accumulated_gain += t.price * t.volume
            self.position -= t.volume
        elif t.action == 'D':
            self.dividends_earned += t.price
        else:
            raise RuntimeError('Illegal transaction type')

    def getReturn(self):
        self._calculateReturn()
        return [self.ticker, self.total_gain, self.total_return]

    def _calculateReturn(self):
        self._getCurrentPrice()
        self.current_asset = self.position * self.current_price + self.dividends_earned
        self.total_gain = self.accumulated_gain - self.capital_invested + self.current_asset
        self.total_return = self.total_gain / self.capital_invested

    def _getCurrentPrice(self):
        self._getInfoFromYFinance()
        self.current_price = float(self.info.history().tail(1)['Close'].iloc[0])

    def _getInfoFromYFinance(self):
        try:
            self.info = yf.Ticker(self._ticker)
        except:
            RuntimeError('Can not fetch stock info for "%s"', self._ticker)

