import sqlite3

import pygame


class R:
    def __init__(self, useful_size):
        database = sqlite3.connect("data/script.sqlite")
        language = database.cursor().execute("SELECT language FROM settings").fetchall()[0][0]
        coefficient = useful_size[0] / 3840
        database.close()
        self.drawable_dictionary = {
            "fan_state_0": pygame.transform.smoothscale(
                pygame.image.load(f"data/media/images/{language}/fan_state_0.png"), useful_size),
            "fan_state_1": pygame.transform.smoothscale(
                pygame.image.load(f"data/media/images/{language}/fan_state_1.png"), useful_size),
            "start_background": pygame.transform.smoothscale(
                pygame.image.load(f"data/media/images/{language}/start_background.png"), useful_size),
            "start_background_achievements": pygame.transform.smoothscale(
                pygame.image.load(f"data/media/images/{language}/start_background_achievements.png"), useful_size),
            "start_background_play": pygame.transform.smoothscale(
                pygame.image.load(f"data/media/images/{language}/start_background_play.png"), useful_size),
            "start_background_settings": pygame.transform.smoothscale(
                pygame.image.load(f"data/media/images/{language}/start_background_settings.png"), useful_size),
            "button_unfocused": pygame.transform.smoothscale(
                (i := pygame.image.load("data/media/images/button_unfocused.png")),
                (i.get_width() * coefficient, i.get_height() * coefficient)),
            "button_unfocused_left_cap": pygame.transform.smoothscale(
                (i := pygame.image.load("data/media/images/button_unfocused_left_cap.png")),
                (i.get_width() * coefficient, i.get_height() * coefficient)),
            "button_unfocused_right_cap": pygame.transform.smoothscale(
                (i := pygame.image.load("data/media/images/button_unfocused_right_cap.png")),
                (i.get_width() * coefficient, i.get_height() * coefficient)),
            "button_focused": pygame.transform.smoothscale(
                (i := pygame.image.load("data/media/images/button_focused.png")),
                (i.get_width() * coefficient, i.get_height() * coefficient)),
            "button_focused_left_cap": pygame.transform.smoothscale(
                (i := pygame.image.load("data/media/images/button_focused_left_cap.png")),
                (i.get_width() * coefficient, i.get_height() * coefficient)),
            "button_focused_right_cap": pygame.transform.smoothscale(
                (i := pygame.image.load("data/media/images/button_focused_right_cap.png")),
                (i.get_width() * coefficient, i.get_height() * coefficient)),
        }

    def drawable(self, name):
        return self.drawable_dictionary[name]



