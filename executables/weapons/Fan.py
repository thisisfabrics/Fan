import pygame.draw

from executables.bullets.Air import Air
from executables.weapons.Weapon import Weapon


class Fan(Weapon):
    def __init__(self, r, pos, animation_name, animation_period):
        super().__init__(r, pos, animation_name, animation_period)
        self.bullet = Air
        self.offset_not_flipped = -30 * self.r.constant("coefficient"), 296.788 * self.r.constant("coefficient")
        self.offset_flipped = 71.428 * self.r.constant("coefficient"), self.offset_not_flipped[1]
        self.apply_offset()
