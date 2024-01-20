import math
import time

import pygame.transform

from executables.bullets.InkBall import InkBall
from executables.entities.enemies.Enemy import Enemy
from modules.trigonometry import convenient_atan


class Dispenser(Enemy):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        self.do_once = True
        super().__init__(r, animation_name, animation_period, *sprite_groups)
        self.speed = 1 * self.r.constant("coefficient")
        self.offsets = tuple((elem, el) for el in (-1, 1, 0) for elem in (-1, 1, 0) if abs(el) != abs(elem))
        self.bullet_period = 1500
        self.bullet_spawn_time = time.time_ns()
        self.released_bullets_group = pygame.sprite.Group()
        self.animation_period = 300
        self.prev_x, self.prev_y = None, None

    def release_bullet(self):
        try:
            InkBall(self.r, (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2),
                    (self.belle.rect.x + self.belle.rect.width // 2, self.belle.rect.y + self.belle.rect.height // 2),
                    self.released_bullets_group)
        except AttributeError:
            pass
        
    def update(self, rooms_obstacles, rooms_entities, field_size, has_uncommon_navigation=False):
        if time.time_ns() - self.bullet_spawn_time >= self.bullet_period * 10 ** 6:
            self.bullet_spawn_time = time.time_ns()
            self.release_bullet()
        if coords := super().update(rooms_obstacles, rooms_entities, field_size, True):
            return coords
        self.released_bullets_group.update()
        self.image = self.animation_frames[-1]
        if self.prev_x is self.prev_y is None:
            self.prev_x, self.prev_y = self.rect[:2]
        else:
            self.rect.x, self.rect.y = self.prev_x, self.prev_y
        before_rotation_width = self.image.get_rect().width
        before_rotation_heigth = self.image.get_rect().height
        self.image = pygame.transform.rotate(
            self.image,
            convenient_atan(self.belle.rect.y + self.belle.rect.height // 2 - self.rect.y - self.rect.height // 2,
                            self.belle.rect.x + self.belle.rect.width // 2 - self.rect.x - self.rect.width // 2,
                            "deg") - 90)
        after_rotation_width = self.image.get_rect().width
        after_rotation_heigth = self.image.get_rect().height
        self.rect.x -= (after_rotation_width - before_rotation_width) // 2
        self.rect.y -= (after_rotation_heigth - before_rotation_heigth) // 2

    def set_animation(self, animation_name, period=None):
        if self.do_once:
            super().set_animation(animation_name, period)
            self.do_once = False
