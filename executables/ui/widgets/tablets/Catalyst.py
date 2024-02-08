from executables.ui.widgets.InteractiveWidget import InteractiveWidget


class Catalyst(InteractiveWidget):
    def __init__(self, r):
        super().__init__(r, (0, 0), lambda: True)
        self.compos_x, self.compos_y = int(), int()
        self.description = str()
        self.calculate_size()

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
