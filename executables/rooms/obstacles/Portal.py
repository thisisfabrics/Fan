from executables.rooms.obstacles.Obstacle import Obstacle


class Portal(Obstacle):
    def __init__(self, r, room_size):
        super().__init__(r)
        self.image = self.r.drawable("portal")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = room_size[1] // 2 - self.rect.height // 2
