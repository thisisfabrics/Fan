from executables.ui.widgets.tablets.Catalyst import Catalyst


class EnergyTransaction(Catalyst):
    def __init__(self, r):
        self.image = r.drawable("catalyst_energy_transaction")
        super().__init__(r)
        self.price = 1000
        self.description = self.r.string("catalyst_energy_transaction")
