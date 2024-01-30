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
        self.padding = 106 * self.r.constant("coefficient")

    def calculate_size(self):
        self.xx, self.yy = self.x + self.width, self.y + self.height

    def append(self, widget):
        # 106 between items
        if self.items:
            widget.x = len(self.items) % 4 * (self.items[0].image.get_width() + self.padding)
            widget.y = self.current_height() - self.items[0].image.get_height()
        widget.y += self.scrollstate
        self.items.append(widget)

    def scroll(self, direction):
        if self.focus and self.current_height() > self.height:
            delta = -direction * 50 * self.r.constant("coefficient")
            self.scrollstate -= delta
            if -self.current_height() + 2 * self.items[0].image.get_height() + self.padding <= self.scrollstate <= 0:
                for elem in self.items:
                    elem.y -= delta
                    elem.calculate_size()
            else:
                self.scrollstate += delta

    def current_height(self):
        return len(self.items) // 4 * (self.items[0].image.get_height() + self.padding) + \
            self.items[0].image.get_height() if self.items else int()

    def build_surface(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        for elem in self.items:
            elem.draw(surface)
        self.image = surface

    def draw(self, surface):
        self.build_surface()
        super().draw(surface)

