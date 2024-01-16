from executables.collectables.Collectable import Collectable


class Battery(Collectable):
    def __init__(self, r, pos, *sprite_groups):
        self.image = r.drawable("battery")
        super().__init__(r, pos, *sprite_groups)
        self.value = 10
