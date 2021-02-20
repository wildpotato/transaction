import os

from stock import Stock

class Portfolio:
    def __init__(self, filename):
        self.filename = filename
        self.stocks = {}
        self.returns = []
        self.total_capital_invested = 0.0
        self.total_asset = 0.0
        self.total_gain = 0.0
        self.total_return = 0.0

    def __repr__(self):
        return "%r" %self.stocks

    def parseRecords(self):
        with open(self.filename, "r") as in_fp:
            lines_of_transactions = in_fp.readlines()
            for line_t in lines_of_transactions:
                self._parseTransaction(line_t)
        in_fp.close()

    def calculateReturn(self):
        for _, stock in self.stocks.items():
            self.returns.append(stock.getReturn())

    def displaySummary(self):
        print("Your Portforlio Summary is below:")
        print("=======================================================")
        self._formatResults()
        print("=======================================================")
        self._formatConclusion()
        print("=======================================================")

    def _formatResults(self):
        print('{:^7}'.format("Ticker") + '{:^12}'.format("Gain/Loss") + '{:>8}'.format("Yield") + "%")
        for ret in self.returns:
            print('{:^7}'.format(ret[0]) + '{:>10.2f}'.format(ret[1]) + '{:>10.2f}'.format(ret[2] * 100) + "%")

    def _formatConclusion(self):
        self._calculateResult()
        print('{:^25}'.format("Total yield (%)") + '{:>9.2}'.format(self.total_return * 100) + "%")
        print('{:^25}'.format("Total gain/loss ($)") + '{:>10.2f}'.format(self.total_gain))
        print('{:^25}'.format("Total capital invested ($)") + '{:>10.2f}'.format(self.total_capital_invested))

    def _calculateResult(self):
        for stock in self.stocks.values():
            self.total_capital_invested += stock.capital_invested
            self.total_asset += stock.current_asset
        self.total_gain = self.total_asset - self.total_capital_invested
        self.total_return = self.total_gain / self.total_capital_invested

    def _parseTransaction(self, line_of_transaction):
        [date, action, ticker, price, volume] = line_of_transaction.split(' ')
        if ticker not in self.stocks:
            self.stocks[ticker] = Stock(ticker)
        self.stocks[ticker].addTransaction(date, action, price, volume)

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
