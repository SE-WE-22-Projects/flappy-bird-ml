# Flappy Bird Q-Learning Solver

This module contains the Reinforcement Learning (Q-Learning) implementation for the Flappy Bird AI. The AI learns to play the game from scratch by interacting with the environment, receiving rewards for staying alive, and getting penalized for crashing.

## 🚀 How to Use

The main entry point for the Q-Learning algorithm is the `__init__.py` file.

### 1. Training the AI
To train the AI to play the game, you need to set the script to training mode. 

1. Open `__init__.py`.
2. Scroll to the bottom of the file to the `if __name__ == "__main__":` block.
3. Set the `IS_TRAINING` variable to `True`:
   ```python
   IS_TRAINING = True
   ```
4. Run the file:
   ```bash
   python -m flappy_bird_ml.solvers.q_learn
   ```
*Note: Training headless (without the game UI) is extremely fast. The model will automatically save to `models/q_model.pickle` after training is complete.*

### 2. Testing / Watching the AI Play
Once the model is trained and saved, you can watch it play!

1. Open `__init__.py`.
2. Scroll to the bottom and set `IS_TRAINING` to `False`:
   ```python
   IS_TRAINING = False
   ```
3. Run the file:
   ```bash
   python -m flappy_bird_ml.solvers.q_learn
   ```
This will load the saved brain (`q_model.pickle`), disable random exploration (`ctl.epsilon = 0`), and open the game window so you can watch the AI fly.

---

## 🧠 How It Works (Overview)

The implementation is broken down into a few key concepts:

*   **State (`discretize`)**: The bird reduces the complex game screen into 3 simple numbers: horizontal distance to the pipe, vertical distance to the gap, and its current velocity.
*   **Action (`select_action`)**: The bird decides whether to flap (1) or do nothing (0). It uses an Epsilon-Greedy policy, meaning it mostly uses its learned knowledge, but sometimes explores randomly to find better paths.
*   **Rewards (`step_update`)**: 
    *   **+1.0**: For flying safely aligned with the gap.
    *   **+0.1**: For surviving a frame.
    *   **-1000**: For hitting a pipe or the ground.
*   **Learning**: The algorithm uses the Bellman Equation to update a massive "cheat sheet" (the Q-Table) mapping every state to the best possible action based on past rewards.

## ⚙️ Hyperparameters
If you want to experiment with the AI's learning behavior, you can tweak these values in the `EfficientQLearner` class:
*   `alpha = 0.1`: The learning rate. How quickly the AI overwrites old information with new information.
*   `gamma = 1.0`: The discount factor. How much the AI cares about long-term survival vs short-term survival.
*   `epsilon = 0.001`: The exploration rate. The percentage of time the AI tries a completely random move instead of relying on its training.
