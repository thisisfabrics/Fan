from executables.ui.widgets.Widget import Widget


class InteractiveWidget(Widget):
    def __init__(self, r, pos, action):
        super().__init__(r, pos)
        self.action = action
        self.focus = False
        self.xx, self.yy = int(), int()

    def calculate_size(self):
        pass

    def check_focus(self, pos):
        pos_x, pos_y = pos
        if self.x <= pos_x - self.r.constant("real_offset_x") <= self.xx and \
                self.y <= pos_y - self.r.constant("real_offset_y") <= self.yy:
            self.focus = True
        else:
            self.focus = False
        self.calculate_size()

    def click(self):
        if self.focus:
            self.action()