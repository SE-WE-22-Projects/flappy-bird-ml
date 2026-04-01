import random
import sys
from abc import ABC, abstractmethod

import pygame

from flappy_bird_ml.game.constants import (
    BIRD_HEIGHT,
    BIRD_MAX_SPEED,
    BIRD_X,
    FLAP_VEL,
    GRAVITY,
    PIPE_GAP,
    PIPE_SPEED,
    PIPE_WIDTH,
)
from flappy_bird_ml.game.screen import GameScreen, GameScreenPyGame
from flappy_bird_ml.game.state import Bird, Pipe


class Controller(ABC):
    @abstractmethod
    def will_flap(self, bird: Bird, next_pipe: Pipe) -> bool:
        pass


class Game:
    def __init__(
        self, screen: GameScreen, controller: Controller, height: int, width: int
    ):
        self.height = height
        self.width = width
        self.screen = screen

    def run_single(
        self,
        max_frames: int = -1,
    ):
        bird = Bird(self.height / 2, 0)
        pipes = [Pipe.new(self.width // 2, self.height)]

        score = 0
        frame = 0
        done = False

        while not done and (max_frames < 0 or frame < max_frames):
            pipe = pipes[0]
            will_flap = controller.will_flap(bird, pipe)
            if will_flap:
                bird.velocity = FLAP_VEL

            bird.velocity += GRAVITY
            bird.y += bird.velocity

            if bird.velocity > BIRD_MAX_SPEED:
                bird.velocity = BIRD_MAX_SPEED

            # Bird collides with top or bottom of the screen
            if bird.y <= 0 or bird.y > self.height - BIRD_HEIGHT:
                done = True
            # Bird collides with pipe
            elif (pipe.x <= BIRD_X <= pipe.x + PIPE_WIDTH) and not (
                pipe.gap_y <= bird.y <= pipe.gap_y + PIPE_GAP
            ):
                done = True

            # print(
            #     f"Collide: {gap_top} {gap_bottom} {pipe.gap_y} {pipe.gap_y + PIPE_GAP} {bird.y} {done}"
            # )

            # passed the pipe
            if pipe.x < BIRD_X:
                score += 1
                pipe.x = self.width
                pipe.gap_y = random.randint(80, self.height - 60 - PIPE_GAP - 60)

            for pipe in pipes:
                pipe.x -= PIPE_SPEED

            screen.display("Playing", score, bird, pipes)
            frame += 1

        screen.display("Ended", score, bird, pipes)

        return score

    def run_interactive(self):
        if not isinstance(screen, GameScreenPyGame):
            raise RuntimeError("Called run_interactive with EmptyGameScreen")

        screen.display("Waiting", 0, Bird(self.height / 2, 0), [])
        screen.wait_input()
        while True:
            self.run_single()
            screen.wait_input()


class PlayerController(Controller):
    def will_flap(self, bird: Bird, next_pipe: Pipe) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        return False


if __name__ == "__main__":
    screen = GameScreenPyGame(720, 512)
    controller = PlayerController()

    game = Game(screen, controller, 512, 720)
    game.run_interactive()
