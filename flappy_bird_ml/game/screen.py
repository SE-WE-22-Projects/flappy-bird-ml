from abc import ABC
from typing import Iterable

from flappy_bird_ml.game import state


class GameScreen(ABC):
    def display(
        self,
        state: state.State,
        score: int,
        bird: state.Bird,
        pipes: Iterable[state.Pipe],
    ):
        pass

    def should_retry(self) -> bool:
        return False


class GameScreenEmpty(GameScreen):
    pass
