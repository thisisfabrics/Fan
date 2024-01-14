import pygame

from executables.rooms.obstacles.Portal import Portal


class Top(Portal):
    def __init__(self, r, room_size):
        super().__init__(r, room_size)
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.x = room_size[0] // 2 - self.rect.width // 2
