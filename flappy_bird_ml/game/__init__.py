import random
from itertools import chain

from flappy_bird_ml.game.constants import (
    BIRD_HEIGHT,
    BIRD_MAX_SPEED,
    BIRD_X,
    FLAP_VEL,
    GRAVITY,
    PIPE_GAP,
    PIPE_SPACING,
    PIPE_SPEED,
    PIPE_WIDTH,
)
from flappy_bird_ml.game.controller import Controller, PlayerController
from flappy_bird_ml.game.screen import GameScreen, GameScreenEmpty
from flappy_bird_ml.game.screen_pygame import GameScreenPyGame
from flappy_bird_ml.game.state import Bird, Pipe


class Game:
    def __init__(
        self, screen: GameScreen, controller: Controller, height: int, width: int
    ):
        self.height = height
        self.width = width
        self.screen = screen
        self.controller = controller

    def run_single(
        self,
        seed: int | None = None,
        max_score: int = -1,
    ):
        r = random.Random(seed)

        bird = Bird(self.height / 2, 0)

        start = self.width // 2
        pipes = [
            Pipe(start, (self.height - PIPE_GAP) // 2),
            Pipe.new(start + PIPE_SPACING, r, self.height),
            Pipe.new(start + PIPE_SPACING * 2, r, self.height),
            Pipe.new(start + PIPE_SPACING * 3, r, self.height),
        ]
        passed_pipes = []

        score = 0
        done = False

        while not done and (max_score < 0 or score < max_score):
            pipe = pipes[0]

            will_flap = self.controller.will_flap(bird, pipe)
            if will_flap:
                bird.velocity = FLAP_VEL

            bird.velocity += GRAVITY
            bird.y += bird.velocity

            if bird.velocity > BIRD_MAX_SPEED:
                bird.velocity = BIRD_MAX_SPEED
            elif bird.velocity < -BIRD_MAX_SPEED:
                bird.velocity = -BIRD_MAX_SPEED

            # Bird collides with top or bottom of the screen
            if bird.y <= 0 or bird.y > self.height - BIRD_HEIGHT:
                done = True
            # Bird collides with pipe
            elif pipe.collides(bx=BIRD_X, by=bird.y):
                done = True

            # print(
            #     f"Collide:  {pipe.gap_bottom_y} {pipe.gap_bottom_y + PIPE_GAP} {bird.y} {done} {pipe.collides(bx=BIRD_X, by=bird.y)}"
            # )

            # passed the pipe
            if pipe.x < BIRD_X and not pipe.scored:
                score += 1
                pipe.scored = True
                pipes.append(Pipe.new(pipes[-1].x + PIPE_SPACING, r, self.height))
                passed_pipes.append(pipes.pop(0))

            for pipe in chain(pipes, passed_pipes):
                pipe.x -= PIPE_SPEED

            for pipe in passed_pipes:
                if pipe.x < -PIPE_WIDTH:
                    passed_pipes.pop(0)

            self.screen.display("Playing", score, bird, chain(pipes, passed_pipes))

        self.screen.display("Ended", score, bird, pipes)

        return score

    def run_interactive(self):
        if not isinstance(self.screen, GameScreenPyGame):
            raise RuntimeError("Called run_interactive with EmptyGameScreen")

        self.screen.display("Waiting", 0, Bird(self.height / 2, 0), [])
        self.screen.wait_input()
        while True:
            self.run_single()
            self.screen.wait_input()


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
