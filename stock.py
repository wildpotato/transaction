import yfinance as yf

from transaction import Transaction

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.transactions = []
        self.current_price = 0.0
        self.open_capital_invested = 0.0
        self.open_market_value = 0.0
        self.open_accumulated_gain = 0.0
        self.open_position = 0
        self.open_return_rate = 0.0
        self.dividends_earned = 0.0
        self.close_capital_invested = 0.0
        self.close_accumulated_gain = 0.0
        self.close_return_rate = 0.0
        self.close_position = 0
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
        t = Transaction(date, action, price, volume, 0)
        self.transactions.append(t)
        if t.action == 'B':
            self._updateBuy(t)
        elif t.action == 'S':
            self._updateSell(t)
        elif t.action == 'D':
            self._updateDividend(t)
        else:
            raise RuntimeError('Illegal transaction type, only B/S/D allowed')

    def calculateReturn(self):
        self._getCurrentPrice()
        self._calculateCloseReturn()
        self._calculateOpenReturn()

    def returnOpen(self):
        if self.open_position > 0:
            return [self.ticker, self.open_position, self.open_accumulated_gain, self.open_return_rate]
        return None

    def returnClose(self):
        if self.close_position > 0:
            return [self.ticker, self.close_position, self.close_accumulated_gain, self.close_return_rate]
        return None

    def _updateBuy(self, new_trans):
        self.open_capital_invested += new_trans.price * new_trans.volume
        self.open_position += new_trans.volume

    def _updateSell(self, new_trans):
        shares_to_sell = new_trans.volume
        for i in range(len(self.transactions)):
            if self.transactions[i].action == 'B':
                if self.transactions[i].volume > self.transactions[i].volume_traded and shares_to_sell > 0:
                    shares_sold = 0
                    if self.transactions[i].volume - self.transactions[i].volume_traded >= shares_to_sell:
                        self.transactions[i].volume_traded += shares_to_sell
                        shares_sold = shares_to_sell
                        shares_to_sell = 0
                    else:
                        shares_to_sell -= self.transactions[i].volume - self.transactions[i].volume_traded
                        self.transactions[i].volume_traded = self.transactions[i].volume
                        shares_sold = self.transactions[i].volume - self.transactions[i].volume_traded
                    self.close_accumulated_gain += shares_sold * (new_trans.price - self.transactions[i].price)
                    self.close_capital_invested += shares_sold * self.transactions[i].price
                    self.close_position += shares_sold
                    self.open_position -= shares_sold
                    self.open_capital_invested -= shares_sold * self.transactions[i].price
                if shares_to_sell == 0:
                    break

    def _updateDividend(self, new_trans):
        self.dividends_earned += new_trans.price

    def _calculateCloseReturn(self):
        if self.close_capital_invested > 0:
            self.close_return_rate = self.close_accumulated_gain / self.close_capital_invested

    def _calculateOpenReturn(self):
        self.open_market_value += self.current_price * self.open_position
        self.open_accumulated_gain = self.open_market_value - self.open_capital_invested
        if self.open_capital_invested > 0:
            self.open_return_rate = self.open_accumulated_gain / self.open_capital_invested

    def _getCurrentPrice(self):
        self._getInfoFromYFinance()
        self.current_price = float(self.info.history().tail(1)['Close'].iloc[0])

    def _getInfoFromYFinance(self):
        try:
            self.info = yf.Ticker(self._ticker)
        except:
            RuntimeError('Cannot fetch stock info for "%s"', self._ticker)

