import os

from stock import Stock

class Portfolio:
    def __init__(self, filename):
        self.filename = filename
        self.stocks = {}
        self.open_capital = 0.0
        self.open_market_value = 0.0
        self.open_return = 0.0
        self.open_out = []
        self.close_capital = 0.0
        self.close_gain = 0.0
        self.close_return = 0.0
        self.close_out = []
        self.total_dividends = 0.0
        self.total_capital = 0.0
        self.total_gain = 0.0
        self.total_return = 0.0
        #self.returns = []
        #self.total_capital_invested = 0.0
        #self.total_asset = 0.0
        #self.total_gain = 0.0
        #self.total_return = 0.0

    def __repr__(self):
        return "%r" %self.stocks.keys()

    def parseRecords(self):
        with open(self.filename, "r") as in_fp:
            lines_of_transactions = in_fp.readlines()
            for line_t in lines_of_transactions:
                self._parseTransaction(line_t)
        in_fp.close()

    def calculateStockReturn(self):
        for _, stock in self.stocks.items():
            stock.calculateReturn()
            if stock.returnOpen() is not None:
                self.open_out.append(stock.returnOpen())
            if stock.returnClose() is not None:
                self.close_out.append(stock.returnClose())
            self._updateOpenStats(stock)
            self._updateCloseStats(stock)
            self._updateTotalDividends(stock)
        self._calculateOpenAndCloseReturn()

    def displaySummary(self):
        print("Your Portforlio Summary is below:")
        print("=======================================================")
        self._formatStockResult(outstanding=False)
        self._formatOpenAndCloseReturn(outstanding=False)
        print("=======================================================")
        self._formatStockResult(outstanding=True)
        self._formatOpenAndCloseReturn(outstanding=True)
        print("=======================================================")

    def _formatStockResult(self, outstanding):
        if not outstanding:
            print('{:^45}'.format("[Profit Ended]"))
            output = self.close_out
        else:
            print('{:^45}'.format("[Outstanding]"))
            output = self.open_out
        print('{:^7}'.format("Ticker") + '{:>8}'.format("Shares") + '{:>14}'.format("Gain/Loss") +
              '{:>10}'.format("Yield") + "%")
        for ret in output:
            print('{:^7}'.format(ret[0]) + '{:>8}'.format(ret[1]) + '{:>14.2f}'.format(ret[2]) +
                  '{:>10.2f}'.format(ret[3] * 100) + "%")

    def _formatOpenAndCloseReturn(self, outstanding):
        capital = self.open_capital if outstanding else self.close_capital
        gain = self.open_market_value - self.open_capital if outstanding else self.close_gain
        return_rate = self.open_return if outstanding else self.close_return
        print('{:^25}'.format("Capital invested ($)") + '{:>10.2f}'.format(capital))
        print('{:^25}'.format("Gain/loss ($)") + '{:>10.2f}'.format(gain))
        print('{:^25}'.format("Return rate (%)") + '{:>9.2f}'.format(return_rate * 100) + "%")

    def _parseTransaction(self, line_of_transaction):
        [date, action, ticker, price, volume] = line_of_transaction.split(' ')
        if ticker not in self.stocks:
            self.stocks[ticker] = Stock(ticker)
        self.stocks[ticker].addTransaction(date, action, price, volume)

    def _updateOpenStats(self, stock):
        self.open_capital += stock.open_capital_invested
        self.open_market_value += stock.open_market_value

    def _updateCloseStats(self, stock):
        self.close_capital += stock.close_capital_invested
        self.close_gain += stock.close_accumulated_gain

    def _updateTotalDividends(self, stock):
        self.total_dividends += stock.dividends_earned

    def _calculateOpenAndCloseReturn(self):
        if self.open_capital > 0:
            self.open_return = (self.open_market_value - self.open_capital) / self.open_capital
        if self.close_capital > 0:
            self.close_return = self.close_gain / self.close_capital

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        if not isinstance(filename, str):
            raise TypeError('Expected a string')
        if not os.path.exists(os.path.join(os.getcwd(), filename)):
            raise ValueError('Record not found in current directory')
        self._filename = filename
