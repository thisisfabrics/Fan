import itertools

import pygame

from executables.entities.Belle import Belle
from executables.entities.Entity import Entity


class Enemy(Entity):
    def __init__(self, r, animation_name, animation_period, *sprite_groups):
        super().__init__(r, animation_name, animation_period, *sprite_groups)
        self.destination = int(), int()
        self.location = int(), int()
        self.clock = pygame.time.Clock()
        self.map = list()
        self.field_size = (int(), int())

    def set_destination(self, entity):
        self.destination = entity.rect.x + entity.rect.width // 2, entity.rect.y + entity.rect.height // 2
        self.destination = (self.destination[0] // int(.045 * self.field_size[0]),
                            self.destination[1] // int(.08 * self.field_size[1]))
        self.location = self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2
        self.location = (self.location[0] // int(.045 * self.field_size[0]),
                         self.location[1] // int(.08 * self.field_size[1]))

    def move(self, count):
        x, y, *_ = self.rect
        for i in range(int(count)):
            self.step()
        self.last_delta_x = self.rect.x - x
        self.last_delta_y = self.rect.y - y

    def step(self):
        pass

    def form_map(self, *groups):
        group = pygame.sprite.Group()
        for elem in itertools.chain(*map(lambda el: el.sprites(), groups)):
            if elem is not self and not isinstance(elem, Belle):
                group.add(elem)
        self.map = list()
        for i in range(self.field_size[1])[::int(.08 * self.field_size[1])]:
            self.map.append(list())
            for j in range(self.field_size[0])[::int(.045 * self.field_size[0])]:
                minisprite = pygame.sprite.Sprite()
                minisprite.rect = pygame.Rect(j, i, 1, 1)
                self.map[-1].append(bool(pygame.sprite.spritecollideany(minisprite, group)))

    def update(self, rooms_obstacles, rooms_entities, field_size):
        super().update()
        self.field_size = field_size
        belle = next(filter(lambda elem: isinstance(elem, Belle), rooms_entities.sprites()))
        self.form_map(rooms_obstacles, rooms_entities)
        self.set_destination(belle)
        self.move(self.clock.tick() * self.speed)
