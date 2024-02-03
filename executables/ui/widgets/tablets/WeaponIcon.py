import pygame.mouse

from executables.ui.widgets.InteractiveWidget import InteractiveWidget


class WeaponIcon(InteractiveWidget):
    def __init__(self, r, pos, name, powers, mouse_pos, action):
        super().__init__(r, pos, action)
        self.image = self.r.drawable(name.lower())
        self.calculate_size()
        label = (pygame.font.Font("../data/media/fonts/AmaticSC-Bold.ttf", int(80 * self.r.constant("coefficient")))
                 .render(f"{self.r.string("level")}"
                         f"{self.r.string("max") if powers[0] == powers[1] else ""}"
                         f"{self.r.string("min") if powers[0] == 1 else ""}: {int(powers[0])}", 1, pygame.Color("black")))
        surf = pygame.Surface((self.xx - self.x + label.get_width() + 120 * self.r.constant("coefficient"),
                               self.yy - self.y), pygame.SRCALPHA)
        surf.blit(self.image, (0, 0))
        surf.blit(label, (self.image.get_width() + 120 * self.r.constant("coefficient"), 0))
        self.image = surf
        self.check_focus(mouse_pos)
        if pygame.mouse.get_pressed()[0]:
            self.click()
