
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
