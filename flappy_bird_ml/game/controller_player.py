import sys

import pygame

from flappy_bird_ml.game.controller import Controller
from flappy_bird_ml.game.state import Bird, Pipe


class PlayerController(Controller):
    def will_flap(self, bird: Bird, next_pipe: Pipe) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        return False
