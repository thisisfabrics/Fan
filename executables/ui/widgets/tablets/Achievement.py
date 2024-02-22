import pygame

from executables.ui.widgets.InteractiveWidget import InteractiveWidget
from executables.ui.widgets.Label import Label


class Achievement(InteractiveWidget):
    def __init__(self, r, pos, condition, icon, description):
        super().__init__(r, pos, lambda: None)
        self.image = pygame.Surface(self.r.drawable("achievement_frame").get_size(), pygame.SRCALPHA, 32)
        self.image.blit(self.r.drawable("achievement_frame"), (0, 0))
        self.image.blit(icon, (self.image.get_width() * 0.5 - icon.get_width() * 0.5,
                               360 * self.r.constant("coefficient") - icon.get_height() * 0.5))
        Label(self.r, description, (200, 721), 100, 600).draw(self.image)
        self.condition = condition
        self.check_condition()

    def check_condition(self):
        if self.condition:
            self.image.blit(self.r.drawable("done"), (0, 0))
