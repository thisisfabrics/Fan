from executables.collectables.Collectable import Collectable


class Powerup(Collectable):
    def __init__(self, r, pos, *sprite_groups):
        self.image = r.drawable("powerup")
        super().__init__(r, pos, sprite_groups)
        self.value = 1
