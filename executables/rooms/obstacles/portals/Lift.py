import pygame

from executables.rooms.obstacles.portals.Portal import Portal


class Lift(Portal):
    def __init__(self, r, room_size, level, *sprites_group):
        super().__init__(r, room_size, *sprites_group)
        self.image_closed = r.drawable("lift")
        self.image_closed = pygame.transform.rotate(self.image_closed, 270)
        self.image_opened = r.drawable("lift_opened")
        self.image_opened = pygame.transform.rotate(self.image_opened, 270)
        self.rect = self.image_closed.get_rect()
        self.rect.x = room_size[0] // 2 - self.rect.width // 2
        self.label = (pygame.font.Font("../data/media/fonts/AmaticSC-Bold.ttf", int(72 * self.r.constant("coefficient")))
                      .render(str(level), 1, pygame.Color("black")))
        self.label_pos = 417.496 * self.r.constant("coefficient"), 52 * self.r.constant("coefficient")
        self.count_of_enemies = int()

    def set_count_of_enemies(self, count):
        self.count_of_enemies = count * 0  # DELETE

    def draw(self, surface):
        surface.blit(self.image_closed if self.count_of_enemies else self.image_opened, self.rect[:2])
        surface.blit(self.label, (self.rect.x + self.label_pos[0], self.rect.y + self.label_pos[1]))
        display_enemies_remain = (pygame.font.Font("../data/media/fonts/AmaticSC-Regular.ttf",
                                                   int(200 * self.r.constant("coefficient")))
                                  .render(f"{self.r.string("remain")}: {self.count_of_enemies}", 1, pygame.Color("black")))
        surface.blit(display_enemies_remain, (self.rect.x + self.label_pos[0] * 2, self.rect.y + self.label_pos[1] * 2))
