import math

from executables.bullets.Bullet import Bullet
from executables.entities.Belle import Belle


class InkBall(Bullet):
    def __init__(self, r, start_pos, end_pos, *sprite_groups):
        super().__init__(r, start_pos, end_pos, *sprite_groups)
        self.hitable_entities = (Belle,)
        self.image = self.r.drawable("inkball")
        self.damage_rate = 10
        self.speed = 1 * self.r.constant("coefficient")
        self.rect = self.image.get_rect()
        self.start_pos = start_pos[0] + 450 * self.r.constant("coefficient") * math.cos(self.angle), \
            start_pos[1] - 450 * self.r.constant("coefficient") * math.sin(self.angle)
        self.rect.x, self.rect.y = self.start_pos
        self.x, self.y = self.start_pos
        self.r.sound("Particle")

    def update(self):
        super().update()
        self.x = self.start_pos[0] + self.lifetime() * self.speed * math.cos(self.angle)
        self.y = self.start_pos[1] - self.lifetime() * self.speed * math.sin(self.angle)
        self.rect.x, self.rect.y = self.x, self.y
        self.current_pos = self.x, self.y


