from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw(self, context):
        pass


class Updatable(ABC):
    @abstractmethod
    def update(self, event, context):
        pass
