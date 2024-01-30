import pygame.mouse

from executables.ui.widgets.InteractiveWidget import InteractiveWidget


class WeaponIcon(InteractiveWidget):
    def __init__(self, r, pos, name, mouse_pos, action):
        super().__init__(r, pos, action)
        self.image = self.r.drawable(name.lower())
        self.calculate_size()
        self.check_focus(mouse_pos)
        if pygame.mouse.get_pressed()[0]:
            self.click()
