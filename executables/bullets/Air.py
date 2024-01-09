import math
import time

import pygame.draw

from executables.bullets.Bullet import Bullet


class Air(Bullet):
    def __init__(self, r, start_pos, end_pos, *sprite_groups):
        super().__init__(r, start_pos, end_pos, *sprite_groups)
        self.speed = 2 * self.r.constant("coefficient")
        self.wavefront_threshold = int(500 * self.r.constant("coefficient"))
        detalization = math.pi / 48
        start_angle = self.angle - math.pi / 16
        end_angle = self.angle + math.pi / 16
        self.angles = [start_angle]
        while (an := self.angles[-1] + detalization) < end_angle:
            self.angles.append(an)
        self.wavefront = list()
        self.wevefront_history = list()
        self.count_of_drawcalls = int()

    def calculate_points(self):
        self.wavefront = [(self.start_pos[0] + math.cos(elem) * self.speed * self.lifetime(),
                           self.start_pos[1] - math.sin(elem) * self.speed * self.lifetime())
                          for elem in self.angles]
        self.wevefront_history.append(self.wavefront)
        self.end_pos = self.wavefront[len(self.wavefront) // 2]

    def draw(self, surface):
        self.calculate_points()
        if self.speed * self.lifetime() > self.wavefront_threshold:
            pygame.draw.polygon(surface, pygame.Color("green"), self.wavefront +
                                self.wevefront_history[-self.count_of_drawcalls][::-1])
        else:
            self.count_of_drawcalls += 1
            pygame.draw.polygon(surface, pygame.Color("green"), self.wavefront + [self.start_pos])

