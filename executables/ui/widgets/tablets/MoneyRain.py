from executables.ui.widgets.tablets.Catalyst import Catalyst


class MoneyRain(Catalyst):
    def __init__(self, r):
        self.image = r.drawable("catalyst_money_rain")
        super().__init__(r)
        self.price = 1500
        self.description = self.r.string("catalyst_money_rain")
