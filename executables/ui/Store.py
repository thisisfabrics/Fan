import random

import pygame

from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button
from executables.ui.widgets.Label import Label


class Store(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.money = self.r.query("SELECT money FROM belle").fetchall()[0][0]
        self.displayed = self.r.query("SELECT type FROM catalyst WHERE displayed = 1").fetchall()
        if not self.displayed:
            self.populate()
        self.displayed = [self.r.constant("id_to_catalyst_object")[elem[0]](self.r) for elem in self.displayed]
        self.buttons = (Button(self.r, self.r.string("buy"), (550, 1857), self.buy),
                        Button(self.r, self.r.string("buy"), (1360, 1817), self.buy),
                        Button(self.r, self.r.string("buy"), (2199, 1797), self.buy))
        self.surfaces = list()
        self.build_surfaces()

    def buy(self):
        pass

    def populate(self):
        self.displayed = self.r.query("SELECT type FROM catalyst WHERE purchased = 0").fetchall()
        random.shuffle(self.displayed)
        while len(self.displayed) > 3:
            self.displayed.pop()

    def build_surfaces(self):
        for elem in self.displayed:
            label = Label(self.r, elem.description, (47, 382), 70, 254)
            surface = pygame.Surface((max(554 * self.r.constant("coefficient"), label.image.get_width() + label.x * 2), 966 * self.r.constant("coefficient")),
                                     pygame.SRCALPHA, 32)
            surface.blit(elem.image, (0.5 * surface.get_width() - 0.5 * elem.image.get_width(),
                                      elem.image.get_height() // 2))
            surface.blit(label.image, (label.x, label.y))
            Label(self.r, f"{self.r.string("costs")}: {elem.price}",
                  (47, pass),
                  70, 254).draw(surface)
            self.surfaces.append(surface)

    def update(self):
        self.frame.blit(self.r.drawable("store"), (0, 0))
        for i, elem in enumerate(self.surfaces):
            self.frame.blit(elem, (self.r.constant("store_offset_x") + i * self.r.constant("store_padding"),
                                   self.r.constant("store_offset_y")))
        for i, button in enumerate(self.buttons):
            button.check_focus(pygame.mouse.get_pos())
            if button.is_enabled and (self.money < self.displayed[i].price if i < len(self.displayed) else True):
                button.is_enabled = False
                if i < len(self.displayed):
                    button.rebuild_label(self.r.string("not_enough_money"))
                    button.focus = False
            button.draw(self.frame)

