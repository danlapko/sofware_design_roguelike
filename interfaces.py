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
