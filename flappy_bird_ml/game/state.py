import random
import typing
from dataclasses import dataclass

from flappy_bird_ml.game.constants import MIN_PIPE_HEGHT, PIPE_GAP

State = typing.Literal["Waiting", "Playing", "Ended"]


@dataclass
class Pipe:
    x: int
    gap_y: int

    @classmethod
    def new(cls, x: int, screen_heght: int):
        return cls(
            x,
            random.randint(MIN_PIPE_HEGHT, screen_heght - PIPE_GAP - MIN_PIPE_HEGHT),
        )


@dataclass
class Bird:
    y: float
    velocity: float
