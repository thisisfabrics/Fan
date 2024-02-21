import itertools
import random

import pygame

from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button
from executables.ui.widgets.Label import Label


class Store(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.images = [self.r.drawable("store_0"), self.r.drawable("store_1")]
        self.add_time_event("animation", lambda: self.images.insert(0, self.images.pop()), 500)
        self.money = self.r.query("SELECT money FROM belle").fetchall()[0][0]
        self.displayed = self.r.query("SELECT id FROM catalyst WHERE displayed = 1").fetchall()
        if not self.displayed:
            self.populate()
        self.displayed = [self.r.constant("id_to_catalyst_object")[elem[0]](self.r) for elem in self.displayed]
        self.buy_buttons = (Button(self.r, self.r.string("buy"), (550, 1857), self.buy),
                            Button(self.r, self.r.string("buy"), (1360, 1817), self.buy),
                            Button(self.r, self.r.string("buy"), (2199, 1820), self.buy))
        self.buttons = (Button(self.r, self.r.string("reset"), (3400, 20), self.exit, True),)
        self.surfaces = list()
        self.build_surfaces()

    def buy(self):
        for i, button in enumerate(self.buy_buttons):
            if not button.focus:
                continue
            self.r.query("UPDATE catalyst SET purchased = 1 "
                         f"WHERE id = {self.r.constant("catalyst_object_to_id")[self.displayed[i].__class__]}")
            self.money -= self.displayed[i].price
            self.r.query(f"UPDATE belle SET money = {self.money}")
            self.r.query(f"UPDATE statistics SET activated_catalysts = activated_catalysts + 1 WHERE is_finished = 0")
        self.r.database.commit()

    def populate(self):
        self.displayed = self.r.query("SELECT id FROM catalyst WHERE displayed = 1").fetchall()
        if not self.displayed:
            self.displayed = self.r.query("SELECT id FROM catalyst WHERE purchased = 0 LIMIT 3").fetchall()
            random.shuffle(self.displayed)
            if delta := 3 - len(self.displayed):
                self.displayed.extend(filter(lambda elem: elem not in self.displayed,
                                             self.r.query(f"SELECT id FROM catalyst LIMIT {delta}")))
            for elem in self.displayed:
                self.r.query(f"UPDATE catalyst SET displayed = 1 WHERE id = {elem[0]}")
            self.r.database.commit()

    def build_surfaces(self):
        for elem in self.displayed:
            label = Label(self.r, elem.description, (47, 320), 70, 350)
            surface = pygame.Surface((max(554 * self.r.constant("coefficient"), label.image.get_width() + label.x * 2),
                                      966 * self.r.constant("coefficient")),
                                     pygame.SRCALPHA, 32)
            surface.blit(elem.image, (0.5 * surface.get_width() - 0.5 * elem.image.get_width(),
                                      elem.image.get_height() // 3))
            surface.blit(label.image, (label.x, label.y))
            Label(self.r, f"{self.r.string("costs")}: {elem.price}",
                  (47, 340 + label.image.get_height() / self.r.constant("coefficient")),
                  80, 254).draw(surface)
            self.surfaces.append(surface)

    def mouse_pressed(self, button, pos):
        if button == 1:
            for elem in itertools.chain(self.buttons, self.buy_buttons):
                elem.click()

    def exit(self):
        self.signal_to_change = "continued"

    def update(self):
        self.frame.blit(self.images[0], (0, 0))
        for i, elem in enumerate(self.surfaces):
            self.frame.blit(elem, (self.r.constant("store_offset_x") + i * self.r.constant("store_padding"),
                                   self.r.constant("store_offset_y")))
        for i, button in enumerate(self.buy_buttons):
            button.check_focus(pygame.mouse.get_pos())
            if button.is_enabled and (
                    next(self.r.query("SELECT purchased FROM catalyst WHERE id = "
                                      f"{self.r.constant("catalyst_object_to_id")[self.displayed[i].__class__]}"))[0]
                    == 1 if len(self.displayed) > i else False):
                button.is_enabled = False
                button.rebuild_label(self.r.string("purchased"))
            elif button.is_enabled and (self.money < self.displayed[i].price if i < len(self.displayed) else True):
                button.is_enabled = False
                if i < len(self.displayed):
                    button.rebuild_label(self.r.string("not_enough_money"))
                    button.focus = False
            button.draw(self.frame)
        for button in self.buttons:
            button.check_focus(pygame.mouse.get_pos())
            button.draw(self.frame)
        Label(self.r, f"{self.r.string("amount_of_money")}: {self.money}", (40, 5), 150, None,
              pygame.Color("white")).draw(self.frame)
        return self.signal_to_change
