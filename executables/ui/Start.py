import itertools
import pygame

from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button
from executables.ui.widgets.Label import Label
from executables.ui.widgets.Scrollbar import Scrollbar
from executables.ui.widgets.tablets.Achievement import Achievement


class Start(Screen):
    def __init__(self, r, frame, update_fps_action):
        super().__init__(r, frame)
        self.game_actions = {
            "update_fps": update_fps_action
        }
        self.state = int()
        self.state_multiplier = 1
        self.alpha = int()
        self.darking_surface = pygame.Surface((self.frame.get_width(), self.frame.get_height()))
        self.darking_surface.fill(self.r.color("sad_gray"))
        self.darking_surface.set_alpha(self.alpha)
        self.threshold = 120
        self.threshold_step = 10
        self.fan = [self.r.drawable("fan_state_0"), self.r.drawable("fan_state_1")]
        self.add_time_event("change_fan", lambda: self.fan.insert(0, self.fan.pop()), 100)
        self.add_time_event("change_yellowing", self.change_yellowing, 50)
        self.state_description = list()
        self.describe_states()

    def describe_states(self):
        self.state_description = [
            (self.r.drawable("start_background"), tuple(), tuple()),
            (self.r.drawable("start_background_play"), (
                Button(self.r, self.r.string("new_game"), (1124, 640), self.new_game),
                Button(self.r, self.r.string("continue"), (1124, 1050), self.continued_game,
                       is_enabled=self.r.are_there_data()),
                Button(self.r, self.r.string("reset"), (20, 20), self.hide_menu, True)
            ), tuple()),
            (self.r.drawable("start_background_settings"), (
                Button(self.r, self.r.string("reset"), (20, 20), self.hide_menu, True),
                Button(self.r, self.r.string("plus"), (2300, 500), lambda: self.change_fps(1), True),
                Button(self.r, self.r.string("minus"), (2750, 500), lambda: self.change_fps(-1), True,
                       next(self.r.query("SELECT fps FROM settings"))[0] > 1),
                Button(self.r, "en", (2300, 800), lambda: self.change_language("en"), True,
                       next(self.r.query("SELECT language FROM settings"))[0] == "ru"),
                Button(self.r, "ru", (2750, 800), lambda: self.change_language("ru"), True,
                       next(self.r.query("SELECT language FROM settings"))[0] == "en"),
                Button(self.r, self.r.string("plus"), (2300, 1100), lambda: self.change_loudness("effects", 1), True,
                       next(self.r.query("SELECT effects FROM settings"))[0] < 100),
                Button(self.r, self.r.string("minus"), (2750, 1100), lambda: self.change_loudness("effects", -1), True,
                       next(self.r.query("SELECT effects FROM settings"))[0] > 0),
                Button(self.r, self.r.string("plus"), (2300, 1400), lambda: self.change_loudness("music", 1), True,
                       next(self.r.query("SELECT music FROM settings"))[0] < 100),
                Button(self.r, self.r.string("minus"), (2750, 1400), lambda: self.change_loudness("music", -1), True,
                       next(self.r.query("SELECT music FROM settings"))[0] > 0),
                Button(self.r, self.r.string("plus"), (2300, 1700), lambda: self.change_loudness("characters", 1), True,
                       next(self.r.query("SELECT characters FROM settings"))[0] < 108),
                Button(self.r, self.r.string("minus"), (2750, 1700), lambda: self.change_loudness("characters", -1), True,
                       next(self.r.query("SELECT characters FROM settings"))[0] > 0),
            ), (
                 Label(self.r, self.r.string("fps"), (500, 500), 250, None, "white"),
                 Label(self.r, str(next(self.r.query("SELECT fps FROM settings"))[0]), (1800, 500), 250, None, "white"),
                 Label(self.r, self.r.string("language"), (500, 800), 250, None, "white"),
                 Label(self.r, self.r.string("effects_loudness"), (500, 1100), 250, None, "white"),
                 Label(self.r, str(next(self.r.query("SELECT effects FROM settings"))[0]),
                       (1800, 1100), 250, None, "white"),
                 Label(self.r, self.r.string("music_volume"), (500, 1400), 250, None, "white"),
                 Label(self.r, str(next(self.r.query("SELECT music FROM settings"))[0]),
                       (1800, 1400), 250, None, "white"),
                 Label(self.r, self.r.string("difficulty"), (500, 1700), 125, 800, "white"),
                 Label(self.r, str(next(self.r.query("SELECT characters FROM settings"))[0]),
                       (1800, 1700), 250, None, "white")
             )),
            (self.r.drawable("start_background_achievements"), (
                Button(self.r, self.r.string("reset"), (20, 20), self.hide_menu, True),
                Button(self.r, self.r.string("clear_statistics"), (2600, 1800), self.clear_statistics)
            ), (
                Label(self.r, self.r.string("actual_statistics"), (2000, 88), 250, None, "white"),
                Scrollbar(self.r, (1920, 388), lambda: True, 1920, 1772),
                Scrollbar(self.r, (440, 0), lambda: True, 1480)
            ))
        ]
        self.state_description[-1][-1][-1].scrollstate = 20 * self.r.constant("coefficient")
        for icon, description, condition in [
            (self.r.drawable("achievement_catterfield"), self.r.string("achievement_catterfield"),
             self.r.query("SELECT * FROM statistics WHERE liquidated_enemies > 99").fetchall()),
            (self.r.drawable("achievement_dischargers"), self.r.string("achievement_dischargers"),
             self.r.query("SELECT * FROM statistics WHERE weapons = 3").fetchall()),
            (self.r.drawable("achievement_floor"), self.r.string("achievement_floor"),
             self.r.query("SELECT * FROM statistics WHERE floor < 1").fetchall())
        ]:
            self.state_description[-1][-1][-1].append(Achievement(self.r, (0, 0), condition, icon, description), True)
        for _, weapons, liquidated_enemies, activated_catalysts, floor, year, month, day, is_finished in \
                self.r.query("SELECT * FROM statistics ORDER BY year, month, day DESC"):
            self.state_description[-1][-1][-2].append(
                Label(self.r, self.r.string("reached_floor").replace('%', str(floor)),
                      (0, 0), 100, None, "white"), True)
            self.state_description[-1][-1][-2].append(
                Label(self.r, self.r.string("collected_dischargers").replace('%', str(weapons)),
                      (0, 0), 100, None, "white"), True)
            self.state_description[-1][-1][-2].append(
                Label(self.r, self.r.string("liquidated_enemies").replace('%', str(liquidated_enemies)),
                      (0, 0), 100, None, "white"), True)
            self.state_description[-1][-1][-2].append(
                Label(self.r, self.r.string("activated_catalysts").replace('%', str(activated_catalysts)),
                      (0, 0), 100, None, "white"), True)
            self.state_description[-1][-1][-2].append(
                Label(self.r, self.r.string("date").replace('%', str(f"{day}.{month}.{year}")),
                      (0, 0), 100, None, "white"), True)
            self.state_description[-1][-1][-2].append(
                Label(self.r, self.r.string("is_finished").replace('%', self.r.string("yes")
                      if is_finished else self.r.string("no")), (0, 0), 100, None, "white"), True)
            self.state_description[-1][-1][-2].append(
                Label(self.r, "____________",
                      (0, 0), 100, None, "white"), True)

    def clear_statistics(self):
        self.r.query("DELETE FROM statistics WHERE is_finished = 1")
        self.r.database.commit()
        self.describe_states()

    def mouse_wheel(self, direction):
        if self.state == 3:
            self.state_description[-1][-1][-1].scroll(direction)
            self.state_description[-1][-1][-2].scroll(direction)

    def mouse_moved(self, pos):
        self.state_description[-1][-1][-1].check_focus(pos)
        self.state_description[-1][-1][-2].check_focus(pos)

    def change_language(self, code):
        self.r.query(f"UPDATE settings SET language = '{code}'")
        self.r.database.commit()
        self.r.reload_strings()
        self.r.reload_drawables()
        self.describe_states()

    def change_fps(self, side):
        self.r.query(f"UPDATE settings SET fps = fps + {side}")
        self.r.database.commit()
        self.game_actions["update_fps"]()
        self.describe_states()

    def change_loudness(self, option, side):
        self.r.query(f"UPDATE settings SET {option} = {option} + {side}")
        self.r.database.commit()
        self.describe_states()

    def hide_menu(self):
        self.state_multiplier = 0

    def new_game(self):
        self.signal_to_change = "continue"

    def continued_game(self):
        self.signal_to_change = "continued"

    def change_yellowing(self):
        if self.state * self.state_multiplier:
            if self.alpha < self.threshold:
                self.alpha += self.threshold_step
        else:
            if self.alpha > 0:
                self.alpha -= self.threshold_step

    def button_pressed(self, key):
        if key == pygame.K_DOWN:
            self.state += 1
        elif key == pygame.K_UP:
            self.state -= 1
        self.state %= 4
        self.state_multiplier = 1
        for element in self.state_description:
            for elem in element[1]:
                elem.focus = False

    def mouse_pressed(self, button, pos):
        if button == 1:
            for elem in itertools.chain(*map(lambda elem: elem[1], self.state_description)):
                elem.click()
        if pos != (0, 0):
            self.add_time_event("clicking", lambda: self.mouse_pressed(1, (0, 0)), 100)

    def mouse_released(self, button):
        self.remove_time_event("clicking")

    def update(self):
        self.frame.blit(self.state_description[self.state][0], (0, 0))
        self.frame.blit(self.fan[0], (0, 0))
        self.darking_surface.set_alpha(self.alpha)
        self.frame.blit(self.darking_surface, (0, 0))
        if self.state * self.state_multiplier:
            for button in self.state_description[self.state][1]:
                button.check_focus(pygame.mouse.get_pos())
                button.draw(self.frame)
            for label in self.state_description[self.state][2]:
                label.draw(self.frame)
        return self.signal_to_change
