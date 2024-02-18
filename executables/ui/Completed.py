import math

import pygame.mouse

from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button
from executables.ui.widgets.Label import Label


class Completed(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.images = [self.r.drawable("completed_0"), self.r.drawable("completed_1"), self.r.drawable("completed_2")]
        self.images.extend(self.images[-2:-len(self.images):-1])
        self.add_time_event("animation", lambda: self.images.insert(0, self.images.pop()), 150)
        self.position = -self.r.constant("useful_height")
        self.add_time_event("moving", lambda: self.move(0), 35)
        self.step = 150 * self.r.constant("coefficient")
        self.previous_floor = self.r.query("SELECT number FROM floor ").fetchall()[0][0]  # if False else 10
        self.label = Label(self.r, self.r.string("floor_is_cleared").replace('%', str(self.previous_floor)),
                           (40, 500), 300, 500, "white")
        self.buttons = (
            Button(self.r, self.r.string("to_the_floor").replace('%', str(self.previous_floor - 1)), (80, 1400),
                   lambda: self.add_time_event("moving", lambda: self.move(self.r.constant("useful_height")), 35)),
            Button(self.r, self.r.string("save_and_quit"), (80, 1750), lambda: self.set_signal("start"))
        )

    def set_signal(self, signal):
        self.signal_to_change = signal

    def mouse_pressed(self, button, pos):
        if button == 1:
            for elem in self.buttons:
                elem.click()

    def move(self, barier):
        if self.position < barier:
            self.position -= min(-1, self.step * -abs(math.sin(self.position / self.r.constant("useful_height"))))
        else:
            self.remove_time_event("moving")
            if self.position >= self.r.constant("useful_height"):
                self.prepare_next_level()
                self.set_signal("continued")

    def prepare_next_level(self):
        self.r.query(f"UPDATE floor SET number = {self.previous_floor - 1}")
        self.r.database.commit()

    def update(self):
        self.frame.fill("black")
        surface = pygame.Surface(self.frame.get_rect()[-2:])
        surface.blit(self.images[0], (0, 0))
        self.label.draw(surface)
        for elem in self.buttons:
            elem.check_focus(pygame.mouse.get_pos())
            elem.draw(surface)
        self.frame.blit(surface, (0, self.position))
        return self.signal_to_change
