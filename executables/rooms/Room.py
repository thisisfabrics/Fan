import random

import pygame.sprite

from executables.rooms.obstacles.Fridge import Fridge


class Room:
    def __init__(self, r):
        self.r = r
        self.image = self.r.drawable("tiles")
        self.obstacles_group = pygame.sprite.Group()
        self.entities = list()
        self.build()

    def build(self):
        for i in range(random.randrange(10)):
            next_obstacle = random.choice((Fridge, ))(self.r)
            x, y = random.randrange(self.image.get_rect().width), random.randrange(self.image.get_rect().height)
            next_obstacle.rect.x, next_obstacle.rect.y = x, y
            while pygame.sprite.spritecollideany(next_obstacle, self.obstacles_group):
                x, y = random.randrange(self.image.get_rect().width), random.randrange(self.image.get_rect().height)
                next_obstacle.rect.x, next_obstacle.rect.y = x, y

    def add_entity(self, entity):
        self.entities.append(entity)

    def draw(self, entity=None):
        this_room = pygame.Surface((self.image.get_rect().width, self.image.get_rect().height))
        this_room.blit(self.image, (0, 0))
        for sprite in self.obstacles_group.sprites():
            this_room.blit(sprite, (sprite.rect.x, sprite.rect.y))
        if entity:
            x = min(self.image.get_rect().width - entity.rect.width, max(0, entity.rect.x))
            y = min(self.image.get_rect().height - entity.rect.height, max(0, entity.rect.y))
            entity.rect.x, entity.rect.y = x, y
            this_room.blit(entity.image, (x, y))
        return this_room
