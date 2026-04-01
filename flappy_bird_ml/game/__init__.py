from flappy_bird_ml.game.controller import Controller, PlayerController
from flappy_bird_ml.game.game import Game
from flappy_bird_ml.game.screen import GameScreenEmpty
from flappy_bird_ml.game.screen_pygame import GameScreenPyGame


def simmulate_game(c: Controller, seed: int | None = None, max_score: int = 1000):
    screen = GameScreenEmpty()
    game = Game(screen, c, 512, 720)
    return game.run_single(seed, max_score)


def run_game(c: Controller, alg_name: str | None = None):
    screen = GameScreenPyGame(512, 720, alg_name=alg_name)

    game = Game(screen, c, 512, 720)
    game.run_interactive()


if __name__ == "__main__":
    controller = PlayerController()
    run_game(controller)
