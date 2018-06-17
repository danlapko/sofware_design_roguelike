from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw(self, context):
        pass


class Updatable(ABC):
    """ Each one who can change it state on next step is Updatable """

    @abstractmethod
    def update(self, event, context):
        pass


class OnMapPlaceable(ABC):
    """ A class that can be placed on a map """

    def __init__(self, i, j):
        self.j = j
        self.i = i
