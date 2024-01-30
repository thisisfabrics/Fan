import pygame


class Widget:
    def __init__(self, r, pos):
        self.r = r
        self.x, self.y = map(lambda elem: elem * self.r.constant("coefficient"), pos)

    def build_surface(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
