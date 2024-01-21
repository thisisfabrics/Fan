import pygame.transform

from executables.bullets.Bullet import Bullet
from executables.entities.enemies.Catterfield import Catterfield


class Stream(Bullet):
    def __init__(self, r, start_pos, end_pos, source, *sprite_groups):
        super().__init__(r, start_pos, end_pos, *sprite_groups)
        self.source = source
        self.hitable_entities = (Catterfield,)
        if self.source.animation_is_flipped:
            self.image = pygame.transform.flip(self.r.drawable("arrows"), 1, 0)
            self.sign_multiplier = -1
        else:
            self.image = self.r.drawable("arrows")
            self.sign_multiplier = 1
        self.damage_rate = 10
        self.speed = 0.5 * self.r.constant("coefficient")
        self.rect = self.image.get_rect()
        self.max_lifetime = 200

    def update(self):
        if self.lifetime() > self.max_lifetime:
            self.kill()
            return
        self.x = self.start_pos[0] + self.lifetime() * self.speed * self.sign_multiplier
        self.y = self.source.rect.y
        self.rect.x, self.rect.y = self.x, self.y
        self.current_pos = self.x, self.y

