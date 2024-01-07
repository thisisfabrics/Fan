import time

import pygame


class Animated:
    def __init__(self, r, animation_name, animation_period):
        self.r = r
        self.spawn_time = time.time_ns()
        self.animation_name = animation_name
        self.animation_frames = list()
        self.animation_is_flipped = list()
        self.animation_period = animation_period
        self.set_animation(self.animation_name)
        self.image = self.animation_frames[0]

    def set_animation(self, animation_name, period=None):
        self.animation_name = animation_name
        self.animation_frames = [elem for key, elem in self.r.drawable_dictionary.items() if animation_name in key]
        if period:
            self.animation_period = period

    def play_animation(self, force=False):
        if time.time_ns() - self.spawn_time >= self.animation_period * 10 ** 6 or force:
            self.image = self.animation_frames.pop(0)
            self.animation_frames.append(self.image)
            if self.animation_is_flipped:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.spawn_time = time.time_ns()
