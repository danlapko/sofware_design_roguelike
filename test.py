import os
import unittest

import pygame

from actor import MainActor
from immovables import Immovable
from main import Context
from map import Map, Wall, Empty


class RoguelikeTest(unittest.TestCase):

    def test_load_map_simple(self):
        context = Context()
        map = Map()
        map.load_map("data/maps_fields/map1.txt", context)
        self.assertTrue(isinstance(map.data[-1][-1].background, Wall))
        self.assertTrue(isinstance(map.data[1][1].background, Empty))

    def test_load_map_immovable(self):
        context = Context()
        map = Map()
        map.load_map("data/maps_fields/map1.txt", context)
        self.assertTrue(isinstance(map.data[-2][-5].background, Empty))
        self.assertTrue(isinstance(map.data[-2][-5].immovable, Immovable))

    def test_load_map_main_actor(self):
        context = Context()
        map = Map()
        map.load_map("data/maps_fields/map1.txt", context)
        self.assertTrue(isinstance(map.data[-3][-9].background, Empty))
        self.assertEqual(map.data[-3][-9].immovable, None)
        self.assertTrue(isinstance(map.data[-3][-9].actor, MainActor))

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
        self.assertEquals(len(context.immovables_container.buf), 7)
        self.assertEquals(len(context.mobs_container.buf), 4)


if __name__ == '__main__':
    unittest.main()
