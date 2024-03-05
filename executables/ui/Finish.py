import pygame

from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button
from executables.ui.widgets.Label import Label


class Finish(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        surface = pygame.Surface(self.r.drawable("finish").get_size())
        surface.blit(self.r.drawable("finish"), (0, 0))
        self.image = surface
        label_about_destructions, label_about_floors = next(
            self.r.query("SELECT liquidated_enemies, floor FROM statistics WHERE is_finished = 0"))
        self.r.query("UPDATE statistics SET is_finished = 1")
        self.r.database.commit()
        Label(self.r, self.r.string("you_have_liquidated").replace('%', str(label_about_destructions - 1)),
              (2405, 394), 200, self.image.get_width() * 0.48, "white").draw(self.image)
        Label(self.r, self.r.string("you_have_reached").replace('%', str(label_about_floors)),
              (2405, 900), 200, self.image.get_width() * 0.48, "white").draw(self.image)
        self.buttons = (
            Button(self.r, self.r.string("new_game"), (2405, 1800), lambda: self.set_signal("continue")),
            Button(self.r, self.r.string("exit"), (2405, 1500), lambda: self.set_signal("start"))
        )

    def mouse_pressed(self, button, pos):
        if button == 1:
            for elem in self.buttons:
                elem.click()

    def update(self):
        self.frame.blit(self.image, (0, 0))
        for elem in self.buttons:
            elem.check_focus(pygame.mouse.get_pos())
            elem.draw(self.frame)
        self.frame.blit(self.darking_surface, (0, 0))
        return self.signal_to_change
