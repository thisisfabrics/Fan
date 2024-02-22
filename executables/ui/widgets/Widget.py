class Widget:
    def __init__(self, r, pos):
        self.r = r
        self.x, self.y = int(), int()
        self.set_pos(pos)

    def calculate_size(self):
        self.xx, self.yy = (self.x + self.image.get_width(),
                            self.y + self.image.get_height())

    def set_pos(self, pos):
        self.x, self.y = map(lambda elem: elem * self.r.constant("coefficient"), pos)

    def build_surface(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
