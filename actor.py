import random

import pygame

from interfaces import Drawable, Updatable
from abc import abstractmethod
import config as c
from logger import log


class AbstactActor(Drawable, Updatable):
    def __init__(self, i, j, image_path):
        self.i = i
        self.j = j
        self.image = pygame.image.load(image_path)
        self.hp = 100
        self.power_koef = 1.0

    def draw(self, context):
        image_main_map = pygame.transform.scale(self.image,
                                                (context.main_map_view.cell_w, context.main_map_view.cell_h))
        image_corner_map = pygame.transform.scale(self.image,
                                                  (context.corner_map_view.cell_w, context.corner_map_view.cell_h))
        main_map_x, main_map_y = context.main_map_view.cell_to_coords(self.i, self.j)
        context.surface.blit(image_main_map, (main_map_x, main_map_y))

        context.surface.blit(image_corner_map, context.corner_map_view.cell_to_coords(self.i, self.j))

        # green line
        green_width = context.main_map_view.cell_w / 10
        green_length = context.main_map_view.cell_h * self.hp / 100
        pygame.draw.rect(context.surface, (0, 128, 0), (main_map_x, main_map_y, green_length, green_width))

    def try_move_to(self, i, j, context) -> bool:
        from map import Wall, Empty

        cell_back, cell_immovable, cell_actor = context.map.data[i][j]

        if isinstance(cell_back, Wall):
            self.face_with_wall(i, j, context)
            return False
        elif cell_actor is not None:
            self.face_with_actor(i, j, context)
            return False
        elif cell_immovable is not None:
            self.face_with_immovable(i, j, context)
            return True
        elif isinstance(cell_back, Empty):
            self.face_with_empty(i, j, context)
            return True

        raise ValueError("Invalid cell")

    def move_to(self, i, j, context):
        context.map.data[self.i][self.j][2] = None
        self.i = i
        self.j = j
        context.map.data[self.i][self.j][2] = self

    def face_with_empty(self, i, j, context):
        self.move_to(i, j, context)

    def face_with_wall(self, i, j, context):
        pass

    def face_with_immovable(self, i, j, context):

        self.move_to(i, j, context)

    @abstractmethod
    def face_with_actor(self, i, j, context):
        pass


class MainActor(AbstactActor):
    def __init__(self, i, j, image_path):
        super().__init__(i, j, image_path)
        self.dressed_equipment = []

    def update(self, event, context):
        if event.key == pygame.K_UP:
            self.try_move_to(self.i, self.j - 1, context)

        elif event.key == pygame.K_DOWN:
            self.try_move_to(self.i, self.j + 1, context)

        elif event.key == pygame.K_LEFT:
            self.try_move_to(self.i - 1, self.j, context)

        elif event.key == pygame.K_RIGHT:
            self.try_move_to(self.i + 1, self.j, context)

    def face_with_immovable(self, i, j, context):
        log.info("MainActor facing with immovable:" + str(i) + " " + str(j))

        immovable = context.map.data[i][j][1]
        if immovable.prize == "food":
            self.hp += 50
        else:
            self.dressed_equipment.append("knife")
            self.power_koef += 0.5
        immovable.kill_me(context)
        self.move_to(i, j, context)

    def face_with_actor(self, i, j, context):
        log.info("MainActor facing with mob:" + str(i) + " " + str(j))

        cur_power_koef = self.power_koef
        if j > self.j:
            cur_power_koef += c.head_power_coef
        else:
            cur_power_koef += c.attack_power_coef

        mob = context.map.data[i][j][2]
        mob_power_koef = mob.power_koef
        if j < self.j:
            mob_power_koef += c.head_power_coef

        self.hp -= mob_power_koef * c.hit_hp
        mob.hp -= cur_power_koef * c.hit_hp

        if mob.hp < 0:
            mob.kill_me(context)

        if self.hp <= 0:
            self.game_over(context, False)

        if len(context.mobs_container.buf) == 0:
            self.game_over(context, True)

    def get_printable_text(self):
        text = "HP: " + str(self.hp) + "\n\nequipment:"
        for equip in self.dressed_equipment:
            if equip == "knife":
                text += "\n   knife (1.5*power)"
        return text

    def undress_last_equipment(self):
        log.info("Main actor undressing last equipment")
        if self.dressed_equipment:
            del self.dressed_equipment[-1]
            self.power_koef -= 0.5

    def game_over(self, context, flag):
        log.info("MainActor game_over win_flag" + str(flag))

        context.game_over(flag)


class Mob(AbstactActor):
    def update(self, event, context):
        possible_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        key = random.randint(0, 3)
        key = possible_keys[key]

        if key == pygame.K_UP:
            self.try_move_to(self.i, self.j - 1, context)

        elif key == pygame.K_DOWN:
            self.try_move_to(self.i, self.j + 1, context)

        elif key == pygame.K_LEFT:
            self.try_move_to(self.i - 1, self.j, context)

        elif key == pygame.K_RIGHT:
            self.try_move_to(self.i + 1, self.j, context)

    def face_with_actor(self, i, j, context):
        mob = context.map.data[i][j][2]
        if not isinstance(mob, MainActor):
            return

        cur_power_koef = self.power_koef
        if j > self.j:
            cur_power_koef += c.head_power_coef
        else:
            cur_power_koef += c.attack_power_coef

        mob_power_koef = mob.power_koef
        if j < self.j:
            mob_power_koef += c.head_power_coef

        self.hp -= mob_power_koef * c.hit_hp
        mob.hp -= cur_power_koef * c.hit_hp

        if self.hp <= 0:
            self.kill_me(context)
        if mob.hp < 0:
            mob.game_over(context, False)
        if len(context.mobs_container.buf) == 0:
            mob.game_over(context, True)

    def kill_me(self, context):
        for i in range(len(context.mobs_container.buf)):
            if context.mobs_container.buf[i] is self:
                del context.mobs_container.buf[i]
                break

        context.map.data[self.i][self.j][2] = None


class MobsContainer(Drawable, Updatable):
    def __init__(self):
        log.info("Creating mobs container")

        self.buf = []

    def add_mob(self, mob: Mob):
        self.buf.append(mob)

    def update(self, event, context):
        for mob in self.buf:
            mob.update(event, context)

    def draw(self, context):
        for mob in self.buf:
            mob.draw(context)
