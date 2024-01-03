import pygame

from executables.entities.Entity import Entity


class Bell(Entity):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(r, animation_name, animation_period, *sprite_groups)
        self.weapons = []
        self.mouse_position_compensation_x = int()
        self.mouse_position_compensation_y = int()
        self.mouse_position_x, self.mouse_position_y = pygame.mouse.get_pos()

    def aim_cursor(self):
        self.set_mouse_position()
        if self.rect.x + self.rect.width / 2 <= self.mouse_position_x and not self.animation_is_flipped:
            self.animation_is_flipped = True
        elif self.rect.x + self.rect.width / 2 > self.mouse_position_x and self.animation_is_flipped:
            self.animation_is_flipped = False

    def set_mouse_position(self):
        self.mouse_position_x, self.mouse_position_y = pygame.mouse.get_pos()
        self.mouse_position_x += self.mouse_position_compensation_x
        self.mouse_position_y += self.mouse_position_compensation_y

    def set_mouse_position_compensation(self, x, y):
        self.mouse_position_compensation_x, self.mouse_position_compensation_y = x, y

    def update(self):
        super().update()
        self.aim_cursor()
