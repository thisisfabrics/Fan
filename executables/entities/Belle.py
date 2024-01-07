import pygame

from executables.entities.Entity import Entity
from executables.weapons.Fan import Fan


class Belle(Entity):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(r, animation_name, animation_period, *sprite_groups)
        self.weapons = [Fan(self.r, self.rect[:2])]
        self.mouse_position_compensation_x = int()
        self.mouse_position_compensation_y = int()
        self.mouse_position_x, self.mouse_position_y = pygame.mouse.get_pos()
        self.x_move_time = UselessClock()
        self.y_move_time = UselessClock()
        self.x_movement = int()
        self.y_movement = int()

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

    def move(self):
        self.last_delta_x = self.x_move_time.tick() * self.x_movement * self.speed
        self.last_delta_y = self.y_move_time.tick() * self.y_movement * self.speed
        self.rect.x += int(self.last_delta_x)
        self.rect.y += int(self.last_delta_y)

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

    def update(self, *args):
        super().update()
        self.move()
        self.aim_cursor()


class UselessClock:
    def tick(self):
        return int()
