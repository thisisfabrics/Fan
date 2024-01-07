import random
import pygame

from executables.entities.Belle import Belle
from executables.rooms.Hall import Hall
from executables.rooms.Room import Room
from executables.ui.Screen import Screen
from modules.collectiontools import linerize


class Continue(Screen):
    def __init__(self, r, frame, mode=False):
        super().__init__(r, frame)
        if not mode:
            self.level = int()
            self.rooms = [[Room(self.r) if random.random() < 1 else Hall(self.r) for j in range(3)] for i in range(3)]
            self.rooms[0][0].add_entity(Belle(self.r, "belle_idle", 200))
            self.rooms[0][0].build()

    def find_belle(self):
        room = next(filter(lambda elem: Belle in map(lambda el: el.__class__, elem.entities_group.sprites()), linerize(self.rooms)))
        belle = room.find_belle()
        return belle, room

    def button_pressed(self, key):
        if key == pygame.K_w:
            self.find_belle()[0].start_moving("up")
        elif key == pygame.K_s:
            self.find_belle()[0].start_moving("down")
        elif key == pygame.K_a:
            self.find_belle()[0].start_moving("left")
        elif key == pygame.K_d:
            self.find_belle()[0].start_moving("right")

    def button_released(self, key):
        if key == pygame.K_w:
            self.find_belle()[0].stop_moving("up")
        elif key == pygame.K_s:
            self.find_belle()[0].stop_moving("down")
        elif key == pygame.K_a:
            self.find_belle()[0].stop_moving("left")
        elif key == pygame.K_d:
            self.find_belle()[0].stop_moving("right")

    def mouse_pressed_pos(self, pos):
        belle, room = self.find_belle()
        room.spawn_bullet(belle.weapons[0].bullet, belle.weapons[0].rect[:2], pos)

    def place_room(self):
        surface_from_room = self.find_belle()[1].draw()
        belle_x, belle_y = self.find_belle()[0].rect.x + self.find_belle()[0].rect.width / 2, \
            self.find_belle()[0].rect.y + self.find_belle()[0].rect.height / 2
        x, y = belle_x - self.r.constant("useful_width") / 2, belle_y - self.r.constant("useful_height") / 2
        x = min(surface_from_room.get_rect().width - self.r.constant("useful_width"), max(0, x))
        y = min(surface_from_room.get_rect().height - self.r.constant("useful_height"), max(0, y))
        self.find_belle()[0].set_mouse_position_compensation(x, y)
        self.frame.blit(surface_from_room, (-x, -y))

    def update(self):
        self.find_belle()[1].update_sprites()
        self.place_room()
