import itertools

import pygame

from executables.entities.Belle import Belle
from executables.entities.Entity import Entity


class Enemy(Entity):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(r, animation_name, animation_period, *sprite_groups)
        self.destination = int(), int()
        self.location = int(), int()
        self.emergency_destination = int(), int()
        self.clock = pygame.time.Clock()
        self.map = list()
        self.field_size = (int(), int())
        self.chunk_width = int()
        self.chunk_height = int()
        self.offsets = tuple((elem, el) for el in (-1, 1, 0) for elem in (-1, 1, 0) if el or elem)

    def set_destination(self, entity):
        self.destination = entity.rect.x + entity.rect.width // 2, entity.rect.y + entity.rect.height // 2
        self.destination = self.destination[1] // self.chunk_height, self.destination[0] // self.chunk_width
        if not self.map[self.destination[0]][self.destination[1]]:
            self.emergency_destination = self.destination

    def set_location(self):
        self.location = self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2
        self.location = self.location[1] // self.chunk_height, self.location[0] // self.chunk_width

    def move(self, length):
        self.step(length)

    def step(self, length):
        destination_pos = self.chunck_to_pos(self.next_chunk())
        delta_x = destination_pos[0] - self.chunck_to_pos(self.location)[0]
        delta_y = destination_pos[1] - self.chunck_to_pos(self.location)[1]
        x_movement = (delta_x ** 2 * length ** 2 / (delta_y ** 2 + delta_x ** 2)) ** 0.5 if delta_y else length
        y_movement = abs(x_movement * delta_y / delta_x) if delta_x else length
        x_movement *= (1 if delta_x > 0 else -1)
        y_movement *= (1 if delta_y > 0 else -1)
        self.last_delta_x = x_movement
        self.last_delta_y = y_movement
        self.x += self.last_delta_x
        self.y += self.last_delta_y
        self.rect.x = self.x
        self.rect.y = self.y

    def chunck_to_pos(self, chunk):
        return (chunk[1] * self.chunk_width + self.chunk_width // 2,
                chunk[0] * self.chunk_height + self.chunk_height // 2)

    def next_chunk(self, emergency=False):
        prevs = [[None] * len(self.map[0]) for i in range(len(self.map))]
        queue = [self.location]
        while queue:
            y, x = queue.pop(0)
            for y_offset, x_offset in self.offsets:
                if 0 <= y + y_offset < len(self.map) and 0 <= x + x_offset < len(self.map[0]) and \
                        prevs[y + y_offset][x + x_offset] is None and not self.map[y + y_offset][x + x_offset]:
                    prevs[y + y_offset][x + x_offset] = y, x
                    queue.append((y + y_offset, x + x_offset))
        if prevs[self.destination[0]][self.destination[1]]:
            y, x = self.destination
            while prevs[y][x] != self.location:
                y, x = prevs[y][x]
            return y, x
        else:
            if emergency:
                self.map = [[False] * len(self.map[0]) for i in range(len(self.map))]
            self.destination = self.emergency_destination
            return self.next_chunk(True)

    def form_map(self, belle, *groups):
        group = pygame.sprite.Group()
        for elem in itertools.chain(*map(lambda el: el.sprites(), groups)):
            if elem is not belle and elem is not self:
                if not pygame.sprite.collide_rect(elem, belle):
                    group.add(elem)
        self.map = list()
        for i in range(self.field_size[1])[::self.chunk_height]:
            self.map.append(list())
            for j in range(self.field_size[0])[::self.chunk_width]:
                minisprite = pygame.sprite.Sprite()
                minisprite.rect = pygame.Rect(j, i, self.chunk_width, self.chunk_height)
                self.map[-1].append(bool(pygame.sprite.spritecollideany(minisprite, group)))

    def add_damaging_bullet(self, bullet):
        super().add_damaging_bullet(bullet)
        if "damage" not in self.animation_name:
            self.set_animation(f"{self.animation_name.split('_')[0]}_damage", 100)

    def remove_damaging_bullet(self, bullet=None):
        super().remove_damaging_bullet(bullet)
        if "movement" not in self.animation_name and not len(self.damaging_bullets):
            self.set_animation(f"{self.animation_name.split('_')[0]}_movement", 200)

    def damage(self):
        for elem, (_, clock) in self.damaging_bullets.items():
            self.energy -= elem.damage_rate * clock.tick() / 1000

    def update(self, rooms_obstacles, rooms_entities, field_size):
        super().update()
        self.remove_damaging_bullet()
        self.damage()
        self.field_size = field_size
        self.chunk_width = int(.045 * self.field_size[0])
        self.chunk_height = int(.08 * self.field_size[1])
        belle = next(filter(lambda elem: isinstance(elem, Belle), rooms_entities.sprites()))
        self.form_map(belle, rooms_obstacles, rooms_entities)
        self.set_destination(belle)
        self.set_location()
        self.move(self.clock.tick() * self.speed)
