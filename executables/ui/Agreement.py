import pygame

from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button


class Agreement(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.image = self.r.drawable("splash")
        self.button = Button(self.r, self.r.string("ok"), (1600, 1854), self.agree)

    def agree(self):
        self.signal_to_change = "start"

    def mouse_moved(self, pos):
        self.button.check_focus(pos)

    def mouse_pressed(self, button, pos):
        if button == 1:
            self.button.click()

    def update(self):
        self.frame.blit(self.image, (0, 0))
        self.button.draw(self.frame)
        return self.signal_to_change
