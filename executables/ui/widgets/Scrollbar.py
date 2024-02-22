import pygame

from executables.ui.widgets.InteractiveWidget import InteractiveWidget


class Scrollbar(InteractiveWidget):
    def __init__(self, r, pos, action, width=None, height=None):
        super().__init__(r, pos, action)
        self.width = width * self.r.constant("coefficient") if width else self.r.constant("useful_width")
        self.height = height * self.r.constant("coefficient") if height else self.r.constant("useful_height")
        self.calculate_size()
        self.items = list()
        self.scrollstate = int()
        self.image = pygame.Surface((0, 0))

    def enumerate_classes(self):
        return [elem.__class__ for elem in self.items]

    def calculate_size(self):
        self.xx, self.yy = self.x + self.width, self.y + self.height

    def append(self, widget, with_internal_structure=False):
        if with_internal_structure and self.items:
            widget.y = self.items[-1].yy + self.r.constant("scrollbar_padding")
        widget.y += self.scrollstate
        widget.calculate_size()
        self.items.append(widget)

    def scroll(self, direction):
        delta = -direction * 100 * self.r.constant("coefficient")
        if self.focus and self.r.constant("scrollbar_padding") > self.items[0].y - delta and \
                self.height - self.r.constant("scrollbar_padding") * 2 < self.items[-1].yy - delta:
            self.scrollstate -= delta
            for elem in self.items:
                elem.y -= delta
                elem.calculate_size()

    def build_surface(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        for elem in self.items:
            elem.compos_x, elem.compos_y = self.x, self.y
            elem.draw(surface)
        self.image = surface

    def draw(self, surface):
        self.build_surface()
        super().draw(surface)

