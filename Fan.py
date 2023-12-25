import sys
import pygame
import runtimeresources

pygame.init()
fps = 30
left_corner_x = left_corner_y = 0
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
useful_width, useful_height = int(), int()
frame = pygame.Surface((0, 0))
aspect_ratio = 16 / 9
r = None


class Screen:
    def __init__(self):
        self.time_events = dict()

    def send_events_to_timeline(self):
        for event, (period, _) in self.time_events.items():
            pygame.time.set_timer(event, period)

    def handle_time_event(self, event):
        self.time_events[event][-1]()


class Button:
    def __init__(self, label, action, x, y):
        coefficient = useful_width / 3840
        self.x, self.y, self.action = x * coefficient, y * coefficient, action
        self.focus = False
        self.label = pygame.font.Font("data/media/fonts/AmaticSC-Regular.ttf", 45) \
            .render(label, 1, pygame.Color("black"))
        self.chuncks = int()
        self.xx, self.yy = int(), int()
        self.calculate_size()

    def calculate_size(self):
        if self.focus:
            string_start = "button_focused"
        else:
            string_start = "button_unfocused"
        addition = sum(r.drawable(elem).get_width() for elem in
                       (f"{string_start}_left_cap", f"{string_start}_right_cap"))
        self.chuncks = 1 + self.label.get_width() // (wi := r.drawable(string_start).get_width())
        self.xx = self.x + addition + self.chuncks * wi
        self.yy = self.y + max(r.drawable(elem).get_height() for elem in
                               (f"{string_start}_left_cap", f"{string_start}_right_cap", string_start))

    def check_focus(self, pos):
        pos_x, pos_y = pos
        if self.x <= pos_x <= self.xx and self.y <= pos_y <= self.yy:
            self.focus = True
        else:
            self.focus = False
        self.calculate_size()

    def build_surface(self):
        surface = pygame.Surface((self.xx - self.x, self.yy - self.y), pygame.SRCALPHA, 32)
        if self.focus:
            string_start = "button_focused"
        else:
            string_start = "button_unfocused"
        left_cap = r.drawable(f"{string_start}_left_cap")
        surface.blit(left_cap, (0, 0))
        surface.blit((prev := r.drawable(string_start)), (left_cap.get_width(), 0))
        for i in range(1, self.chuncks):
            surface.blit(r.drawable(string_start), (left_cap.get_width() + prev.get_width() * i, 0))
        surface.blit(r.drawable(f"{string_start}_right_cap"),
                     (left_cap.get_width() + prev.get_width() * self.chuncks, 0))
        surface.blit(self.label, (surface.get_width() * 0.5 - self.label.get_width() * 0.5,
                                  surface.get_height() * 0.5 - self.label.get_height() * 0.5))
        return surface


class Start(Screen):
    def __init__(self):
        super().__init__()
        self.fan = [r.drawable("fan_state_0"), r.drawable("fan_state_1")]
        self.time_events[pygame.USEREVENT + 1] = (100, self.change_fan)
        self.send_events_to_timeline()
        self.state = int()
        self.state_description = [
            (r.drawable("start_background"), False, tuple()),
            (r.drawable("start_background_play"), True, (Button("Новая игра", self.new_game, 172, 121),
                                                         Button("Продолжить", self.new_game, 172, 521))),
            (r.drawable("start_background_settings"), True, tuple()),
            (r.drawable("start_background_achievements"), True, tuple())
        ]
        self.yellowing = int()
        self.yellowing_surface = pygame.Surface((useful_width, useful_height))
        self.yellowing_surface.fill(pygame.Color(194, 102, 41))
        self.yellowing_surface.set_alpha(self.yellowing)
        self.threshold = 120
        self.threshold_step = 10

    def new_game(self):
        pass

    def change_fan(self):
        self.fan.insert(0, self.fan.pop())

    def button_pressed(self, key):
        if key == pygame.K_DOWN:
            self.state += 1
        elif key == pygame.K_UP:
            self.state -= 1
        self.state %= 4

    def mouse_moved(self, pos):
        for button in self.state_description[self.state][-1]:
            button.check_focus(pos)

    def update(self):
        frame.blit(self.state_description[self.state][0], (0, 0))
        frame.blit(self.fan[0], (0, 0))
        if self.state_description[self.state][1]:
            if self.yellowing < self.threshold:
                self.yellowing += self.threshold_step
            self.yellowing_surface.set_alpha(self.yellowing)
            frame.blit(self.yellowing_surface, (0, 0))
            for button in self.state_description[self.state][-1]:
                frame.blit(button.build_surface(), (button.x, button.y))
        else:
            if self.yellowing > 0:
                self.yellowing -= self.threshold_step
            self.yellowing_surface.set_alpha(self.yellowing)
            frame.blit(self.yellowing_surface, (0, 0))


def configure_frame():
    global useful_width, useful_height, left_corner_y, left_corner_x, frame, r
    window_width, window_height = (info := pygame.display.Info()).current_w, info.current_h
    useful_width, useful_height = window_width, window_height
    if window_width / window_height != aspect_ratio:
        if window_width > window_height:
            useful_width = aspect_ratio * window_height
            left_corner_x = 0.5 * info.current_w - 0.5 * useful_width
        else:
            useful_height = window_width / aspect_ratio
            left_corner_y = 0.5 * info.current_h - 0.5 * useful_height
    frame = pygame.Surface((useful_width, useful_height))
    r = runtimeresources.R((useful_width, useful_height))


def main():
    configure_frame()
    current_screen = Start()
    clock = pygame.time.Clock()
    playtime = True
    while playtime:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    playtime = False
                else:
                    current_screen.button_pressed(event.key)
            elif event.type in current_screen.time_events:
                current_screen.handle_time_event(event.type)
            elif event.type == pygame.MOUSEMOTION:
                current_screen.mouse_moved(event.pos)
        current_screen.update()
        window.blit(frame, (left_corner_x, left_corner_y))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
