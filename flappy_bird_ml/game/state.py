import random
import typing
from dataclasses import dataclass

from flappy_bird_ml.game.constants import (
    BIRD_HEIGHT,
    BIRD_MAX_SPEED,
    BIRD_X,
    GRAVITY,
    MIN_PIPE_HEGHT,
    PIPE_GAP,
    PIPE_WIDTH,
)

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

    def has_passed_bird(self):
        return self.x + PIPE_WIDTH < BIRD_X


@dataclass
class Bird:
    y: float
    velocity: float

    def physics_tick(self):
        self.velocity += GRAVITY
        if self.velocity > BIRD_MAX_SPEED:
            self.velocity = BIRD_MAX_SPEED
        elif self.velocity < -BIRD_MAX_SPEED:
            self.velocity = -BIRD_MAX_SPEED
        self.y += self.velocity

    def check_collusion(self, height: int, pipe: Pipe):
        # Bird collides with top or bottom of the screen
        if self.y <= 0 or self.y > height - BIRD_HEIGHT:
            return True
        # Bird collides with pipe
        elif pipe.collides(bx=BIRD_X, by=self.y):
            return True
            # print(
            #     f"Collide:  {pipe.gap_bottom_y} {pipe.gap_bottom_y + PIPE_GAP} {bird.y} {done} {pipe.collides(bx=BIRD_X, by=bird.y)}"
            # )
            #
        return False


@dataclass
class Frame:
    bird: Bird
    pipe: Pipe
    score: int
    frame_score: float
    is_dead: bool
