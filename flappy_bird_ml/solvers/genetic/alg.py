import numpy as np

from flappy_bird_ml.game import simmulate_game
from flappy_bird_ml.solvers.genetic.controller import GeneticController

# number of individuals per generation
POP_SIZE = 100
# how many generations to run
GENERATIONS = 200
# probability that a gene is copied from parent A
CROSSOVER_RATE = 0.5
# probability each weight is perturbed
MUTATION_RATE = 0.1
# standard deviation of Gaussian noise
MUTATION_STD = 0.02


FEATURES = ["y", "v", "d", "gap_y"]


def init_population():
    """Return an array (POP_SIZE × (len(FEATURES)+1)) of random weights."""
    dim = len(FEATURES) + 1  # +1 for bias
    return np.random.randn(POP_SIZE, dim)


def evaluate_fitness(pop):
    """
    Return a fitness vector: higher is better.
    Each individual is evaluated by `run_game(theta)` (avg over episodes).
    """
    fitness = []
    for theta in pop:
        score = simmulate_game(GeneticController(theta))  # 5 episodes per evaluation
        fitness.append(score)
    return np.array(fitness)


def tournament_selection(pop, fitness, k=3):
    """Return a new population by selecting best of `k` random draws."""
    new_pop = []
    for _ in range(POP_SIZE):
        idxs = np.random.choice(np.arange(len(pop)), size=k, replace=False)
        winner = pop[idxs[np.argmax(fitness[idxs])]]
        new_pop.append(winner.copy())
    return np.array(new_pop)


def crossover(parent_a, parent_b):
    """Uniform crossover – each gene chosen from A or B with 0.5 probability."""
    mask = np.random.rand(*parent_a.shape) < CROSSOVER_RATE
    child = np.where(mask, parent_a, parent_b)
    return child


def mutate(individual):
    """Add Gaussian noise to weights that survive the mutation test."""
    mask = np.random.rand(*individual.shape) < MUTATION_RATE
    individual[mask] += np.random.randn(int(np.count_nonzero(mask))) * MUTATION_STD
    return individual


def evolve(pop, fitness):
    """
    One GA iteration: selection → crossover → mutation.
    Returns new population and its fitness.
    """
    # 1. Selection
    pop_sel = tournament_selection(pop, fitness)

    # 2. Crossover (pairwise)
    children = []
    for i in range(0, POP_SIZE, 2):
        a = pop_sel[i]
        b = pop_sel[(i + 1) % POP_SIZE]
        child_a = crossover(a, b)
        child_b = crossover(b, a)
        children.extend([child_a, child_b])

    # 3. Mutation
    mutated_children = [mutate(c) for c in children]

    new_pop = np.array(mutated_children)
    new_fit = evaluate_fitness(new_pop)

    return new_pop, new_fit


def best_individual(pop, fitness):
    """Return the best theta and its score."""
    idx = np.argmax(fitness)
    theta = pop[idx]
    return theta, fitness[idx]
