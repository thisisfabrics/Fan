import time
import pygame.transform

from executables.bullets.InkBall import InkBall
from executables.entities.Belle import Belle
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
        self.temperature = float()
        self.boiling_rate = 0.1
        self.boiling_clock = pygame.time.Clock()

    def release_bullet(self, to_where):
        try:
            InkBall(self.r,
                    (self.rect.x + self.image.get_rect().width // 2, self.rect.y + self.image.get_rect().height // 2),
                    (to_where.rect.x + to_where.rect.width // 2, to_where.rect.y + to_where.rect.height // 2),
                    self.released_bullets_group)
        except AttributeError:
            pass

    def boiling(self):
        if self.damaging_bullets:
            self.temperature += self.boiling_rate * self.boiling_clock.tick()
            self.temperature = min(100, self.temperature)
        else:
            self.temperature -= self.boiling_rate * self.boiling_clock.tick()
            self.temperature = max(0, self.temperature)

    def apply_temperature(self):
        surface = pygame.Surface(self.image.get_rect()[-2:], pygame.SRCALPHA, 32)
        surface.blit(self.image, (0, 0))
        surface.fill(pygame.Color(0, 0, int(self.temperature)), special_flags=pygame.BLEND_RGB_ADD)
        self.image = surface
        
    def update(self, rooms_obstacles, rooms_entities, field_size, has_uncommon_navigation=False):
        if coords := super().update(rooms_obstacles, rooms_entities, field_size, True):
            return coords
        belle = next(filter(lambda elem: isinstance(elem, Belle), rooms_entities.sprites()))
        self.released_bullets_group.update()
        self.image = self.animation_frames[-1]
        self.apply_temperature()
        self.boiling()
        if self.prev_x is self.prev_y is None:
            self.prev_x, self.prev_y = self.rect[:2]
        else:
            self.rect.x, self.rect.y = self.prev_x, self.prev_y
        before_rotation_width = self.image.get_rect().width
        before_rotation_heigth = self.image.get_rect().height
        self.image = pygame.transform.rotate(
            self.image,
            convenient_atan(belle.rect.y + belle.rect.height // 2 - self.rect.y - self.rect.height // 2,
                            belle.rect.x + belle.rect.width // 2 - self.rect.x - self.rect.width // 2,
                            "deg") - 90)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        after_rotation_width = self.image.get_rect().width
        after_rotation_heigth = self.image.get_rect().height
        self.rect.x -= (after_rotation_width - before_rotation_width) // 2
        self.rect.y -= (after_rotation_heigth - before_rotation_heigth) // 2
        if time.time_ns() - self.bullet_spawn_time >= self.bullet_period * 10 ** 6:
            self.bullet_spawn_time = time.time_ns()
            self.release_bullet(belle)

    def set_animation(self, animation_name, period=None):
        if self.do_once:
            super().set_animation(animation_name, period)
            self.do_once = False
