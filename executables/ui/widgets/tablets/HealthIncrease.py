from executables.ui.widgets.tablets.Catalyst import Catalyst


class HealthIncrease(Catalyst):
    def __init__(self, r, pos, compos):
        self.image = r.drawable("catalyst_health_increase")
        super().__init__(r, pos, compos)
        self.description = self.r.string("catalyst_health_increase")
