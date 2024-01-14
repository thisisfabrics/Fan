import random

import pygame.sprite

from executables.entities.Belle import Belle
from executables.rooms.obstacles.Bottom import Bottom
from executables.rooms.obstacles.Fridge import Fridge
from executables.entities.Catterfield import Catterfield
from executables.rooms.obstacles.Right import Right
from executables.rooms.obstacles.Top import Top
from executables.rooms.obstacles.Portal import Portal


class Room:
    def __init__(self, r, collection_coords):
        self.r = r
        self.collection_coords = collection_coords
        self.image = self.r.drawable("tiles")
        self.obstacles_group = pygame.sprite.Group()
        self.max_count_of_obstacles = 3
        self.max_count_of_enemies = 4
        self.entities_group = pygame.sprite.Group()
        self.portals_group = pygame.sprite.Group()
        self.build()
        self.populate()

    def populate(self):
        self.entities_group.empty()
        for i in range(random.randrange(1, self.max_count_of_enemies)):
            next_enemy = (choiced := random.choice((Catterfield, )))(self.r, f"{choiced.__name__.lower()}_movement",
                                                                     200)
            x, y = (random.randrange(self.image.get_rect().width - next_enemy.rect.width),
                    random.randrange(self.image.get_rect().height - next_enemy.rect.height))
            next_enemy.rect.x, next_enemy.rect.y = x, y
            while pygame.sprite.spritecollideany(next_enemy, self.obstacles_group) or \
                    pygame.sprite.spritecollideany(next_enemy, self.entities_group):
                x, y = (random.randrange(self.image.get_rect().width - next_enemy.rect.width),
                        random.randrange(self.image.get_rect().height - next_enemy.rect.height))
                next_enemy.rect.x, next_enemy.rect.y = x, y
            next_enemy.x = next_enemy.rect.x
            next_enemy.y = next_enemy.rect.y
            self.add_entity(next_enemy)

    def build(self):
        belle_width, belle_height = self.r.drawable("belle_idle_0").get_rect()[-2:]
        portal_width, portal_height = self.r.drawable("portal").get_rect()[-2:]
        belle_addition_size = int(50 * self.r.constant("coefficient"))
        approved_spawn_x_range_start = belle_width + portal_width + belle_addition_size
        approved_spawn_x_range_end = self.image.get_rect().width - belle_width - portal_width - belle_addition_size
        approved_spawn_y_range_start = belle_height + portal_width + belle_addition_size
        approved_spawn_y_range_end = self.image.get_rect().height - belle_height - portal_width - belle_addition_size
        self.obstacles_group.empty()
        self.portals_group.empty()
        for i in range(random.randrange(1, self.max_count_of_obstacles)):
            next_obstacle = random.choice((Fridge, ))(self.r)
            x, y = (random.randrange(approved_spawn_x_range_start,
                                     approved_spawn_x_range_end - next_obstacle.rect.width),
                    random.randrange(approved_spawn_y_range_start,
                                     approved_spawn_y_range_end - next_obstacle.rect.height))
            next_obstacle.rect.x, next_obstacle.rect.y = x, y
            iteration = 1000
            while (pygame.sprite.spritecollideany(next_obstacle, self.obstacles_group) or
                    pygame.sprite.spritecollideany(next_obstacle, self.entities_group)) and iteration:
                iteration -= 1
                x, y = (random.randrange(approved_spawn_x_range_start,
                                         approved_spawn_x_range_end - next_obstacle.rect.width),
                        random.randrange(approved_spawn_y_range_start,
                                         approved_spawn_y_range_end - next_obstacle.rect.height))
                next_obstacle.rect.x, next_obstacle.rect.y = x, y
            if not iteration:
                continue
            self.obstacles_group.add(next_obstacle)
        y, x = self.collection_coords
        if x != 2:
            self.portals_group.add(Right(self.r, self.image.get_rect()[-2:]))
        if y != 2:
            self.portals_group.add(Bottom(self.r, self.image.get_rect()[-2:]))
        if x:
            self.portals_group.add(Portal(self.r, self.image.get_rect()[-2:]))
        if y:
            self.portals_group.add(Top(self.r, self.image.get_rect()[-2:]))

    def add_entity(self, entity):
        self.entities_group.add(entity)

    def remove_entity(self, entity):
        self.entities_group.remove(entity)

    def draw_obstacles(self, surface):
        self.obstacles_group.draw(surface)

    def draw_portals(self, surface):
        self.portals_group.draw(surface)

    def draw_entities(self, surface, hand_mode=False):
        belle = self.find_belle()
        for entity in self.entities_group.sprites() if not hand_mode else (belle,):
            if isinstance(entity, Belle) and not hand_mode:
                continue
            if not hand_mode and pygame.sprite.collide_rect(entity, belle) and belle.became_ghost_at is None:
                belle.damage_collision(entity)
            x = min(self.image.get_rect().width - entity.rect.width, max(0, entity.rect.x))
            y = min(self.image.get_rect().height - entity.rect.height, max(0, entity.rect.y))
            if entity.rect.x != x:
                entity.undo_move_x()
            if entity.rect.y != y:
                entity.undo_move_y()
            surface.blit(entity.image, (entity.rect.x, entity.rect.y))

    def draw_belle(self, surface):
        entity = self.find_belle()
        if pygame.sprite.spritecollideany(entity, self.obstacles_group):
            entity.undo_move_x()
            if pygame.sprite.spritecollideany(entity, self.obstacles_group):
                entity.redo_move_x()
                entity.undo_move_y()
                if pygame.sprite.spritecollideany(entity, self.obstacles_group):
                    entity.undo_move_x()
        is_entered_portal = False
        if portal := pygame.sprite.spritecollideany(entity, self.portals_group):
            sequence_x = [portal.rect.x, entity.rect.x, entity.rect.x + entity.rect.width,
                          portal.rect.x + portal.rect.width]
            sequence_y = [portal.rect.y, entity.rect.y, entity.rect.y + entity.rect.height,
                          portal.rect.y + portal.rect.height]
            if sequence_x != sorted(sequence_x) and sequence_y != sorted(sequence_y):
                if entity.last_delta_x:
                    entity.undo_move_x()
                if entity.last_delta_y:
                    entity.undo_move_y()
            else:
                is_entered_portal = portal
        self.draw_entities(surface, True)
        return is_entered_portal

    def draw_bullets(self, surface):
        for bullet in self.find_belle().weapons[0].bullets_group.sprites():
            for entity in self.entities_group.sprites():
                if pygame.sprite.collide_rect(bullet, entity) and entity.__class__ in bullet.hitable_entities:
                    entity.add_damaging_bullet(bullet)
            bullet.draw(surface)

    def find_belle(self):
        try:
            return next(filter(lambda elem: isinstance(elem, Belle), self.entities_group.sprites()))
        except StopIteration:
            pass

    def draw_weapon(self, surface):
        surface.blit((we := self.find_belle().weapons[0]).image, we.rect[:2])

    def draw(self):
        this_room = pygame.Surface((self.image.get_rect().width, self.image.get_rect().height))
        this_room.blit(self.image, (0, 0))
        self.draw_obstacles(this_room)
        self.draw_portals(this_room)
        self.draw_entities(this_room)
        self.draw_bullets(this_room)
        is_entered_portal = self.draw_belle(this_room)
        self.draw_weapon(this_room)
        return this_room, is_entered_portal

    def update_sprites(self):
        self.find_belle().weapons[0].bullets_group.update()
        self.find_belle().weapons[0].update()
        self.entities_group.update(self.obstacles_group, self.entities_group, self.image.get_rect()[-2:])
