import numpy as np

from flappy_bird_ml.game import Controller
from flappy_bird_ml.game.constants import BIRD_X
from flappy_bird_ml.game.state import Bird, Pipe


class GeneticController(Controller):
    def __init__(self, theta) -> None:
        self.theta = theta

    def will_flap(self, bird: Bird, next_pipe: Pipe) -> bool:
        features = [
            1,  # bias
            bird.y,
            bird.velocity,
            next_pipe.x - BIRD_X,
            next_pipe.gap_y,
        ]
        return np.dot(self.theta, features) > 0
