import pygame.sprite


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, r, pos=(0, 0), *sprite_groups):
        super().__init__(*sprite_groups)
        self.r = r
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.mask = pygame.mask.from_surface(self.image)
