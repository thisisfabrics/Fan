import datetime
import random
import pygame

from executables.collectables.CyclotronDecoy import CyclotronDecoy
from executables.collectables.FanDecoy import FanDecoy
from executables.collectables.VacuumCleanerDecoy import VacuumCleanerDecoy
from executables.entities.Belle import Belle
from executables.rooms.Hall import Hall
from executables.rooms.Room import Room
from executables.rooms.obstacles.Obstacle import Obstacle
from executables.rooms.obstacles.portals.Bottom import Bottom
from executables.rooms.obstacles.portals.Lift import Lift
from executables.rooms.obstacles.portals.Right import Right
from executables.rooms.obstacles.portals.Shop import Shop
from executables.rooms.obstacles.portals.Top import Top
from executables.ui.Screen import Screen
from executables.ui.widgets.Button import Button
from executables.ui.widgets.Label import Label
from executables.ui.widgets.tablets.WeaponIcon import WeaponIcon
from executables.weapons.Cyclotron import Cyclotron
from executables.weapons.Fan import Fan
from executables.weapons.VacuumCleaner import VacuumCleaner
from modules.collectiontools import linerize


class Continue(Screen):
    def __init__(self, r, frame, use_the_database=False):
        super().__init__(r, frame)
        self.inventory_window_is_showing = False
        self.buttons = (Button(self.r, self.r.string("pause"),
                               (3400, 20), self.pause_game, True),)
        if use_the_database:
            self.fetch_from_database()
        else:
            self.r.query("UPDATE statistics SET is_finished = 1")
            self.r.query("INSERT INTO statistics(weapons, liquidated_enemies, activated_catalysts, floor, year, month, "
                         f"day, is_finished) VALUES(0, 0, 0, 10, {datetime.datetime.now().strftime("%Y, %m, %d")}, 0)")
            self.r.database.commit()
            self.floor = 10
            self.rooms = list()
            self.build_rooms()
            self.rooms[0][0].add_entity(Belle(self.r, "belle_idle", 200))
            self.rooms[0][0].build()
            self.add_weapons()
        self.lift = Lift(self.r, self.rooms[0][0].image.get_rect()[-2:], self.floor, self.rooms[0][0].portals_group)
        self.shop = Shop(self.r, self.rooms[0][0].image.get_rect()[-2:], self.rooms[0][0].portals_group)
        self.empty_database(use_the_database)

    def build_rooms(self):
        self.rooms = [[Room(self.r, (i, j)) if random.random() < .5 else Hall(self.r, (i, j)) for j in range(3)]
                      for i in range(3)]

    def add_weapons(self, assortment=(VacuumCleanerDecoy,)):
        for decoy in assortment:
            randroom = self.rooms[random.randrange(len(self.rooms))][random.randrange(len(self.rooms[0]))]
            decoy(self.r, randroom.free_pos(), 1, randroom.collectables_group)
        FanDecoy(self.r, self.rooms[0][0].free_pos(), 1, self.rooms[0][0].collectables_group)
        CyclotronDecoy(self.r, self.rooms[0][0].free_pos(), 1, self.rooms[0][0].collectables_group)

    def find_belle(self):
        room = next(filter(lambda elem: Belle in map(lambda el: el.__class__, elem.entities_group.sprites()),
                           linerize(self.rooms)))
        belle = room.find_belle()
        return belle, room

    def button_pressed(self, key):
        if key == pygame.K_w:
            self.find_belle()[0].start_moving("up")
        elif key == pygame.K_s:
            self.find_belle()[0].start_moving("down")
        elif key == pygame.K_a:
            self.find_belle()[0].start_moving("left")
        elif key == pygame.K_d:
            self.find_belle()[0].start_moving("right")
        elif key == pygame.K_TAB:
            self.inventory_window_is_showing = not self.inventory_window_is_showing

    def button_released(self, key):
        if key == pygame.K_w:
            self.find_belle()[0].stop_moving("up")
        elif key == pygame.K_s:
            self.find_belle()[0].stop_moving("down")
        elif key == pygame.K_a:
            self.find_belle()[0].stop_moving("left")
        elif key == pygame.K_d:
            self.find_belle()[0].stop_moving("right")

    def mouse_pressed(self, button, pos):
        if button == 1:
            if self.find_belle()[0].weapons:
                self.add_time_event("release_bullets",
                                    self.find_belle()[0].use_weapon, self.find_belle()[0].weapons[0].timeout)
            for elem in self.buttons:
                elem.click()

    def mouse_released(self, button):
        if button == 1:
            self.remove_time_event("release_bullets")
            self.find_belle()[0].mouse_updated = True

    def mouse_moved(self, pos):
        if self.inventory_window_is_showing:
            for elem in self.find_belle()[0].catalysts.items:
                elem.check_focus(pos)
            self.find_belle()[0].catalysts.check_focus(pos)
        for elem in self.buttons:
            elem.check_focus(pos)

    def mouse_wheel(self, direction):
        if self.inventory_window_is_showing:
            self.find_belle()[0].catalysts.scroll(direction)

    def push_belle_in_direction(self, portal):
        belle, room = self.find_belle()
        belle_row, belle_column = room.collection_coords
        room.remove_entity(belle)
        if isinstance(portal, Right):
            belle_column = belle_column + 1
            belle.x -= room.image.get_rect().width - self.r.drawable("portal").get_rect().width * 2 - belle.rect.width
        elif isinstance(portal, Top):
            belle_row = belle_row - 1
            belle.y += room.image.get_rect().height - self.r.drawable("portal").get_rect().width * 2 - belle.rect.height
        elif isinstance(portal, Bottom):
            belle_row = belle_row + 1
            belle.y -= room.image.get_rect().height - self.r.drawable("portal").get_rect().width * 2 - belle.rect.height
        elif isinstance(portal, Lift):
            if not self.lift.count_of_enemies:
                self.rooms[belle_row][belle_column].add_entity(belle)
                belle.undo_move_y()
                self.push_to_database()
                self.signal_to_change = "completed"
                return
        elif isinstance(portal, Shop):
            self.rooms[belle_row][belle_column].add_entity(belle)
            belle.undo_move_x()
            self.push_to_database()
            self.signal_to_change = "store"
            return
        else:
            belle_column = belle_column - 1
            belle.x += room.image.get_rect().width - self.r.drawable("portal").get_rect().width * 2 - belle.rect.width
        belle.rect.x, belle.rect.y = belle.x, belle.y
        self.rooms[belle_row][belle_column].add_entity(belle)
        if room.__class__ != self.rooms[belle_row][belle_column].__class__:
            if isinstance(portal, Top) or isinstance(portal, Bottom):
                belle.x = self.rooms[belle_row][belle_column].image.get_rect().width / 2 - belle.rect.width / 2
                belle.y = portal.rect.height if not isinstance(portal, Top) else \
                    self.rooms[belle_row][belle_column].image.get_rect().height - \
                    portal.rect.height - belle.rect.height
            else:
                belle.y = self.rooms[belle_row][belle_column].image.get_rect().height / 2 - belle.rect.height / 2
                belle.x = portal.rect.width if isinstance(portal, Right) else \
                    self.rooms[belle_row][belle_column].image.get_rect().width - \
                    portal.rect.width - belle.rect.width
            belle.rect.x = belle.x
            belle.rect.y = belle.y
        self.clear_clocks_and_bullets()

    def clear_clocks_and_bullets(self):
        belle, room = self.find_belle()
        for elem in room.entities_group.sprites():
            elem.damaging_bullets = dict()
            try:
                elem.clock.tick()
                elem.released_bullets_group.empty()
            except AttributeError:
                pass
        if belle.weapons:
            belle.weapons[0].bullets_group.empty()

    def place_room(self):
        surface_from_room, is_entered_portal = self.find_belle()[1].draw()
        belle_x, belle_y = self.find_belle()[0].rect.x + self.find_belle()[0].rect.width / 2, \
            self.find_belle()[0].rect.y + self.find_belle()[0].rect.height / 2
        x, y = belle_x - self.r.constant("useful_width") / 2, belle_y - self.r.constant("useful_height") / 2
        x = min(surface_from_room.get_rect().width - self.r.constant("useful_width"), max(0, x))
        y = min(surface_from_room.get_rect().height - self.r.constant("useful_height"), max(0, y))
        self.find_belle()[0].set_mouse_position_compensation(x, y)
        self.frame.blit(surface_from_room, (-x, -y))
        return is_entered_portal

    def place_health_bar(self, entity):
        for i in range(entity.energy_threshold // self.r.constant("battery_equivalent")):
            self.frame.blit(self.r.drawable("active_battery")
                            if entity.energy - self.r.constant("battery_equivalent") * i > 0 else
                            self.r.drawable("passive_battery"),
                            (self.r.constant("health_bar_offset") + i * self.r.constant("health_bar_padding"),
                             self.r.constant("health_bar_offset")))

    def place_inventory_window(self):
        if not self.inventory_window_is_showing:
            return
        focused = None
        self.frame.blit(self.r.drawable("inventory_window"), (0, 0))
        if self.find_belle()[0].weapons:
            for i, elem in enumerate(self.find_belle()[0].weapons):
                icon = WeaponIcon(self.r, (420, i * 300 + 1090), elem.__class__.__name__,
                                  (elem.power, elem.power_threshold),
                                  elem.description, pygame.mouse.get_pos(),
                                  lambda: self.find_belle()[0].sort_weapon_by(elem.__class__))
                if icon.focus:
                    focused = icon
                icon.draw(self.frame)
        else:
            (Label(self.r, self.r.string("if_not_weapons"), (450, 1500), 90, 400,
                   pygame.Color(127, 108, 84))
             .draw(self.frame))
        if self.find_belle()[0].catalysts.items:
            self.find_belle()[0].catalysts.draw(self.frame)
            for elem in self.find_belle()[0].catalysts.items:
                if elem.focus:
                    focused = elem
        else:
            Label(self.r, self.r.string("catalysts_will_appear"), (1600, 1200), 90,
                  800, pygame.Color(127, 108, 84)).draw(self.frame)
        if focused:
            Label(self.r, focused.description, (2800, 1200), 90, 370,
                  pygame.Color(127, 108, 84)).draw(self.frame)
        else:
            Label(self.r, self.r.string("no_focus"), (2800, 1200), 90, 400,
                  pygame.Color(127, 108, 84)).draw(self.frame)

    def place_buttons(self):
        for elem in self.buttons:
            elem.draw(self.frame)

    def place_interface(self):
        belle = self.find_belle()[0]
        self.place_health_bar(belle)
        self.place_inventory_window()
        self.place_buttons()

    def push_to_database(self):
        self.empty_database(True)
        self.r.query(f"INSERT INTO floor(number) VALUES({self.floor})")
        for i, elem in enumerate(linerize(self.rooms)):
            self.r.query("INSERT INTO room(id, type, row, column) VALUES("
                         f"{i + 1}, {self.r.constant("room_object_to_id")[elem.__class__]}, "
                         f"{elem.collection_coords[0]}, {elem.collection_coords[1]})")
            for el in elem.obstacles_group.sprites() + elem.collectables_group.sprites():
                self.r.query("INSERT INTO obstacle_collectable(type, x, y, room_id) VALUES("
                             f"{self.r.constant("obstacle_collectable_object_to_id")[el.__class__]}, "
                             f"{el.rect.x}, {el.rect.y}, {i + 1})")
            for el in elem.entities_group.sprites():
                self.r.query("INSERT INTO entity(type, animation_name, animation_period, x, y, "
                             "energy, last_delta_x, last_delta_y, room_id) VALUES("
                             f"{self.r.constant("entity_object_to_id")[el.__class__]}, "
                             f"'{el.animation_name}', {el.animation_period}, {el.x}, {el.y}, {el.energy}, "
                             f"{el.last_delta_x}, {el.last_delta_y}, {i + 1})")
        try:
            vacuumcleaner_power = (next(filter(lambda e: isinstance(e, VacuumCleaner), self.find_belle()[0].weapons))
                                   .power)
        except StopIteration:
            vacuumcleaner_power = int()
        try:
            fan_power = (next(filter(lambda e: isinstance(e, Fan), self.find_belle()[0].weapons))
                         .power)
        except StopIteration:
            fan_power = int()
        try:
            cyclotron_power = (next(filter(lambda e: isinstance(e, Cyclotron), self.find_belle()[0].weapons))
                               .power)
        except StopIteration:
            cyclotron_power = int()
        self.r.query(f"INSERT INTO belle(money, vacuumcleaner_power, cyclotron_power, fan_power) VALUES("
                     f"{self.find_belle()[0].money}, {vacuumcleaner_power}, {cyclotron_power}, {fan_power})")
        self.r.database.commit()

    def empty_database(self, use_the_database):
        for elem in ("floor", "belle", "entity", "obstacle_collectable", "room"):
            self.r.query(f"DELETE FROM {elem}")
        if not use_the_database:
            self.r.query("UPDATE catalyst SET purchased = 0")
            self.r.query("UPDATE catalyst SET displayed = 0")
        self.r.database.commit()

    def fetch_from_database(self):
        self.floor = self.r.query("SELECT number FROM floor").fetchall()[0][0]
        if condition := self.floor != self.r.query("SELECT floor FROM statistics WHERE is_finished = 0").fetchall()[0][0]:
            self.build_rooms()
        else:
            self.rooms = list()
            current_row = list()
            for type, row, column in self.r.query("SELECT type, row, column FROM room ORDER BY row, column"):
                if len(current_row) == 3:
                    self.rooms.append(current_row)
                    current_row = list()
                current_row.append(self.r.constant("id_to_room_object")[type](self.r, (row, column), True))
            self.rooms.append(current_row)
            for type, x, y, room_row, room_column in self.r.query("SELECT obstacle_collectable.type, "
                                                                  "obstacle_collectable.x, obstacle_collectable.y, "
                                                                  "room.row, room.column FROM obstacle_collectable "
                                                                  "INNER JOIN room "
                                                                  "ON obstacle_collectable.room_id = room.id"):
                obstacle_collectable = self.r.constant("id_to_obstacle_collectable_object")[type](self.r, (x, y))
                if isinstance(obstacle_collectable, Obstacle):
                    self.rooms[room_row][room_column].obstacles_group.add(obstacle_collectable)
                else:
                    self.rooms[room_row][room_column].collectables_group.add(obstacle_collectable)
        for type, animation_name, animation_period, x, y, energy, last_delta_x, last_delta_y, room_row, room_column in \
                self.r.query("SELECT entity.type, entity.animation_name, entity.animation_period, entity.x, entity.y, "
                             "entity.energy, entity.last_delta_x, entity.last_delta_y, room.row, room.column "
                             "FROM entity INNER JOIN room ON entity.room_id = room.id"):
            if condition and self.r.constant("id_to_entity_object")[type] != Belle:
                continue
            entity = self.r.constant("id_to_entity_object")[type](self.r, animation_name, animation_period)
            entity.x, entity.y = x, y
            if condition:
                width, height = self.rooms[0][0].image.get_size()
                entity.x = width / 2 - entity.image.get_width() / 2
                entity.y = self.r.drawable("portal").get_width() + 1
            entity.rect.x, entity.rect.y = entity.x, entity.y
            entity.energy = energy
            entity.last_delta_x, entity.last_delta_y = last_delta_x, last_delta_y
            self.rooms[room_row][room_column].entities_group.add(entity)
        for type, purchased, _ in self.r.query("SELECT * FROM catalyst"):
            if purchased:
                self.find_belle()[0].catalysts.append(self.r.constant("id_to_catalyst_object")[type](self.r))
            self.find_belle()[0].apply_catalysts()
        _, money, vacuumcleaner_power, cyclotron_power, fan_power = next(self.r.query("SELECT * FROM belle"))
        self.find_belle()[0].money = money
        if vacuumcleaner_power:
            VacuumCleanerDecoy(self.r, self.find_belle()[0].rect[:2], vacuumcleaner_power,
                               self.find_belle()[1].collectables_group)
        if cyclotron_power:
            CyclotronDecoy(self.r, self.find_belle()[0].rect[:2], cyclotron_power,
                           self.find_belle()[1].collectables_group)
        if fan_power:
            FanDecoy(self.r, self.find_belle()[0].rect[:2], fan_power,
                     self.find_belle()[1].collectables_group)
        if condition:
            self.r.query(f"UPDATE statistics SET floor = {self.floor} WHERE is_finished = 0")
        self.r.query(f"UPDATE statistics SET weapons = {len(self.find_belle()[0].weapons)} "
                     f"WHERE is_finished = 0")
        self.r.database.commit()

    def finish_game(self):
        self.r.database.commit()
        self.empty_database(False)
        self.signal_to_change = "finish"

    def pause_game(self):
        self.push_to_database()
        self.signal_to_change = "start"

    def update(self):
        self.find_belle()[1].update_sprites()
        try:
            if entered_portal := self.place_room():
                self.push_belle_in_direction(entered_portal)
            self.place_interface()
        except StopIteration:
            self.finish_game()
        self.lift.set_count_of_enemies(len(
            linerize([elem.entities_group.sprites() for elem in linerize(self.rooms)])) - 1)
        return self.signal_to_change
