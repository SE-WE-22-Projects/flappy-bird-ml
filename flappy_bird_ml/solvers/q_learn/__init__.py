import pickle
import random
from collections import defaultdict
from pathlib import Path
from typing import Tuple

from flappy_bird_ml.game import run_game, simmulate_game_state
from flappy_bird_ml.game.constants import BIRD_X, PIPE_GAP, PIPE_SPACING
from flappy_bird_ml.game.controller import Controller
from flappy_bird_ml.game.state import Bird, Pipe


class EfficientQLearner(Controller):
    def __init__(self):
        # We use a lower Alpha and a higher Gamma for stability
        self.q_table = defaultdict(lambda: [0.0, 0.0])  # Q-values for each state-action pair
        self.alpha = 0.1  # Learning rate for Q updates how strongly new rewards update old Q-values
        self.gamma = 1.0  # Discount factor for future rewards : how much future rewards matter vs immediate rewardx
        self.epsilon = 0.001  # Exploration rate for random actions probability of choosing a random action. Higher = more exploration; lower = more exploitation of learned policy.

        self.prev_state = None
        self.prev_action = None

    def discretize(self, bird, pipe) -> Tuple:
        """
        Efficient State: Reduce the number of possible states.
        The bird doesn't need to see 500px ahead. 140px is enough.
        """
        # 1. Horizontal distance capped at 140px (reduces state table size)
        dx = min(PIPE_SPACING, (pipe.x - BIRD_X)) // 10

        # 2. Vertical distance to the gap center
        gap_center = pipe.gap_bottom_y + (PIPE_GAP // 2)
        dy = (bird.y - gap_center) // 10

        # 3. Velocity (coarse bins to prevent 'overthinking')
        vel = int(bird.velocity)

        return (dx, dy, vel)

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.choice([0, 1])
        # Return index of max value
        return 0 if self.q_table[state][0] >= self.q_table[state][1] else 1

    def step_update(self, bird, pipe, done):
        if self.prev_state is None:
            return

        next_state = self.discretize(bird, pipe)

        # REWARD SHAPING: This is the 'secret sauce'
        # Default survival reward is low.
        actual_reward = 0.1

        # Massive penalty for dying
        if done:
            actual_reward = -1000
        # Reward for being vertically aligned with the gap
        elif abs(bird.y - (pipe.gap_bottom_y + PIPE_GAP // 2)) < 20:
            actual_reward = 1

        # Update
        old_q = self.q_table[self.prev_state][self.prev_action]
        max_future_q = max(self.q_table[next_state])
        self.q_table[self.prev_state][self.prev_action] += self.alpha * (
            actual_reward + self.gamma * max_future_q - old_q
        )

    def will_flap(self, bird, next_pipe) -> bool:
        state = self.discretize(bird, next_pipe)
        action = self.select_action(state)
        self.prev_state = state
        self.prev_action = action
        return action == 1


def train_efficiently(episodes=10000):
    ctl = EfficientQLearner()

    # Optional: Load previous progress to keep training
    # ctl.load()

    score = 0
    total = 0
    for ep in range(episodes):
        # Start conditions
        b = Bird(y=256, velocity=0)

        c_score = simmulate_game_state(ctl, bird=b, cb=ctl.step_update)
        score = max(score, c_score)
        total += c_score

        if ep % 5000 == 0:
            print(
                f"Episode {ep} | States: {len(ctl.q_table)} | Score: {score} | avg {total / 5000: 0.2f}"
            )
            score = 0
            total = 0

    # Save the 'Brain'
    with open(
        Path(__file__).parent.parent.parent.parent / "models" / "q_model.pickle", "wb"
    ) as f:
        pickle.dump(dict(ctl.q_table), f)
    return ctl


def load_model():
    with open(
        Path(__file__).parent.parent.parent.parent / "models" / "q_model.pickle", "rb"
    ) as f:
        table = pickle.load(f)
        ctl = EfficientQLearner()
        ctl.q_table = defaultdict(lambda: [0.0, 0.0], table)
        ctl.epsilon = 0

    return ctl


if __name__ == "__main__":
    # Train
    # ctl = train_efficiently(1500000)

    ctl = load_model()

    # Test
    ctl.epsilon = 0
    run_game(ctl, "q_learn")
