from executables.entities.Enemy import Enemy


class Catterfield(Enemy):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(r, animation_name, animation_period, *sprite_groups)
