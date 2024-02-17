from executables.ui.Screen import Screen


class Completed(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.images = [self.r.drawable("completed_0"), self.r.drawable("completed_1"), self.r.drawable("completed_2")]
        self.images.extend(self.images[-2:-len(self.images):-1])
        self.add_time_event("animation", lambda: self.images.insert(0, self.images.pop()), 150)

    def update(self):
        self.frame.blit(self.images[0], (0, 0))
