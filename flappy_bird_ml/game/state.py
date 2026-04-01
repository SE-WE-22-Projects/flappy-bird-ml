import random
import typing
from dataclasses import dataclass

from flappy_bird_ml.game.constants import MIN_PIPE_HEGHT, PIPE_GAP

State = typing.Literal["Waiting", "Playing", "Ended"]


@dataclass
class Pipe:
    x: int
    gap_y: int
    scored: bool = False

    @classmethod
    def new(cls, x: int, r: random.Random, screen_heght: int):
        y_pos = r.randint(MIN_PIPE_HEGHT, screen_heght - PIPE_GAP - MIN_PIPE_HEGHT)
        return cls(x, y_pos)


@dataclass
class Bird:
    y: float
    velocity: float
