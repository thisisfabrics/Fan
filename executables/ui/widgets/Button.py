import pygame


class Button:
    def __init__(self, r, label, pos, action, is_icon=False):
        self.r = r
        self.is_icon = is_icon
        self.padding = 20 * self.r.constant("coefficient")
        self.x, self.y = map(lambda elem: elem * self.r.constant("coefficient"), pos)
        self.action = action
        self.focus = False
        self.label = pygame.font.Font("../data/media/fonts/AmaticSC-Regular.ttf",
                                      int(125 * self.r.constant("coefficient"))) \
            .render(label, 1, pygame.Color("black"))
        self.chuncks = int()
        self.xx, self.yy = int(), int()
        self.calculate_size()

    def calculate_size(self):
        if self.focus:
            string_start = "button_focused"
        else:
            string_start = "button_unfocused"
        addition = sum(self.r.drawable(elem).get_width() for elem in
                       (f"{string_start}_left_cap", f"{string_start}_right_cap"))
        self.chuncks = not self.is_icon + self.label.get_width() // ((wi := self.r.drawable(string_start).get_width()) +
                                                                     addition - int(self.padding * 2))
        self.xx = self.x + addition + self.chuncks * wi
        self.yy = self.y + self.r.drawable(string_start).get_height()

    def check_focus(self, pos):
        pos_x, pos_y = pos
        if self.x <= pos_x <= self.xx and self.y <= pos_y + self.r.constant("real_offset") <= self.yy:
            self.focus = True
        else:
            self.focus = False
        self.calculate_size()

    def click(self):
        if self.focus:
            self.action()

    def build_surface(self):
        surface = pygame.Surface((self.xx - self.x, self.yy - self.y), pygame.SRCALPHA, 32)
        if self.focus:
            string_start = "button_focused"
        else:
            string_start = "button_unfocused"
        left_cap = self.r.drawable(f"{string_start}_left_cap")
        surface.blit(left_cap, (0, 0))
        for i in range(self.chuncks):
            surface.blit(self.r.drawable(string_start), (left_cap.get_width() +
                                                         self.r.drawable(string_start).get_width() * i, 0))
        surface.blit(self.r.drawable(f"{string_start}_right_cap"),
                     (left_cap.get_width() + self.r.drawable(string_start).get_width() * self.chuncks, 0))
        surface.blit(self.label, (surface.get_width() * 0.5 - self.label.get_width() * 0.5,
                                  surface.get_height() * 0.5 - self.label.get_height() * 0.5))
        return surface
