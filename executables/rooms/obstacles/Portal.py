from executables.rooms.obstacles.Obstacle import Obstacle


class Portal(Obstacle):
    def __init__(self, r, room_size, *sprite_groups):
        super().__init__(r, *sprite_groups)
        self.image = self.r.drawable("portal")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = room_size[1] // 2 - self.rect.height // 2

    def draw(self, surface):
        surface.blit(self.image, self.rect[:2])
