import math
import time

import pygame.draw

from executables.bullets.Bullet import Bullet


class Air(Bullet):
    def __init__(self, r, start_pos, end_pos, *sprite_groups):
        super().__init__(r, start_pos, end_pos, *sprite_groups)
        self.start_radius = int(500 * self.r.constant("coefficient"))
        self.detalization = math.pi / 24
        self.angles = list()

    def draw(self, surface):
        if not self.angles:
            angle = math.atan(abs(self.delta_y / self.delta_x))
            if self.delta_x < 0 < self.delta_y:
                angle = math.pi - angle
            if self.delta_y < 0 < self.delta_x:
                angle = 2 * math.pi - angle
            if self.delta_x < 0 and self.delta_y < 0:
                angle = angle + math.pi
            angle = 2 * math.pi - angle
            start_angle = angle - math.pi / 8
            end_angle = angle + math.pi / 8
            self.angles = [start_angle, end_angle]
            for i in range(1, int((end_angle - start_angle) // self.detalization)):
                self.angles.insert(-1, start_angle + i * self.detalization)
        points = [(self.start_pos[0] + math.cos(elem) * self.start_radius * (time.time() - self.spawn_time),
                   self.start_pos[1] - math.sin(elem) * self.start_radius * (time.time() - self.spawn_time))
                  for elem in self.angles]
        points.append(self.start_pos)
        pygame.draw.polygon(surface, pygame.Color("green"), points)

