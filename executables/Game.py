import sys
import pygame

from executables.ui.Continue import Continue
from executables.ui.Finish import Finish
from executables.ui.Start import Start
from executables.ui.Store import Store
from modules.runtimeresources import R


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((0, 0))  # , pygame.FULLSCREEN
        self.aspect_ratio = 16 / 9
        self.useful_width, self.useful_height = (info := pygame.display.Info()).current_w, info.current_h
        self.real_width, self.real_height = self.useful_width, self.useful_height
        self.left_corner_y, self.left_corner_x = int(), int()
        if self.useful_width < self.useful_height:
            if self.useful_width / self.useful_height != self.aspect_ratio:
                self.useful_height = self.useful_width / self.aspect_ratio
        else:
            if self.useful_width / self.useful_height != self.aspect_ratio:
                self.useful_width = self.useful_height / self.aspect_ratio
        self.left_corner_x = 0.5 * info.current_w - 0.5 * self.useful_width
        self.left_corner_y = 0.5 * info.current_h - 0.5 * self.useful_height
        self.frame = pygame.Surface((self.useful_width, self.useful_height))
        self.r = R((self.useful_width, self.useful_height), (self.real_width, self.real_height))
        self.fps = 60
        self.current_screen = Start(self.r, self.frame)
        self.clock = pygame.time.Clock()
        self.playtime = True
        self.loop()

    def navigate(self, destination):
        if destination:
            if destination == "start":
                self.current_screen = Start(self.r, self.frame)
            elif destination == "continue":
                self.current_screen = Continue(self.r, self.frame)
            elif destination == "continued":
                self.current_screen = Continue(self.r, self.frame, True)
            elif destination == "finish":
                self.current_screen = Finish(self.r, self.frame)
            elif destination == "store":
                self.current_screen = Store(self.r, self.frame)

    def loop(self):
        while self.playtime:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEWHEEL:
                    self.current_screen.mouse_wheel(event.y)
                elif event.type == pygame.KEYDOWN:
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
                    self.current_screen.mouse_pressed(event.button, event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.current_screen.mouse_released(event.button)
            self.navigate(self.current_screen.update())
            self.window.blit(self.frame, (self.left_corner_x, self.left_corner_y))
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    pygame.init()
    Game()
