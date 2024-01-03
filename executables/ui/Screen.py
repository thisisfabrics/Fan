import pygame


class Screen:
    def __init__(self, r, frame):
        self.r = r
        self.frame = frame
        self.time_events = dict()

    def add_time_event(self, name, action, period):
        self.time_events[pygame.USEREVENT + len(self.time_events)] = name, period, action
        pygame.time.set_timer(next(reversed(self.time_events.keys())), period)

    def handle_time_event(self, event):
        self.time_events[event][-1]()

    def button_pressed(self, key):
        pass

    def button_released(self, key):
        pass

    def mouse_moved(self, pos):
        pass

    def mouse_pressed(self, button):
        pass