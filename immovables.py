import random

import pygame

from interfaces import Drawable, Updatable
import config as c
from logger import log


class Immovable(Drawable):
    """ Now only prizes (boxes) are Immovable. """

    possible_prizes = ["food", "knife"]

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.prize = random.randint(0, 1)
        self.prize = self.possible_prizes[self.prize]
        self.image = pygame.image.load(c.immovable_image)

    def draw(self, context):
        image_main_map = pygame.transform.scale(self.image,
                                                (context.main_map_view.cell_w, context.main_map_view.cell_h))
        image_corner_map = pygame.transform.scale(self.image,
                                                  (context.corner_map_view.cell_w, context.corner_map_view.cell_h))
        context.surface.blit(image_main_map, context.main_map_view.cell_to_coords(self.i, self.j))
        pygame.draw.rect(context.surface, (200, 100, 0),
                         (*context.corner_map_view.cell_to_coords(self.i, self.j), context.corner_map_view.cell_w,
                          context.corner_map_view.cell_h))

    def kill_me(self, context):
        for i in range(len(context.immovables_container.buf)):
            if context.immovables_container.buf[i] is self:
                del context.immovables_container.buf[i]
                break

        context.map.data[self.i][self.j][1] = None


class ImmovablesContainer(Drawable, Updatable):
    """ Container for Immovables storing together for easy management and updating """

    def __init__(self):
        log.info("Creating ImmovablesContainer")
        self.buf = []

    def add_immovable(self, immovable: Immovable):
        self.buf.append(immovable)

    def update(self, event, context):
        pass

    def draw(self, context):
        for immovable in self.buf:
            immovable.draw(context)
