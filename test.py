import os
import unittest

import pygame

from actor import MainActor
from immovables import Immovable
from main import Context
from map import Map, Wall, Empty


class MyTestCase(unittest.TestCase):

    def test_load_map_simple(self):
        context = Context()
        map = Map()
        map.load_map("data/maps_fields/map1.txt", context)
        self.assertTrue(isinstance(map.data[-1][-1][0], Wall))
        self.assertTrue(isinstance(map.data[1][1][0], Empty))

    def test_load_map_immovable(self):
        context = Context()
        map = Map()
        map.load_map("data/maps_fields/map1.txt", context)
        self.assertTrue(isinstance(map.data[-2][-5][0], Empty))
        self.assertTrue(isinstance(map.data[-2][-5][1], Immovable))

    def test_load_map_main_actor(self):
        context = Context()
        map = Map()
        map.load_map("data/maps_fields/map1.txt", context)
        self.assertTrue(isinstance(map.data[-3][-9][0], Empty))
        self.assertEqual(map.data[-3][-9][1], None)
        self.assertTrue(isinstance(map.data[-3][-9][2], MainActor))

    def test_bad_map(self):
        context = Context()
        self.assertRaises(ValueError, Map().load_map, "data/maps_fields/map_bad.txt", context)

    def test_load_image(self):
        pygame.init()
        screen = pygame.display.set_mode((50, 50))
        cat = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/images", "wall.jpg"))
        screen.blit(cat, (0, 0))
        pygame.quit()

    def test_context(self):
        context = Context()
        self.assertEquals(len(context.immovables_container.buf), 5)
        self.assertEquals(len(context.mobs_container.buf), 4)


if __name__ == '__main__':
    unittest.main()
