import itertools
import pygame

from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button


class Start(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.state = int()
        self.state_multiplier = 1
        self.yellowing = int()
        self.yellowing_surface = pygame.Surface((self.frame.get_width(), self.frame.get_height()))
        self.yellowing_surface.fill(self.r.color("autumn_yellow"))
        self.yellowing_surface.set_alpha(self.yellowing)
        self.threshold = 120
        self.threshold_step = 10
        self.fan = [self.r.drawable("fan_state_0"), self.r.drawable("fan_state_1")]
        self.add_time_event("change_fan", lambda: self.fan.insert(0, self.fan.pop()), 100)
        self.add_time_event("change_yellowing", self.change_yellowing, 50)
        self.state_description = [
            (self.r.drawable("start_background"), tuple()),
            (self.r.drawable("start_background_play"), (
                Button(self.r, r.string("new_game"), (1124, 640), self.new_game),
                Button(self.r, r.string("continue"), (1124, 1050), self.new_game),
                Button(self.r, r.string("reset"), (20, 20), self.hide_menu, True)
            )),
            (self.r.drawable("start_background_settings"), (
                Button(self.r, "Ничего", (0, 0), lambda: True),
            )),
            (self.r.drawable("start_background_achievements"), (
                Button(self.r, "Ничего", (0, 0), lambda: True),
            ))
        ]

    def hide_menu(self):
        self.state_multiplier = 0

    def new_game(self):
        self.signal_to_change = "continue"

    def change_yellowing(self):
        if self.state * self.state_multiplier:
            if self.yellowing < self.threshold:
                self.yellowing += self.threshold_step
        else:
            if self.yellowing > 0:
                self.yellowing -= self.threshold_step

    def button_pressed(self, key):
        if key == pygame.K_DOWN:
            self.state += 1
        elif key == pygame.K_UP:
            self.state -= 1
        self.state %= 4
        self.state_multiplier = 1

    def mouse_moved(self, pos):
        for button in self.state_description[self.state][-1]:
            button.check_focus(pos)

    def mouse_pressed(self, button, pos):
        if button == 1:
            for elem in itertools.chain(*map(lambda elem: elem[-1], self.state_description)):
                elem.click()

    def update(self):
        self.frame.blit(self.state_description[self.state][0], (0, 0))
        self.frame.blit(self.fan[0], (0, 0))
        self.yellowing_surface.set_alpha(self.yellowing)
        if self.state * self.state_multiplier:
            self.frame.blit(self.yellowing_surface, (0, 0))
            for button in self.state_description[self.state][-1]:
                button.draw(self.frame)
        else:
            self.frame.blit(self.yellowing_surface, (0, 0))
        return self.signal_to_change
