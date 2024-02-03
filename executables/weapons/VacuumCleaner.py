import pygame

from executables.bullets.Stream import Stream
from executables.weapons.Weapon import Weapon


class VacuumCleaner(Weapon):
    def __init__(self, r, pos, animation_name, animation_period):
        super().__init__(r, pos, animation_name, animation_period)
        self.bullet = Stream
        self.offset_not_flipped = -180 * self.r.constant("coefficient"), 296.788 * self.r.constant("coefficient")
        self.offset_flipped = 20 * self.r.constant("coefficient"), self.offset_not_flipped[1]
        self.bullet_offset_x = int()
        self.apply_offset()
        self.timeout = 200

    def release_bullet(self, mouse_position_compenstation):
        for i in range(self.power):
            self.bullet(self.r,
                        (self.rect.x + self.rect.width // 2 + self.bullet_offset_x * (1 if self.animation_is_flipped else -1),
                         self.rect.y + self.rect.height // 2),
                        ((mp := pygame.mouse.get_pos())[0] + mouse_position_compenstation[0],
                         mp[1] + mouse_position_compenstation[1]), self, self.bullets_group)

    def apply_offset(self):
        super().apply_offset()
        self.bullet_offset_x = 300 if self.animation_is_flipped else 500
        self.bullet_offset_x *= self.r.constant("coefficient")
