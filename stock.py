#!/usr/bin/python3

import yfinance as yf
import argparse
import os
import pprint

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--record", help="record that contains your transaction history")
    parser.add_argument("-s", "--start_timestamp", help="starting time")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-d", "--duration", type=int, help="duration after starting time")
    parser.add_argument("-v", "--verbosity_level", default=0, help="verbosity level: 0 is off")
    return parser

class Transaction:
    def __init__(self, date, action, price, volume):
        self.date = date
        self.action = action
        self.price = price
        self.volume = volume

    def __repr__(self):
        return "%r %r %r %r" %(self._date, self._action, self._price, self._volume)

    @property
    def amount(self):
        if self._action == 'B' or self._action == 'S':
            return self._price * self._volume
        elif self._action == 'D':
            return self._price
        else:
            raise RuntimeError('Invalid transaction type')

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if not isinstance(date, str):
            raise TypeError('Expected a string, get %s' %type(date))
        if not len(date) == 8:
            raise ValueError('Date must be YYYYMMDD')
        self._date = int(date)

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        if not isinstance(action, str):
            raise TypeError('Expected a string')
        if action not in ['B', 'S', 'D']:
            raise ValueError('Expected "B", "S", or "D"')
        self._action = action

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        try:
            self._price = float(price)
        except:
            raise TypeError('Expected a float')

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        if not isinstance(volume, str):
            raise TypeError('Expected a string')
        volume = volume.strip()
        if not volume.isnumeric():
            raise ValueError('Expected an integer, get "%s"' %volume)
        self._volume = int(volume)

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


def main():
    p = Portfolio("record")
    p.parseRecords()
    p.calculateReturn()
    p.displaySummary()

if __name__ == "__main__":
    main()
