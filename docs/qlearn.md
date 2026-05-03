# Q-learning in Flappy Bird ML

This document is a short viva-ready explanation of how Q-learning is implemented and used in this project.

## 1) Big picture
- The game loop asks a controller each frame: "Should the bird flap?"
- The Q-learning controller answers that question using a learned Q-table.
- Training uses a lightweight simulator that provides rewards for good states and penalties for collisions.

## 2) Where it lives in the code
- Q-learning controller and training logic: flappy_bird_ml/solvers/q_learn/__init__.py
- Simulation used during training: flappy_bird_ml/game/__init__.py
- Game loop used during play: flappy_bird_ml/game/game.py
- Physics and collision: flappy_bird_ml/game/state.py
- Constants (gravity, flap speed, pipe gap): flappy_bird_ml/game/constants.py

## 3) State representation (discretized)
The controller converts the continuous game state into a discrete tuple:

State = (y_bin, vel_bin, dx_bin, dy_bin)

- y_bin: bird vertical position, bucketed by Y_BIN_SIZE
- vel_bin: bird velocity, bucketed by VEL_BIN_SIZE
- dx_bin: horizontal distance to the next pipe, bucketed by DX_BIN_SIZE
- dy_bin: vertical distance from bird to pipe gap center, bucketed by DY_BIN_SIZE

Why discretize:
- Keeps the state space finite and manageable.
- Allows a simple table to store values for each state-action pair.

## 4) Actions
Two actions:
- 0 = do nothing
- 1 = flap

The controller chooses actions using epsilon-greedy:
- With probability epsilon: random action (exploration)
- Otherwise: action with highest Q value (exploitation)

## 5) Q-learning update rule
The Q-table stores Q(state, action).

Update:
Q(s, a) = Q(s, a) + alpha * (reward + gamma * max_a' Q(s', a') - Q(s, a))

Meaning:
- alpha: learning rate (how fast we update)
- gamma: discount factor (value of future rewards)
- reward: immediate feedback from the simulator

## 6) Rewards used in training
The training simulator emits rewards on each step:
- Collision: large negative reward (-100000) and episode ends
- Pipe passed: +10 and episode ends
- Otherwise: small positive reward (+1 or +2), encourages staying in safe zones

Why these rewards:
- Strong penalty discourages crashes.
- Passing a pipe is the main objective.
- Small positive reward keeps the bird near a reasonable height.

## 7) Training procedure
- Training does not run the full visual game loop.
- It runs a fast simulation for many starting states:
  - iterate over pipe y positions
  - iterate over bird y positions
  - iterate over velocities
- Each simulated step calls controller.step_update(...) to apply the Q update.
- Epsilon decays each episode to reduce exploration over time.

## 8) How it is used at runtime
- During training: epsilon starts high to explore.
- For gameplay: epsilon is set to 0 (pure exploitation).
- The controller is passed into run_game(...) to play in the real game loop.

## 9) Files created during training
- The learned Q-table is saved as models/qlearn.pickle
- The file is loaded later to run the learned policy.

## 10) Strengths and limitations (talking points)
Strengths:
- Simple, explainable policy.
- Fast to train with a compact state space.
- Does not require a neural network or GPU.

Limitations:
- Discretization loses detail.
- Q-table size grows with state granularity.
- Rewards are hand-designed; behavior depends on reward shaping.

## 11) Short viva script (30-60 seconds)
"In this project, Q-learning controls the bird by choosing between two actions: flap or not flap. We discretize the game state into four bins: bird height, velocity, horizontal distance to the next pipe, and vertical distance to the pipe gap center. The controller uses epsilon-greedy to explore early on, then exploits the best Q values later. Training runs in a fast simulator that assigns rewards: a big penalty for collisions, a reward for passing pipes, and small positive rewards for staying in safe positions. The Q-table is updated using the standard rule with learning rate and discount factor. After training, epsilon is set to zero and the learned policy is used in the real game loop."

## 12) If asked "why Q-learning here?"
- The action space is tiny (flap or not), perfect for tabular Q-learning.
- The environment is simple and mostly deterministic.
- It provides a clear, interpretable baseline before trying more complex methods.
