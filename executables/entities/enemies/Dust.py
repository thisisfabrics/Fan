import math
import random
import time

import pygame.time

from executables.entities.Belle import UselessClock
from executables.entities.enemies.Enemy import Enemy
from modules.trigonometry import convenient_atan


class Dust(Enemy):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(r, animation_name, animation_period, *sprite_groups)
        self.speed = 10 * self.r.constant("coefficient")
        self.collision_damage_rate = 40
        self.energy_threshold = self.energy // 2
        self.move_time = None

    def update(self, rooms_obstacles, rooms_entities, field_size, has_uncommon_navigation=False):
        super().update(rooms_obstacles, rooms_entities, field_size, True)
        if self.move_time is None and self.energy < self.energy_threshold:
            self.move_time = pygame.time.Clock()
            self.destination = (random.randrange(field_size[0]) // self.chunk_width,
                                random.randrange(field_size[1]) // self.chunk_height)
            iterations = 1000
            while self.map[self.destination[1]][self.destination[0]] and iterations:
                iterations -= 1
                self.destination = (random.randrange(field_size[0]) // self.chunk_width,
                                    random.randrange(field_size[1]) // self.chunk_height)
            self.destination = self.chunck_to_pos(self.destination)
        elif self.move_time:
            if self.location != self.destination:
                angle = convenient_atan(self.destination[0] - self.location[0], self.destination[1] - self.location[1])
                self.x += math.cos(angle) * self.move_time.tick() * self.speed
                self.rect.x = self.x
                self.y -= math.sin(angle) * self.move_time.tick() * self.speed
                self.rect.y = self.y
            else:
                self.move_time = UselessClock()
