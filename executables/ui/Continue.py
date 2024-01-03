import random
import pygame

from executables.entities.Bell import Bell
from executables.rooms.Hall import Hall
from executables.rooms.Room import Room
from executables.ui.Screen import Screen
from modules.collectiontools import linerize


class Continue(Screen):
    def __init__(self, r, frame, mode=False):
        super().__init__(r, frame)
        if not mode:
            self.level = int()
            self.rooms = [[Room(self.r) if random.random() < 0 else Hall(self.r) for j in range(3)] for i in range(3)]
            self.bell = Bell(self.r, "bell_idle", 200)
            self.rooms[0][0].add_entity(self.bell)

    def button_pressed(self, key):
        if key == pygame.K_w:
            self.bell.start_moving("up")
        elif key == pygame.K_s:
            self.bell.start_moving("down")
        elif key == pygame.K_a:
            self.bell.start_moving("left")
        elif key == pygame.K_d:
            self.bell.start_moving("right")

    def button_released(self, key):
        if key == pygame.K_w:
            self.bell.stop_moving("up")
        elif key == pygame.K_s:
            self.bell.stop_moving("down")
        elif key == pygame.K_a:
            self.bell.stop_moving("left")
        elif key == pygame.K_d:
            self.bell.stop_moving("right")

    def place_room(self):
        room = next(filter(lambda elem: self.bell in elem.entities, linerize(self.rooms)))
        bell_x, bell_y = self.bell.rect.x + self.bell.rect.width / 2, self.bell.rect.y + self.bell.rect.height / 2
        x, y = bell_x - self.r.constant("useful_width") / 2, bell_y - self.r.constant("useful_height") / 2
        x = min(room.image.get_rect().width - self.r.constant("useful_width"), max(0, x))
        y = min(room.image.get_rect().height - self.r.constant("useful_height"), max(0, y))
        self.bell.set_mouse_position_compensation(x, y)
        self.frame.blit(room.draw(self.bell), (-x, -y))

    def update(self):
        self.bell.update()
        self.frame.fill(pygame.Color("red"))
        self.place_room()
