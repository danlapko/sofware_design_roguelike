import pygame

from interfaces import Updatable, Drawable
from logger import log


class TextsContainer(Drawable, Updatable):
    def __init__(self, base_x, base_y, text_callback):
        log.info("Creating TextsContainer text_callback:" + str(text_callback))

        self.text_callback = text_callback
        self.base_y = base_y
        self.base_x = base_x
        self.buf = []
        self.text_surface = None

    def update(self, event, context):
        pass

    def draw(self, context):
        self.clean_window(context)
        text = self.text_callback()
        lines = text.split("\n")
        myfont = pygame.font.SysFont('Comic Sans MS', 28)
        for i, line in enumerate(lines):
            self.text_surface = self.get_surface(line, myfont)
            context.surface.blit(self.text_surface, (self.base_x, self.base_y + i * self.text_surface.get_size()[1]))

    def clean_window(self, context):
        text = " \n                                              " \
               "\n                                                " \
               "\n                                             " \
               "\n                                             " \
               "\n                                             " \
               "\n                                             " \
               "\n                                             " \
               "\n                                             " \
               "\n                                             "
        lines = text.split("\n")
        myfont = pygame.font.SysFont('Comic Sans MS', 28)
        for i, line in enumerate(lines):
            self.text_surface = self.get_surface(line, myfont)
            context.surface.blit(self.text_surface, (self.base_x, self.base_y + i * self.text_surface.get_size()[1]))

    def draw_final_text(self, context, text):
        log.info("Drawing final text:" + text)

        text += "\nPress any key to exit."
        lines = text.split("\n")
        myfont = pygame.font.SysFont('Comic Sans MS', 28)
        for i, line in enumerate(lines):
            self.text_surface = self.get_surface(line, myfont)
            context.surface.blit(self.text_surface,
                                 (self.base_x, self.base_y + i * self.text_surface.get_size()[1] + 250))

    def get_surface(self, text, font):
        text_surface = font.render(text, False, (0, 120, 0), (0, 0, 0))
        return text_surface
