import pygame.draw

from executables.bullets.Air import Air
from executables.weapons.Weapon import Weapon


class Fan(Weapon):
    def __init__(self, r, pos):
        super().__init__(r, pos)
        self.bullet = Air
