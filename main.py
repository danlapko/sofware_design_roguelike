import sys

import pygame

import config as c
from actor import MobsContainer
from immovables import ImmovablesContainer
from map import Map, MainMapView, CornerMapView
from textobject import TextsContainer
from logger import log


class Context:
    def __init__(self):
        # my fields
        self.map = None
        self.main_map_view = None
        self.corner_map_view = None
        self.main_actor = None
        self.mobs_container = None
        self.immovables_container = None
        self.texts_container = None
        self.keydown_handlers = None
        self.is_game_over = False

        # pygame fields
        self.surface = None
        self.clock = None

        self._init_pygame()
        self._init_fields()
        log.info("Context created")

    def _init_fields(self):
        self.map = Map()

        # self.main_actor = MainActor()
        self.mobs_container = MobsContainer()
        self.immovables_container = ImmovablesContainer()

        self.map.load_map(c.map_path, self)

        self.main_map_view = MainMapView(self.map, c.main_map_cell_w, c.main_map_cell_h, c.main_map_x, c.main_map_y)
        self.corner_map_view = CornerMapView(self.map, c.corner_map_cell_w, c.corner_map_cell_h, c.corner_map_x,
                                             c.corner_map_y)
        self.texts_container = TextsContainer(c.text_x, c.text_y, self.main_actor.get_printable_text)

        self.keydown_handlers = [self.main_actor.update, self.mobs_container.update, self.immovables_container.update,
                                 self.texts_container.update]

        self.is_game_over = False

    def _init_pygame(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((c.win_width, c.win_height))
        pygame.display.flip()

        pygame.display.set_caption(c.win_caption)
        self.clock = pygame.time.Clock()

    def _step(self, event):
        log.info("Event: " + str(event))

        if event.key == pygame.K_u:
            self.main_actor.undress_last_equipment()

        else:
            for handler in self.keydown_handlers:
                log.info("Handler " + str(handler) + " will processes an event: ")
                handler(event, self)

        self._redraw()

    def _redraw(self):
        self.main_map_view.draw(self)
        self.corner_map_view.draw(self)
        self.immovables_container.draw(self)
        self.main_actor.draw(self)
        self.mobs_container.draw(self)
        self.texts_container.draw(self)

    def run(self):
        log.info("Starting main loop")

        self.show_start_up_shout_down_text("Press arrow to start")
        while not self.is_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    log.info("Exiting by is_game_over==True")
                    self.is_game_over = True
                elif event.type == pygame.KEYDOWN and event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,
                                                                    pygame.K_DOWN]:
                    self._step(event)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    self._step(event)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.game_over(False)

            pygame.display.update()
            self.clock.tick(c.frame_rate)

    def show_start_up_shout_down_text(self, text):
        self.surface.fill((0, 0, 0))

        font = pygame.font.SysFont('Comic Sans MS', 28)

        lines = text.split("\n")
        for i, line in enumerate(lines):
            text_surface = font.render(line, False, (0, 120, 0), (0, 0, 0))
            self.surface.blit(text_surface,
                              (c.win_height * 2 // 5, c.win_width * 2 // 5 + i * text_surface.get_size()[1]))
        pygame.display.update()
        self.clock.tick(c.frame_rate)

    def game_over(self, win_flag):
        if win_flag:
            self.show_start_up_shout_down_text("YOU WIN!\nPress any key to exit")
        else:
            self.show_start_up_shout_down_text("FAIL, YOU DIED!\nPress any key to exit")
        pygame.display.update()
        self.clock.tick(c.frame_rate)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    sys.exit()

    def _exit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Context()
    game.run()
