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
        self.x_move_time = UselessClock()
        self.y_move_time = UselessClock()
        self.x_movement = int()
        self.y_movement = int()
        self.last_delta_x = float()
        self.last_delta_y = float()

    def repos(self, pos):
        self.rect.x, self.rect.y = pos

    def random_repos(self, x_stop_range, y_stop_range, *dont_collide_with_these_sprite_groups):
        pos = (random.randrange(x_stop_range - self.rect.width),
               random.randrange(y_stop_range - self.rect.height))
        self.rect.x, self.rect.y = pos
        while sum(1 for el in filter(lambda elem: pygame.sprite.spritecollideany(self, elem),
                                     dont_collide_with_these_sprite_groups)):
            pos = (random.randrange(x_stop_range - self.rect.width),
                   random.randrange(y_stop_range - self.rect.height))
            self.rect.x, self.rect.y = pos

    def damage(self, bullet):
        self.energy -= bullet.damage
        if self.energy <= 0:
            self.kill()

    def set_animation(self, animation_name, period=None):
        self.animation_name = animation_name
        self.animation_frames = [elem for key, elem in self.r.drawable_dictionary.items() if animation_name in key]
        if period:
            self.animation_period = period

    def start_moving(self, direction):
        if direction == "up":
            self.y_movement = -1
            self.y_move_time = pygame.time.Clock()
        elif direction == "down":
            self.y_movement = 1
            self.y_move_time = pygame.time.Clock()
        elif direction == "left":
            self.x_movement = -1
            self.x_move_time = pygame.time.Clock()
        elif direction == "right":
            self.x_movement = 1
            self.x_move_time = pygame.time.Clock()
        if "movement" not in self.animation_name:
            self.set_animation(f"{self.__class__.__name__.lower()}_movement")

    def stop_moving(self, direction):
        if direction == "up":
            if self.y_movement == -1:
                self.y_move_time = UselessClock()
        elif direction == "down":
            if self.y_movement == 1:
                self.y_move_time = UselessClock()
        elif direction == "left":
            if self.x_movement == -1:
                self.x_move_time = UselessClock()
        elif direction == "right":
            if self.x_movement == 1:
                self.x_move_time = UselessClock()
        if not (self.y_move_time.tick() + self.x_move_time.tick()) and "idle" not in self.animation_name:
            self.set_animation(f"{self.__class__.__name__.lower()}_idle")

    def play_animation(self):
        if time.time_ns() - self.spawn_time >= self.animation_period * 10 ** 6:
            self.image = self.animation_frames.pop(0)
            self.animation_frames.append(self.image)
            if self.animation_is_flipped:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.spawn_time = time.time_ns()

    def move(self):
        self.last_delta_x = self.x_move_time.tick() * self.x_movement * self.speed
        self.last_delta_y = self.y_move_time.tick() * self.y_movement * self.speed
        self.rect.x += int(self.last_delta_x)
        self.rect.y += int(self.last_delta_y)

    def undo_move_x(self):
        self.rect.x -= int(self.last_delta_x)

    def undo_move_y(self):
        self.rect.y -= int(self.last_delta_y)

    def redo_move_x(self):
        self.rect.x += int(self.last_delta_x)

    def redo_move_y(self):
        self.rect.y += int(self.last_delta_y)

    def update(self):
        self.play_animation()
        self.move()


class UselessClock:
    def tick(self):
        return int()
