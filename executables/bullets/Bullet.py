import math
import time

import pygame.time

from modules.trigonometry import convenient_atan


class Bullet(pygame.sprite.Sprite):
    def __init__(self, r, start_pos, end_pos, *sprite_groups):
        super().__init__(*sprite_groups)
        self.r = r
        self.damage_rate = 1
        self.spawn_time = time.time_ns() / 10 ** 6
        self.lifetime = lambda: time.time_ns() / 10 ** 6 - self.spawn_time
        self.start_pos = start_pos
        self.hitable_entities = tuple()
        self.end_pos = end_pos
        self.current_pos = self.start_pos
        self.speed = 0.5 * self.r.constant("coefficient")
        self.barier_rect = pygame.Rect(self.start_pos[0] - self.r.constant("useful_width") / 2,
                                       self.start_pos[1] - self.r.constant("useful_height") / 2,
                                       self.r.constant("useful_width"), self.r.constant("useful_height"))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.angle = convenient_atan(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        self.x, self.y = self.rect[:2]

    def update(self):
        if not (self.barier_rect.x <= self.current_pos[0] <= self.barier_rect.x + self.barier_rect.width and
                self.barier_rect.y <= self.current_pos[1] <= self.barier_rect.y + self.barier_rect.height):
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect[:2])

