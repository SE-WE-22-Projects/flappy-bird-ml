import random
import typing

from flappy_bird_ml.game.constants import BIRD_X, FLAP_VEL, PIPE_GAP, PIPE_SPEED
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
    bird: Bird,
    cb: typing.Callable[[Bird, Pipe, bool], None],
):
    score = 0

    pipes = 1000

    pipe = Pipe(300, random.randint(140, 360))

    while True:
        will_flap = c.will_flap(bird, pipe)
        if will_flap:
            bird.velocity = FLAP_VEL

        bird.physics_tick()

        if bird.check_collusion(512, pipe):
            # bird, pipe, reward, done
            cb(bird, pipe, True)
            return score
        elif pipe.has_passed_bird():
            if pipes < 0:
                cb(bird, pipe, True)
                return score + 1

            cb(bird, pipe, False)
            pipe = Pipe(300, random.randint(140, 360))
            pipes -= 1
            score += 1
        else:
            cb(bird, pipe, False)

        pipe.x -= PIPE_SPEED


def run_game(c: Controller, alg_name: str | None = None):
    from flappy_bird_ml.game.screen_pygame import GameScreenPyGame

    screen = GameScreenPyGame(512, 720, alg_name=alg_name)

    game = Game(screen, c, 512, 720)
    game.run_interactive()


if __name__ == "__main__":
    from flappy_bird_ml.game.controller_player import PlayerController

    controller = PlayerController()
    run_game(controller)
