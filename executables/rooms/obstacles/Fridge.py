import pygame.mask

from executables.rooms.obstacles.Obstacle import Obstacle


class Fridge(Obstacle):
    def __init__(self, r, pos=(0, 0), *sprite_groups):
        super().__init__(r, *sprite_groups)
        self.image = self.r.drawable("fridge")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.mask = pygame.mask.from_surface(self.image)
