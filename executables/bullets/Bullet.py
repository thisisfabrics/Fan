import math
import time

import pygame.time


class Bullet(pygame.sprite.Sprite):
    def __init__(self, r, start_pos, end_pos, *sprite_groups):
        super().__init__(*sprite_groups)
        self.r = r
        self.spawn_time = time.time_ns() / 10 ** 6
        self.lifetime = lambda: time.time_ns() / 10 ** 6 - self.spawn_time
        self.delta_x = end_pos[0] - start_pos[0]
        self.delta_y = end_pos[1] - start_pos[1]
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.speed = 0.5 * self.r.constant("coefficient")
        self.rect = pygame.Rect(self.start_pos[0] - self.r.constant("useful_width") / 2,
                                self.start_pos[1] - self.r.constant("useful_height") / 2,
                                self.r.constant("useful_width"), self.r.constant("useful_height"))
        print(self.rect)
        self.angle = math.atan(abs(self.delta_y / self.delta_x))
        if self.delta_x < 0 < self.delta_y:
            self.angle = math.pi - self.angle
        if self.delta_y < 0 < self.delta_x:
            self.angle = 2 * math.pi - self.angle
        if self.delta_x < 0 and self.delta_y < 0:
            self.angle = self.angle + math.pi
        self.angle = 2 * math.pi - self.angle

    def update(self):
        if not (self.rect.x <= self.start_pos[0] <= self.rect.x + self.rect.width and
                self.rect.y <= self.start_pos[1] <= self.rect.y + self.rect.height):
            self.kill()
            return

