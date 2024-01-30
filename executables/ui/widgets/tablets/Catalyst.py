from executables.ui.widgets.InteractiveWidget import InteractiveWidget


class Catalyst(InteractiveWidget):
    def __init__(self, r, pos, compos):
        super().__init__(r, pos, lambda: True)
        self.compos_x, self.compos_y = map(lambda elem: elem * self.r.constant("coefficient"), compos)
        self.description = str()

    def calculate_size(self):
        self.xx, self.yy = (self.x + self.image.get_width(),
                            self.y + self.image.get_height())

    def check_focus(self, pos):
        self.x += self.compos_x
        self.y += self.compos_y
        self.xx += self.compos_x
        self.yy += self.compos_y
        super().check_focus(pos)
        self.x -= self.compos_x
        self.y -= self.compos_y
        self.xx -= self.compos_x
        self.yy -= self.compos_y
