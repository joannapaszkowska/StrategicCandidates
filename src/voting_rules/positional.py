import numpy as np
from src.utils.utils import conditional_jit


# scoring_func_winner_idx returns a function that returns an index of a winner under positional voting rule with
# scoring function defined by vector of weights
def scoring_func_winner_idx(weights):
    def f(distance, candidates):
        scores = np.zeros(len(distance))
        calculate_scores(distance, scores, weights)
        return np.argmax(scores)
    return f


@conditional_jit()
def calculate_scores(distance, harmonic, weights):
    for v, preferences in enumerate(distance):
        for i, c in enumerate(np.argsort(preferences)):
            harmonic[c] += weights[i]
    return


# harmonic_vector returns a vector filed with subsequent harmonic weights
def harmonic_vector(n):
    weights = np.zeros(n)
    for i in range(n):
        weights[i] = 1 / (i+1)
    return weights


# harmonic_vector_rev returns a vector filed with subsequent values of reversed harmonic function
def harmonic_vector_rev(n):
    weights = np.zeros(n)
    for i in range(n):
        weights[i] = 1 - (1 / (n-i))
    return weights
