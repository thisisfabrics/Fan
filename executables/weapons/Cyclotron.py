from executables.bullets.AlphaParticle import AlphaParticle
from executables.weapons.Weapon import Weapon


class Cyclotron(Weapon):
    def __init__(self, r, pos, animation_name, animation_period):
        super().__init__(r, pos, animation_name, animation_period)
        self.bullet = AlphaParticle
        self.offset_not_flipped = -70 * self.r.constant("coefficient"), 270 * self.r.constant("coefficient")
        self.offset_flipped = 70 * self.r.constant("coefficient"), self.offset_not_flipped[1]
        self.apply_offset()
        self.timeout = 200
        self.description = self.r.string("cyclotron")

