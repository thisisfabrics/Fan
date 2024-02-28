import pygame.sprite


class Collectable(pygame.sprite.Sprite):
    def __init__(self, r, pos, *sprite_groups):
        super().__init__(*sprite_groups)
        self.r = r
        self.value = int()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def collect(self):
        self.r.sound("Powerup")
        self.kill()
        return self.value
