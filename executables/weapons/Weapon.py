import pygame.sprite


class Weapon(pygame.sprite.Sprite):
    def __init__(self, r, pos):
        super().__init__()
        self.r = r
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect.x, self.rect.y = pos
