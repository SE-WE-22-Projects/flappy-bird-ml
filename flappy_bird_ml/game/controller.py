import sys
from abc import ABC, abstractmethod

import pygame

from flappy_bird_ml.game.state import Bird, Pipe


class Controller(ABC):
    @abstractmethod
    def will_flap(self, bird: Bird, next_pipe: Pipe) -> bool:
        pass


class PlayerController(Controller):
    def will_flap(self, bird: Bird, next_pipe: Pipe) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        return False
