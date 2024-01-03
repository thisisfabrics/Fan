import pygame.sprite


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, r, *sprite_groups):
        super().__init__(*sprite_groups)
        self.r = r
