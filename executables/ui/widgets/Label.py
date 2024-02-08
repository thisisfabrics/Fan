import functools

import pygame.font

from executables.ui.widgets.Widget import Widget


class Label(Widget):
    def __init__(self, r, label, pos, size, width=None, color=None):
        super().__init__(r, pos)
        self.label = label
        self.color = color if color else pygame.Color("black")
        self.width = width * self.r.constant("coefficient") if width else self.r.constant("useful_width")
        self.size = int(size * self.r.constant("coefficient"))
        self.font = pygame.font.Font("../data/media/fonts/AmaticSC-Regular.ttf",
                                     self.size)
        self.image = None
        self.build_surface()

    def build_subsurface(self, wi, substring):
        surface = pygame.Surface((wi, substring[0].get_height()),
                                 pygame.SRCALPHA, 32)
        position = -(self.size // 2)
        for i, elem in enumerate(substring):
            surface.blit(elem, (position + self.size // 2, 0))
            position += elem.get_width() + self.size // 2
        return surface

    def build_surface(self):
        strings = list()
        substring = list()
        max_width = int()
        for word in self.label.split():
            entire_width = functools.reduce(lambda result, elem: result + elem.get_width() + self.size // 2, substring,
                                            int())
            if (wi := (string := self.font.render(word, 1, self.color)).get_width()) + entire_width \
                    <= self.width:
                substring.append(string)
                max_width = max(max_width, entire_width + wi)
            else:
                max_width = max(max_width, entire_width + wi)
                substring.append(string)
                strings.append(self.build_subsurface(max_width, substring))
                substring = list()
        if substring:
            strings.append(self.build_subsurface(max_width, substring))
        self.image = pygame.Surface((max_width, len(strings) * strings[0].get_height()), pygame.SRCALPHA, 32)
        for i, string in enumerate(strings):
            self.image.blit(string, (0, i * strings[0].get_height()))
