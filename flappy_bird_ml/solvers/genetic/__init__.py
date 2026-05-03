import numpy

from flappy_bird_ml.game import run_game
from flappy_bird_ml.solvers import model_dir
from flappy_bird_ml.solvers.genetic.alg import (
    GENERATIONS,
    POP_SIZE,
    best_individual,
    evaluate_fitness,
    evolve,
    init_population,
)
from flappy_bird_ml.solvers.genetic.controller import GeneticController


def train():
    print(f"Population size: {POP_SIZE}")
    print(f"Generations     : {GENERATIONS}")

    pop = init_population()
    fitness = evaluate_fitness(pop)

    best_theta, avg_score, best_score = best_individual(pop, fitness)
    print(f"Initial best score: {best_score:.3f}  | Average Score: {avg_score:.3f}")

    for gen in range(1, GENERATIONS + 1):
        pop, fitness = evolve(pop, fitness)

        current_best_theta, avg_score, current_best_score = best_individual(
            pop, fitness
        )

        print(
            f"Gen {gen:03d} | Best: {current_best_score:.3f}  | Average: {avg_score:.3f}"
        )

        if current_best_score > best_score:
            best_theta = current_best_theta
            best_score = current_best_score

    print("Weights (bias + w_y, w_v, w_d, w_gap_y):")
    print(best_theta)

    numpy.save(model_dir() / "genetic.npy", best_theta)

    run_game(GeneticController(best_theta), alg_name="Genetic")


def play():
    best_theta = numpy.load(model_dir() / "genetic.npy")
    run_game(GeneticController(best_theta), alg_name="Genetic")


if __name__ == "__main__":
    IS_TRAINING = True
    if IS_TRAINING:
        train()
    else:
        play()
