from executables.rooms.obstacles.portals.Portal import Portal


class Shop(Portal):
    def __init__(self, r, room_size, *sprites_group):
        super().__init__(r, room_size, *sprites_group)
        self.image = self.r.drawable("shop")
