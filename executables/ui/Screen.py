import pygame


class Screen:
    def __init__(self, r, frame, with_darking=True):
        self.r = r
        self.frame = frame
        self.time_events = {pygame.USEREVENT: ("blank", 1987, lambda: True)}
        self.darking_surface = pygame.Surface(self.frame.get_size())
        if with_darking:
            self.darking_surface.set_alpha(255)
            self.add_time_event("darking", self.darking, 10)
        else:
            self.darking_surface.set_alpha(0)
        self.signal_to_change = None

    def darking(self):
        if self.darking_surface.get_alpha() != 0:
            self.darking_surface.set_alpha(self.darking_surface.get_alpha() - 1)
        else:
            self.remove_time_event("darking")

    def set_signal(self, signal):
        self.signal_to_change = signal

    def add_time_event(self, name, action, period):
        self.time_events[next(reversed(self.time_events.keys())) + 1] = name, period, action
        pygame.time.set_timer(next(reversed(self.time_events.keys())), period)

    def remove_time_event(self, name):
        try:
            key_for_removement = next(key for key, (na, _, _) in self.time_events.items() if na == name)
        except StopIteration:
            return
        pygame.time.set_timer(key_for_removement, 0)
        del self.time_events[key_for_removement]

    def handle_time_event(self, event):
        self.time_events[event][-1]()

    def button_pressed(self, key):
        pass

    def button_released(self, key):
        pass

    def mouse_moved(self, pos):
        pass

    def mouse_pressed(self, button, pos):
        pass

    def mouse_released(self, button):
        pass

    def mouse_wheel(self, direction):
        pass

    def update(self):
        pass
