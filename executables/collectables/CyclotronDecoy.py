from executables.collectables.Collectable import Collectable
from executables.weapons.Fan import Fan


class CyclotronDecoy(Collectable):
    def __init__(self, r, pos, *sprite_group):
        self.image = r.drawable("cyclotron")
        super().__init__(r, pos, *sprite_group)
        self.weapon = Fan(self.r, self.rect[:2], "cyclotron_idle", 200)
