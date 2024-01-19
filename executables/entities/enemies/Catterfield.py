import math

from executables.entities.enemies.Enemy import Enemy


class Catterfield(Enemy):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(r, animation_name, animation_period, *sprite_groups)
        self.speed = 0.1 * self.r.constant("coefficient")
        self.collision_damage_rate = 20
        self.angle = math.pi

    def add_damaging_bullet(self, bullet):
        super().add_damaging_bullet(bullet)
        self.angle = 2 * math.pi - bullet.angle

    def move(self, length):
        if len(self.damaging_bullets):
            length = self.speed * max(map(lambda elem: elem[0].tick(), self.damaging_bullets.values()))
            self.x += (x_movement := length * math.cos(self.angle))
            self.y += (y_movement := length * math.sin(self.angle))
            self.rect.x = self.x
            self.rect.y = self.y
            self.last_delta_x = x_movement
            self.last_delta_y = y_movement
        else:
            super().move(length)
