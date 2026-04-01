import random
import typing
from dataclasses import dataclass

from flappy_bird_ml.game.constants import MIN_PIPE_HEGHT, PIPE_GAP, PIPE_WIDTH

State = typing.Literal["Waiting", "Playing", "Ended"]


@dataclass
class Pipe:
    x: int
    gap_bottom_y: int
    scored: bool = False

    @classmethod
    def new(cls, x: int, r: random.Random, screen_heght: int):
        y_pos = r.randint(MIN_PIPE_HEGHT, screen_heght - PIPE_GAP - MIN_PIPE_HEGHT)
        return cls(x, y_pos)

    def collides(self, bx, by, radius=13):
        cap_ext = 3
        # top pipe rect
        if (
            bx + radius > self.x - cap_ext
            and bx - radius < self.x + PIPE_WIDTH + cap_ext
            and by - radius < self.gap_bottom_y
        ):
            return True

        # bottom pipe rect
        bot_y = self.gap_bottom_y + PIPE_GAP
        if (
            bx + radius > self.x - cap_ext
            and bx - radius < self.x + PIPE_WIDTH + cap_ext
            and by + radius > bot_y
        ):
            return True
        return False


@dataclass
class Bird:
    y: float
    velocity: float
