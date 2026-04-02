import typing

from flappy_bird_ml.game.constants import FLAP_VEL
from flappy_bird_ml.game.controller import Controller
from flappy_bird_ml.game.game import Game
from flappy_bird_ml.game.screen import GameScreenEmpty
from flappy_bird_ml.game.state import Bird, Pipe


def simmulate_game(c: Controller, seed: int | None = None, max_score: int = 1000):
    screen = GameScreenEmpty()
    game = Game(screen, c, 512, 720)
    return game.run_single(seed, max_score)


def simmulate_game_state(
    c: Controller,
    pipe: Pipe,
    bird: Bird,
    cb: typing.Callable[[Bird, Pipe, float, bool], None],
):
    has_collided = False

    while not has_collided:
        will_flap = c.will_flap(bird, pipe)
        if will_flap:
            bird.velocity = FLAP_VEL

        bird.physics_tick()
        has_collided = bird.check_collusion(512, pipe)

        if bird.check_collusion(512, pipe):
            # bird, pipe, reward, done
            cb(bird, pipe, -1000, True)
            return -1000
        elif not has_collided and pipe.has_passed_bird():
            cb(bird, pipe, 10, False)
            return 10
        else:
            cb(bird, pipe, 0.1, False)


def run_game(c: Controller, alg_name: str | None = None):
    from flappy_bird_ml.game.screen_pygame import GameScreenPyGame

    screen = GameScreenPyGame(512, 720, alg_name=alg_name)

    game = Game(screen, c, 512, 720)
    game.run_interactive()


if __name__ == "__main__":
    from flappy_bird_ml.game.controller_player import PlayerController

    controller = PlayerController()
    run_game(controller)
