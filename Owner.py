class Owner:

    def __init__(self, diction, year):
        self._young = diction.get('y_amount')
        self._adult = diction.get('a_amount')
        self._old = diction.get('o_amount')
        self._young_cost = diction.get('young_cost')
        self._adult_cost = diction.get('adult_cost')
        self._old_cost = diction.get('old_cost')
        self._young_sell = diction.get('young_sell')
        self._adult_sell = diction.get('adult_sell')
        self._old_sell = diction.get('old_sell')
        self._cap = diction.get('capital')
        self._must_buyfood = diction.get('all_food')
        self._year = year
        self._penalty = diction.get('penalty')

    def check_penalty(self):
        _penalty = 0
        if self._young < self._young_sell:
            _penalty = penalty + (self._young_sell - self._young) * self._penalty
        if self._adult < self._adult_sell:
            _penalty = penalty + (self._adult_sell - self._adult) * self._penalty
        if self._old < self._old_sell:
            _penalty = penalty + (self._old_sell - self._old) * self._penalty
        return _penalty

    def sell(self):
        if self._year == 0:
            capit = (self._cap - self._must_buyfood +
                     self._young_cost * self._young_sell + self._adult_cost * self._adult_sell +
                     self._old_cost * self._old_sell)
        else:
            capit = (self._cap - self._must_buyfood - self.check_penalty() +
                     self._young * self._young_cost + self._adult * self._adult_cost +
                     self._old * self._old_cost +
                     self._young_cost * self._young_sell + self._adult_cost * self._adult_sell +
                     self._old_cost * self._old_sell)
        return capit

    def paying_capacity(self):
        _flag = False
        _capit = self.sell()
        if _capit < 0: 
            _flag = True
        return _flag
