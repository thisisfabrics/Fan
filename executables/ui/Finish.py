from executables.ui.Screen import Screen
from executables.ui.widgets.Label import Label


class Finish(Screen):
    def __init__(self, r, frame):
        super().__init__(r, frame)
        self.frame.fill("black")
        self.alpha = 0
        self.image = self.r.drawable("finish")
        self.image.set_alpha(0)
        self.add_time_event("increase_alpha", self.increase_alpha, 100)
        self.label_about_destructions, self.label_about_floors = self.r.query("SELECT liquidated_enemies, floor FROM "
                                                                              "statistics WHERE is_finished = 0")
        self.r.query("UPDATE statistics SET is_finished = 1")
        self.r.database.commit()
        self.label_about_destructions = Label(self.r, )

    def increase_alpha(self):
        self.alpha += 1
        if self.alpha == 100:
            self.remove_time_event("increase_alpha")
        self.image.set_alpha(self.alpha)

    def update(self):
        self.frame.blit(self.image, (0, 0))
