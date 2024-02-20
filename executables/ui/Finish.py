import pygame

from executables.ui.Screen import Screen
from executables.ui.widgets.Label import Label


class Finish(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.frame.fill("black")
        self.alpha = 0
        self.image = self.r.drawable("finish")
        self.image.set_alpha(0)
        self.add_time_event("increase_alpha", self.increase_alpha, 100)
        label_about_destructions, label_about_floors = next(
            self.r.query("SELECT liquidated_enemies, floor FROM statistics WHERE is_finished = 0"))
        self.r.query("UPDATE statistics SET is_finished = 1")
        self.r.database.commit()
        Label(self.r, self.r.string("you_have_liquidated").replace('%', str(label_about_destructions - 1)),
              (2405, 994), 200, self.image.get_width() * 0.48, "white").draw(self.image)
        Label(self.r, self.r.string("you_have_reached").replace('%', str(label_about_floors)),
              (2405, 1500), 200, self.image.get_width() * 0.48, "white").draw(self.image)

    def increase_alpha(self):
        self.alpha += 1
        if self.alpha == 100:
            self.remove_time_event("increase_alpha")
        self.image.set_alpha(self.alpha)

    def update(self):
        self.frame.blit(self.image, (0, 0))
