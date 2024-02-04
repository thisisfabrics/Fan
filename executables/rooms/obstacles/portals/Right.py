import pygame.transform

from executables.rooms.obstacles.portals.Portal import Portal


class Right(Portal):
    def __init__(self, r, room_size):
        super().__init__(r, room_size)
        self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect.x = room_size[0] - self.rect.width
