import pygame

from executables.entities.Entity import Entity


class Enemy(Entity):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(r, animation_name, animation_period, *sprite_groups)

    def set_visibility(self, visible):
        if visible:
            self.image.set_alpha(255)
            self.rect.width = self.image.get_rect().width
            self.rect.height = self.image.get_rect().height
        else:
            self.image.set_alpha(0)

