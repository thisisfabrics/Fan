import math
import random
import time

import pygame.time

from executables.entities.enemies.Enemy import Enemy
from modules.trigonometry import convenient_atan


class Dust(Enemy):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        self.do_once = True
        super().__init__(r, animation_name, animation_period, *sprite_groups)
        self.speed = 1 * self.r.constant("coefficient")
        self.collision_damage_rate = 40
        self.energy_threshold = self.energy // 2
        self.move_time_x = None
        self.move_time_y = None

    def set_destination(self, entity):
        pass

    def set_animation(self, animation_name, period=None):
        if self.do_once:
            super().set_animation(animation_name, period)
            self.do_once = False

    def update(self, rooms_obstacles, rooms_entities, field_size, has_uncommon_navigation=False):
        super().update(rooms_obstacles, rooms_entities, field_size, True)
        if self.move_time_x is None:
            if self.energy < self.energy_threshold:
                self.move_time_x = pygame.time.Clock()
                self.move_time_y = pygame.time.Clock()
                self.destination = random.randrange(len(self.map)), random.randrange(len(self.map[0]))
                iterations = 1000
                while self.map[self.destination[0]][self.destination[1]] and iterations:
                    iterations -= 1
                    self.destination = random.randrange(len(self.map)), random.randrange(len(self.map[0]))
            else:
                return
        if self.location != self.destination:
            angle = convenient_atan(self.destination[0] - self.location[0], self.destination[1] - self.location[1])
            self.x += abs(math.cos(angle) * self.move_time_x.tick() * self.speed) * (1 if self.location[1] < self.destination[1] else -1)
            self.rect.x = self.x
            self.y -= math.sin(angle) * self.move_time_y.tick() * self.speed
            self.rect.y = self.y
        else:
            self.move_time_x = None
            self.energy_threshold = int()
        print(self.location, self.destination, convenient_atan(self.destination[0] - self.location[0], self.destination[1] - self.location[1]))
