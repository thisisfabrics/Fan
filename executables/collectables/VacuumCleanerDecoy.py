from executables.collectables.Collectable import Collectable
from executables.weapons.Fan import Fan


class VacuumCleanerDecoy(Collectable):
    def __init__(self, r, pos, *sprite_group):
        self.image = r.drawable("vacuumcleaner")
        super().__init__(r, pos, *sprite_group)
        self.weapon = Fan(self.r, self.rect[:2], "vacuumcleaner_idle", 200)
