import pygame

import config as c
from interfaces import Drawable, Updatable, OnMapPlaceable
from logger import log


class Empty(OnMapPlaceable, Drawable):
    """ Background cell """

    def __init__(self, i, j):
        super().__init__(i, j)
        self.image = pygame.image.load(c.empty_image)

    def draw(self, context):
        image_main_map = pygame.transform.scale(self.image,
                                                (context.main_map_view.cell_w, context.main_map_view.cell_h))
        image_corner_map = pygame.transform.scale(self.image,
                                                  (context.corner_map_view.cell_w, context.corner_map_view.cell_h))
        context.surface.blit(image_main_map, context.main_map_view.cell_to_coords(self.i, self.j))
        pygame.draw.rect(context.surface, (76, 153, 0),
                         (*context.corner_map_view.cell_to_coords(self.i, self.j), context.corner_map_view.cell_w,
                          context.corner_map_view.cell_h))


class Wall(OnMapPlaceable, Drawable):
    """ Background cell """

    def __init__(self, i, j):
        super().__init__(i, j)
        self.image = pygame.image.load(c.wall_image)

    def draw(self, context):
        image_main_map = pygame.transform.scale(self.image,
                                                (context.main_map_view.cell_w, context.main_map_view.cell_h))
        image_corner_map = pygame.transform.scale(self.image,
                                                  (context.corner_map_view.cell_w, context.corner_map_view.cell_h))
        context.surface.blit(image_main_map, context.main_map_view.cell_to_coords(self.i, self.j))
        pygame.draw.rect(context.surface, (100, 100, 100),
                         (*context.corner_map_view.cell_to_coords(self.i, self.j), context.corner_map_view.cell_w,
                          context.corner_map_view.cell_h))


class Cell(OnMapPlaceable, Drawable, Updatable):
    """ Cell container for three types of objects that can be placed on map at the same time """

    def __init__(self, i, j, background=None, immovable=None, actor=None):
        super().__init__(i, j)
        self.actor = actor
        self.immovable = immovable
        self.background = background

    def update(self, event, context):
        pass

    def draw(self, context):
        pass


class Map(Updatable):
    """ The whole map.
    Each cell of the grid (data) contains list of three elements:
    [Background_obj (Empty or Wall), Immovable_obj (None possible), Actor_obj (None possible)] """

    def __init__(self):
        log.info("Creating Map")

        self.n_rows = 0
        self.n_cols = 0
        self.data = None

    def load_map(self, filename, context):
        from actor import MainActor, Mob
        from immovables import Immovable

        log.info("Loading map from file: " + filename)

        with open(filename, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            self.n_rows = len(lines)
            self.n_cols = len(lines[0])

            self.data = [None] * len(lines)
            self.data = [[None] * len(lines[0]) for _ in self.data]

            main_actor_found = False
            for i, line in enumerate(lines):
                assert self.n_cols == len(line), "map field is not rectangular"
                for j, elem in enumerate(line):
                    if elem == ".":
                        log.info("Creating Empty cell, coords: " + str(i) + " " + str(j))
                        self.data[i][j] = Cell(i, j, Empty(i, j), None, None)
                    elif elem == "#":
                        log.info("Creating Wall cell, coords: " + str(i) + " " + str(j))
                        self.data[i][j] = Cell(i, j, Wall(i, j), None, None)
                    elif elem == "A":
                        log.info("Creating MainActor cell, coords: " + str(i) + " " + str(j))
                        assert False == main_actor_found, "more then one main Actors found"
                        main_actor_found = True
                        context.main_actor = MainActor(i, j, c.main_actor_image)
                        self.data[i][j] = Cell(i, j, Empty(i, j), None, context.main_actor)
                    elif elem == "M":
                        log.info("Creating Mob cell, coords: " + str(i) + " " + str(j))
                        mob = Mob(i, j, c.mob_image)
                        context.mobs_container.add_mob(mob)
                        self.data[i][j] = Cell(i, j, Empty(i, j), None, mob)
                    elif elem == "I":
                        log.info("Creating Immutable cell, coords: " + str(i) + " " + str(j))
                        immovable = Immovable(i, j)
                        context.immovables_container.add_immovable(immovable)
                        self.data[i][j] = Cell(i, j, Empty(i, j), immovable, None)

                    else:
                        raise ValueError("Invalid map symbol: " + elem)

    def update(self, event, context):
        pass


class AbstractMapView(Drawable):
    """ Abstact Map View for different map representation. Contains reference to map as field. """

    def __init__(self, map: Map, cell_w, cell_h, base_x, base_y):
        log.info("Creating MapView:" + str(self.__class__))

        self.map = map
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.base_x = base_x
        self.base_y = base_y
        self.w = self.cell_w * self.map.n_rows
        self.h = self.cell_h * self.map.n_cols

    def cell_to_coords(self, i, j) -> (int, int):
        x = self.base_x + i * self.cell_w
        y = self.base_y + j * self.cell_h
        return x, y

    def draw(self, context):
        for i in range(self.map.n_rows):
            for j in range(self.map.n_cols):
                cell = self.map.data[i][j]
                cell.background.draw(context)


class MainMapView(AbstractMapView):
    """ Map View for Main map. """
    pass


class CornerMapView(AbstractMapView):
    """ Map View for Corner map. """
    pass
