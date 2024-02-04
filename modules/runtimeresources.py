import os
import sqlite3
import pygame


class R:
    def __init__(self, useful_size, real_size):
        self.database = sqlite3.connect("../data/script.sqlite")
        self.query = self.database.cursor().execute
        self.useful_size = useful_size
        self.real_size = real_size
        self.coefficient = useful_size[0] / 3840
        self.language = str()
        self.observe_language()
        self.drawable_dictionary = dict()
        self.reload_drawables()
        self.string_dictionary = dict()
        self.reload_strings()
        self.constant_dictionary = {
            "coefficient": self.coefficient,
            "useful_width": self.useful_size[0],
            "useful_height": self.useful_size[1],
            "real_offset_y": abs(self.useful_size[1] - self.real_size[1]) / 2,
            "real_offset_x": abs(self.useful_size[0] - self.real_size[0]) / 2,
        }
        self.color_dictionary = {
            "autumn_yellow": pygame.Color(194, 102, 41),
            "air_bullet_filling": pygame.Color(160, 144, 137)
        }

    def observe_language(self):
        self.language = self.query("SELECT language FROM settings").fetchall()[0][0]

    def reload_strings(self):
        self.observe_language()
        for key, value in map(lambda elem: elem.strip().split(',', 1),
                              open(f"../data/media/strings/{self.language}.csv", 'r', encoding="utf-8")):
            self.string_dictionary[key] = value

    def reload_drawables(self):
        self.observe_language()
        for elem in os.listdir(directory := f"../data/media/images/{self.language}"):
            self.drawable_dictionary[elem.split('.')[0]] = pygame.transform.smoothscale(
                (im := pygame.image.load(f"{directory}/{elem}")),
                (im.get_width() * self.coefficient, im.get_height() * self.coefficient))
        for elem in os.listdir(directory := "../data/media/images"):
            if '.' not in elem:
                continue
            self.drawable_dictionary[elem.split('.')[0]] = pygame.transform.smoothscale(
                (im := pygame.image.load(f"{directory}/{elem}")),
                (im.get_width() * self.coefficient, im.get_height() * self.coefficient))

    def drawable(self, name):
        return self.drawable_dictionary[name]

    def constant(self, name):
        return self.constant_dictionary[name]

    def string(self, name):
        return self.string_dictionary[name]

    def color(self, name):
        return self.color_dictionary[name]
