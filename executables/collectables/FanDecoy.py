from executables.collectables.Collectable import Collectable
from executables.weapons.Fan import Fan


class FanDecoy(Collectable):
    def __init__(self, r, pos, power=1, *sprite_group):
        self.image = r.drawable("fan")
        super().__init__(r, pos, *sprite_group)
        self.value = [Fan(self.r, self.rect[:2], "fan_idle", 200, 1)]

