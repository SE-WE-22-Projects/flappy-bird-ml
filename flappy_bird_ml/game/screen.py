from abc import ABC
from typing import Iterable

from flappy_bird_ml.game import state


class GameScreen(ABC):
    """
    Handles displaying the game state
    """

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
    """
    Game screen that renders nothing.
    Used during model training to skip unnecessary processing.
    """

    pass
