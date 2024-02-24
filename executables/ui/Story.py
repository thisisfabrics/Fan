import pygame

from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button


class Story(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.image = self.r.drawable("com")
        self.darking_surface = pygame.Surface((0, 0))
        self.darking_surface.set_alpha(0)
        self.add_time_event("darking", self.darking, 20)
        self.button = Button(self.r, self.r.string("continue"), (1600, 1854), self.new_game)

    def darking(self):
        if self.darking_surface.get_alpha() != 255:
            self.darking_surface.set_alpha(self.darking_surface.get_alpha() + 1)
        else:
            self.remove_time_event("darking")

    def new_game(self):
        self.signal_to_change = "continue"

    def mouse_moved(self, pos):
        self.button.check_focus(pos)

    def mouse_pressed(self, button, pos):
        if button == 1:
            self.button.click()

    def update(self):
        self.frame.fill("black")
        self.frame.blit(self.image, (0, 0))
        self.button.draw(self.frame)
        self.frame.blit(self.darking_surface, (0, 0))
        return self.signal_to_change
