import os

from stock import Stock

class Portfolio:
    def __init__(self, filename):
        self.filename = filename
        self.stocks = {}
        self.open_capital = 0.0
        self.open_gain = 0.0
        self.open_return = 0.0
        self.open_out = []
        self.close_capital = 0.0
        self.close_gain = 0.0
        self.close_return = 0.0
        self.close_out = []
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

    def displaySummary(self):
        print("Your Portforlio Summary is below:")
        print("=======================================================")
        self._formatStockResult(outstanding=False)
        print("=======================================================")
        self._formatStockResult(outstanding=True)
        print("=======================================================")
        #self._formatConclusion()
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
