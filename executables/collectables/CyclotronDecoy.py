from executables.collectables.Collectable import Collectable
from executables.weapons.Cyclotron import Cyclotron


class CyclotronDecoy(Collectable):
    def __init__(self, r, pos, power=1, *sprite_group):
        self.image = r.drawable("cyclotron")
        super().__init__(r, pos, *sprite_group)
        self.value = [Cyclotron(self.r, self.rect[:2], "cyclotron_idle", 200, 1)]
