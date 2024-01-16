from executables.collectables.Collectable import Collectable


class Coin(Collectable):
    def __init__(self, r, pos, *sprite_groups):
        self.image = r.drawable("coin")
        super().__init__(r, pos, *sprite_groups)
