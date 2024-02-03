import random
import pygame

from executables.collectables.CyclotronDecoy import CyclotronDecoy
from executables.collectables.FanDecoy import FanDecoy
from executables.collectables.VacuumCleanerDecoy import VacuumCleanerDecoy
from executables.entities.Belle import Belle
from executables.rooms.Hall import Hall
from executables.rooms.Room import Room
from executables.rooms.obstacles.Bottom import Bottom
from executables.rooms.obstacles.Lift import Lift
from executables.rooms.obstacles.Right import Right
from executables.rooms.obstacles.Top import Top
from executables.ui.Screen import Screen
from executables.ui.widgets.Label import Label
from executables.ui.widgets.tablets.WeaponIcon import WeaponIcon
from modules.collectiontools import linerize


class Continue(Screen):
    def __init__(self, r, frame, mode=False):
        super().__init__(r, frame)
        if not mode:
            self.level = 10
            self.rooms = [[Room(self.r, (i, j)) if random.random() < .5 else Hall(self.r, (i, j)) for j in range(3)]
                          for i in range(3)]
            self.rooms[0][0].add_entity(Belle(self.r, "belle_idle", 200))
            self.rooms[0][0].build()
            self.add_weapons()
            self.battery_equivalent = 10
            self.interface_offset = 40 * self.r.constant("coefficient"), 40 * self.r.constant("coefficient")
            self.inventory_window_is_showing = False
            self.lift = Lift(self.r, self.rooms[0][0].image.get_rect()[-2:], self.level, self.rooms[0][0].portals_group)

    def add_weapons(self):
        for decoy in (VacuumCleanerDecoy,):
            randroom = self.rooms[random.randrange(len(self.rooms))][random.randrange(len(self.rooms[0]))]
            decoy(self.r, randroom.free_pos(), randroom.collectables_group)
        FanDecoy(self.r, self.rooms[0][0].free_pos(), self.rooms[0][0].collectables_group)
        CyclotronDecoy(self.r, self.rooms[0][0].free_pos(), self.rooms[0][0].collectables_group)

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

    def mouse_released(self, button):
        if button == 1:
            self.remove_time_event("release_bullets")
            self.find_belle()[0].mouse_updated = True

    def mouse_moved(self, pos):
        if self.inventory_window_is_showing:
            for elem in self.find_belle()[0].catalysts.items:
                elem.check_focus(pos)
            self.find_belle()[0].catalysts.check_focus(pos)

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
                self.signal_to_change = "stage_passed"
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
        for i in range(entity.energy_threshold // self.battery_equivalent):
            self.frame.blit(self.r.drawable("active_battery") if entity.energy - self.battery_equivalent * i > 0 else
                            self.r.drawable("passive_battery"),
                            (self.interface_offset[0] + 120 * i * self.r.constant("coefficient"),
                             self.interface_offset[1]))

    def place_inventory_window(self):
        if not self.inventory_window_is_showing:
            return
        self.frame.blit(self.r.drawable("inventory_window"), (0, 0))
        if self.find_belle()[0].weapons:
            for i, elem in enumerate(self.find_belle()[0].weapons):
                (WeaponIcon(self.r, (550, i * 300 + 1090), elem.__class__.__name__,
                            pygame.mouse.get_pos(), lambda: self.find_belle()[0].sort_weapon_by(elem.__class__))
                 .draw(self.frame))
        else:
            (Label(self.r, self.r.string("if_not_weapons"), (450, 1200), 90, 400 * self.r.constant("coefficient"),
                   pygame.Color(127, 108, 84))
             .draw(self.frame))
        focused = None
        if self.find_belle()[0].catalysts.items:
            self.find_belle()[0].catalysts.draw(self.frame)
            for elem in self.find_belle()[0].catalysts.items:
                if elem.focus:
                    focused = elem
        else:
            Label(self.r, self.r.string("catalysts_will_appear"), (1600, 1200), 90,
                  800 * self.r.constant("coefficient"), pygame.Color(127, 108, 84)).draw(self.frame)
        if focused:
            Label(self.r, focused.description, (2800, 1200), 90, 400 * self.r.constant("coefficient"),
                  pygame.Color(127, 108, 84)).draw(self.frame)
        else:
            Label(self.r, self.r.string("no_focus"), (2800, 1200), 90, 400 * self.r.constant("coefficient"),
                  pygame.Color(127, 108, 84)).draw(self.frame)

    def place_interface(self):
        belle = self.find_belle()[0]
        self.place_health_bar(belle)
        self.place_inventory_window()

    def push_to_database(self):
        pass

    def finish_game(self):
        self.signal_to_change = "finish"

    def update(self):
        self.find_belle()[1].update_sprites()
        try:
            if entered_portal := self.place_room():
                self.push_belle_in_direction(entered_portal)
            self.place_interface()
        except StopIteration:
            self.push_to_database()
            self.finish_game()
        self.lift.set_count_of_enemies(len(linerize([elem.entities_group.sprites() for elem in linerize(self.rooms)])) - 1)
        return self.signal_to_change
