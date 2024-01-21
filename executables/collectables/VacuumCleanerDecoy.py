from executables.collectables.Collectable import Collectable
from executables.weapons.VacuumCleaner import VacuumCleaner


class VacuumCleanerDecoy(Collectable):
    def __init__(self, r, pos, *sprite_group):
        self.image = r.drawable("vacuumcleaner")
        super().__init__(r, pos, *sprite_group)
        self.value = [VacuumCleaner(self.r, self.rect[:2], "vacuumcleaner_idle", 200)]
