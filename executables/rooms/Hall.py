import pygame

from executables.rooms.Room import Room


class Hall(Room):
    def __init__(self, r, collection_coords, is_recreated=False):
        super().__init__(r, collection_coords, is_recreated)
        quad_surface = pygame.Surface(((w := self.r.constant("useful_width")) * 2,
                                       (h := self.r.constant("useful_height")) * 2))
        quad_surface.fill(pygame.Color(142, 175, 154))
        quad_surface.blit(self.image, (0, 0))
        quad_surface.blit(self.image, (w, 0))
        quad_surface.blit(self.image, (0, h))
        quad_surface.blit(self.image, (w, h))
        self.image = quad_surface
        self.max_count_of_obstacles *= 3
        self.max_count_of_enemies *= 3
        self.build_portals()
        if not is_recreated:
            self.build()
            self.populate()

