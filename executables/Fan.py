import sys
import pygame

from executables.ui.Continue import Continue
from executables.ui.Start import Start
from modules.runtimeresources import R


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.aspect_ratio = 16 / 9
        self.useful_width, self.useful_height = (info := pygame.display.Info()).current_w, info.current_h
        self.left_corner_y = int()
        if self.useful_width / self.useful_height != self.aspect_ratio:
            self.useful_height = self.useful_width / self.aspect_ratio
            self.left_corner_y = 0.5 * info.current_h - 0.5 * self.useful_height
        self.frame = pygame.Surface((self.useful_width, self.useful_height))
        self.r = R((self.useful_width, self.useful_height))
        self.fps = 60
        self.current_screen = Start(self.r, self.frame)
        self.clock = pygame.time.Clock()
        self.playtime = True
        self.loop()

    def navigate(self, destination):
        if destination:
            if destination == "continue":
                self.current_screen = Continue(self.r, self.frame)

    def loop(self):
        while self.playtime:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playtime = False
                    else:
                        self.current_screen.button_pressed(event.key)
                elif event.type == pygame.KEYUP:
                    self.current_screen.button_released(event.key)
                elif event.type in self.current_screen.time_events:
                    self.current_screen.handle_time_event(event.type)
                elif event.type == pygame.MOUSEMOTION:
                    self.current_screen.mouse_moved(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.current_screen.mouse_pressed(event.button)
            self.navigate(self.current_screen.update())
            self.window.blit(self.frame, (0, self.left_corner_y))
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    pygame.init()
    Game()
