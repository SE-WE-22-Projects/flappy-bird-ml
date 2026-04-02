import pickle
import random
from collections import defaultdict
from pathlib import Path
from typing import Tuple

import numpy

from flappy_bird_ml.game import run_game, simmulate_game_state
from flappy_bird_ml.game.constants import BIRD_X, PIPE_GAP, PIPE_SPEED
from flappy_bird_ml.game.controller import Controller
from flappy_bird_ml.game.state import Bird, Pipe

# Discretization bins
Y_BIN_SIZE = 4
VEL_BIN_SIZE = 1
DX_BIN_SIZE = 2
DY_BIN_SIZE = 4

ACTIONS = [0, 1]  # 0 = no flap, 1 = flap


class QLearningController(Controller):
    def __init__(self):
        self.q_table = defaultdict(lambda: [0.0, 0.0])

        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.99
        self.epsilon = 1

        # For tracking previous step
        self.prev_state = None
        self.prev_action = None

    # State Discretization
    def discretize(self, bird, pipe) -> Tuple:
        # Bird Y
        y_bin = int(bird.y // Y_BIN_SIZE)

        # Velocity (-8 to 8, step 0.5, normalize index)
        vel_bin = int((bird.velocity + 8) / VEL_BIN_SIZE)

        # Horizontal distance to pipe
        dx = pipe.x - BIRD_X
        dx_bin = int(dx // DX_BIN_SIZE)

        # Gap center
        gap_center = pipe.gap_bottom_y + (PIPE_GAP // 2)

        # Vertical difference
        dy = bird.y - gap_center
        dy_bin = int((dy + 256) // DY_BIN_SIZE)  # shift to avoid negatives

        return (y_bin, vel_bin, dx_bin, dy_bin)

    # Policy (ε-greedy)
    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)
        return int(self.q_table[state][1] > self.q_table[state][0])

    # Q-learning update
    def update(self, state, action, reward, next_state):
        best_next = max(self.q_table[next_state])
        current = self.q_table[state][action]

        self.q_table[state][action] += self.alpha * (
            reward + self.gamma * best_next - current
        )

    # Main control method
    def will_flap(self, bird, next_pipe) -> bool:
        state = self.discretize(bird, next_pipe)
        action = self.select_action(state)

        # Store for update later
        self.prev_state = state
        self.prev_action = action

        return action == 1

    def step_update(self, bird, pipe, reward, done):
        if self.prev_state is None:
            return

        next_state = self.discretize(bird, pipe)

        self.update(self.prev_state, self.prev_action, reward, next_state)

        if done:
            self.prev_state = None
            self.prev_action = None


def train(controller, episodes=10000):
    for episode in range(episodes):
        best_score = -1e10

        for pipe_y in range(100, 400 + 1, DY_BIN_SIZE):
            for bird_y in range(0, 512 + 1, Y_BIN_SIZE):
                for vel in range(
                    -16,
                    16 + 1,
                ):
                    score = simmulate_game_state(
                        controller,
                        Pipe(200, pipe_y),
                        bird=Bird(y=bird_y, velocity=vel / 2),
                        cb=controller.step_update,
                    )
                    if score > best_score:
                        print(f"New best {score}")
                    best_score = max(best_score, score)

        print(
            f"Episode {episode}, Score: {best_score}, Epsilon: {controller.epsilon:.3f}"
        )

        controller.epsilon = max(0.01, controller.epsilon * 0.75)


def load():
    ctl = QLearningController()
    with open(Path("./models/qlearn.pickle"), "rb") as f:
        ctl.q_table = defaultdict(lambda: [0.0, 0.0], pickle.load(f))
    return ctl


def run_training():
    ctl = QLearningController()
    try:
        train(ctl)
    except KeyboardInterrupt:
        pass

    with open(Path("./models/qlearn.pickle"), "wb") as f:
        pickle.dump(dict(ctl.q_table), f)

    return ctl


if __name__ == "__main__":
    ctl = run_training()

    ctl.epsilon = 0
    run_game(ctl, "q_learn")
