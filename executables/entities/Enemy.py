import pygame

from executables.entities.Entity import Entity


class Enemy(Entity):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(r, animation_name, animation_period, *sprite_groups)

