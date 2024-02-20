import pygame

from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button
from executables.ui.widgets.Label import Label


class Finish(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.frame.fill("black")
        self.alpha = int()
        self.image = self.r.drawable("finish")
        self.image.set_alpha(self.alpha)
        self.add_time_event("increase_alpha", self.increase_alpha, 5)
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

    def increase_alpha(self):
        self.alpha += 1
        if self.alpha == 255:
            self.remove_time_event("increase_alpha")
        self.image.set_alpha(self.alpha)

    def update(self):
        self.frame.fill("black")
        self.frame.blit(self.image, (0, 0))
        for elem in self.buttons:
            elem.check_focus(pygame.mouse.get_pos())
            elem.draw(self.frame)
        return self.signal_to_change
