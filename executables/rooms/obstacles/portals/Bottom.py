import pygame

from executables.rooms.obstacles.portals.Portal import Portal


class Bottom(Portal):
    def __init__(self, r, room_size):
        super().__init__(r, room_size)
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = room_size[0] // 2 - self.rect.width // 2
        self.rect.y = room_size[1] - self.rect.height
