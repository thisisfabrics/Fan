import random
import time

import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(*sprite_groups)
        self.r = r
        self.animation_name = animation_name
        self.animation_frames = list()
        self.animation_is_flipped = False
        self.animation_period = animation_period
        self.set_animation(animation_name)
        self.image = self.animation_frames[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (self.r.constant("useful_width") / 2 - self.rect.width / 2,
                                    self.r.constant("useful_height") / 2 - self.rect.height / 2)
        self.spawn_time = time.time_ns()
        self.energy = 100
        self.speed = 0.5
        self.x_movement = int()
        self.y_movement = int()
        self.last_delta_x = float()
        self.last_delta_y = float()

    def damage(self, bullet):
        self.energy -= bullet.damage
        if self.energy <= 0:
            self.kill()

    def set_animation(self, animation_name, period=None):
        self.animation_name = animation_name
        self.animation_frames = [elem for key, elem in self.r.drawable_dictionary.items() if animation_name in key]
        if period:
            self.animation_period = period

    def play_animation(self):
        if time.time_ns() - self.spawn_time >= self.animation_period * 10 ** 6:
            self.image = self.animation_frames.pop(0)
            self.animation_frames.append(self.image)
            if self.animation_is_flipped:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.spawn_time = time.time_ns()

    def undo_move_x(self):
        self.rect.x -= int(self.last_delta_x)

    def undo_move_y(self):
        self.rect.y -= int(self.last_delta_y)

    def redo_move_x(self):
        self.rect.x += int(self.last_delta_x)

    def redo_move_y(self):
        self.rect.y += int(self.last_delta_y)

    def update(self, *args):
        self.play_animation()
