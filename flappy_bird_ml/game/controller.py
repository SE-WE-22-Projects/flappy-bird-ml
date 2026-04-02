from abc import ABC, abstractmethod

from flappy_bird_ml.game.state import Bird, Pipe


class Controller(ABC):
    @abstractmethod
    def will_flap(self, bird: Bird, next_pipe: Pipe) -> bool:
        pass
