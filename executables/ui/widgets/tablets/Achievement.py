import pygame

from executables.ui.widgets.Label import Label
from executables.ui.widgets.Widget import Widget


class Achievement(Widget):
    def __init__(self, r, pos, condition, icon, description):
        super().__init__(r, pos)
        self.image = self.r.drawable("achievement_frame")
        self.image.blit(icon, (self.image.get_width() * 0.5 - icon.get_width() * 0.5,
                               360 * self.r.constant("coefficient") - icon.get_height() * 0.5))
        Label(self.r, description, (0, 721), 100, 1100).draw(self.image)
        self.condition = condition
        self.check_condition()

    def check_condition(self):
        if self.condition():
            self.image.fill(pygame.Color(5, 50, 10, 50), special_flags=pygame.BLEND_MULT)
            pygame.draw.lines(
                self.image, pygame.Color(0, 255, 0), False,
                ((0, 0), (self.image.get_width() // 2, self.image.get_height()), (self.image.get_width(), 0)), width=10)
