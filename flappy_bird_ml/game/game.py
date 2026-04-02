import random
from itertools import chain

from flappy_bird_ml.game.constants import (
    FLAP_VEL,
    PIPE_GAP,
    PIPE_SPACING,
    PIPE_SPEED,
    PIPE_WIDTH,
)
from flappy_bird_ml.game.controller import Controller
from flappy_bird_ml.game.screen import GameScreen
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
        """
        Runs a single game until the bird hits a pipe or the max score is reached.

        Parameters:
            seed - the seed to use for generating pipe hieghts
            max_score - the max score before the game ends. Unlimited if -1.
        """
        r = random.Random(seed)

        bird = Bird(self.height / 2, 0)

        start = self.width // 2
        pipes = [
            Pipe(start, (self.height - PIPE_GAP) // 2),
        ]

        while pipes[-1].x < self.width + PIPE_SPACING:
            pipes.append(Pipe.new(start + PIPE_SPACING * len(pipes), r, self.height))

        passed_pipes = []

        score = 0
        has_collided = False

        while not has_collided and (max_score < 0 or score < max_score):
            pipe = pipes[0]

            will_flap = self.controller.will_flap(bird, pipe)
            if will_flap:
                bird.velocity = FLAP_VEL

            bird.physics_tick()
            has_collided = bird.check_collusion(self.height, pipe)

            # passed the pipe
            if not has_collided and pipe.has_passed_bird() and not pipe.scored:
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
        from flappy_bird_ml.game.screen_pygame import GameScreenPyGame

        if not isinstance(self.screen, GameScreenPyGame):
            raise RuntimeError("Called run_interactive with EmptyGameScreen")

        self.screen.display("Waiting", 0, Bird(self.height / 2, 0), [])
        self.screen.wait_input()
        while True:
            self.run_single()
            self.screen.wait_input()
