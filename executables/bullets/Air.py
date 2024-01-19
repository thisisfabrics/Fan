import math

import pygame.draw
import executables.bullets.Bullet
import executables.entities


class Air(executables.bullets.Bullet.Bullet):
    def __init__(self, r, start_pos, end_pos, *sprite_groups):
        super().__init__(r, start_pos, end_pos, *sprite_groups)
        self.speed = 2 * self.r.constant("coefficient")
        self.wavefront_threshold = int(500 * self.r.constant("coefficient"))
        self.damage_rate = 10
        self.hitable_entities = (executables.entities.enemies.Catterfield.Catterfield, executables.entities.enemies.Dust.Dust)
        detalization = math.pi / 48
        start_angle = self.angle - math.pi / 16
        end_angle = self.angle + math.pi / 16
        self.angles = [start_angle]
        while (an := self.angles[-1] + detalization) < end_angle:
            self.angles.append(an)
        self.wavefront = list()
        self.wavefront_history = list()
        self.killing = False

    def calculate_points(self):
        self.wavefront = [(self.start_pos[0] + math.cos(elem) * self.speed * self.lifetime(),
                           self.start_pos[1] - math.sin(elem) * self.speed * self.lifetime())
                          for elem in self.angles]
        self.wavefront_history.append(self.wavefront)
        self.current_pos = self.wavefront[len(self.wavefront) // 2]

    def draw(self, surface):
        if not self.killing:
            self.calculate_points()
            rect_collection = self.wavefront_history[0] + self.wavefront_history[-1]
            self.rect = pygame.Rect(m_x := min(rect_collection, key=lambda elem: elem[0])[0],
                                    m_y := min(rect_collection, key=lambda elem: elem[1])[1],
                                    max(rect_collection, key=lambda elem: elem[0])[0] - m_x,
                                    max(rect_collection, key=lambda elem: elem[1])[1] - m_y,)
            if self.speed * self.lifetime() > self.wavefront_threshold:
                del self.wavefront_history[0]
                self.decorate(surface, self.wavefront + self.wavefront_history[0][::-1])
            else:
                self.decorate(surface, self.wavefront + [self.start_pos])
        else:
            if len(self.wavefront_history) == 1:
                self.kill()
                return
            del self.wavefront_history[0]
            self.decorate(surface, self.wavefront + self.wavefront_history[0][::-1])

    def decorate(self, surface, points):
        points_group_1, points_group_2 = points, points
        if self.speed * self.lifetime() > self.wavefront_threshold:
            points_group_1 = points[:len(points) // 2] + self.wavefront_history[len(self.wavefront_history) // 3 * 2][::-1]
            points_group_2 = points[len(points) // 2:] + self.wavefront_history[len(self.wavefront_history) // 3]
        for elem in (points_group_1, points_group_2):
            pygame.draw.polygon(surface, self.r.color("air_bullet_filling"), elem)
            pygame.draw.polygon(surface, pygame.Color("black"), elem, int(10 * self.r.constant("coefficient")))

    def update(self):
        if not (self.barier_rect.x <= self.current_pos[0] <= self.barier_rect.x + self.barier_rect.width and
                self.barier_rect.y <= self.current_pos[1] <= self.barier_rect.y + self.barier_rect.height):
            self.killing = True
