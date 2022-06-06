import numpy as np
from src.utils.utils import conditional_jit


# borda_winner_idx returns an index of a winner under Borda method
def borda_winner_idx(distance, candidates):
    borda = np.zeros(len(distance))
    borda_scores(distance, borda)
    return np.argmax(borda)


# borda_scores returns an array that contains scores of every candidate under Borda rule
# borda[candidate_idx] determines borda score of candidate with given index
@conditional_jit()
def borda_scores(distance, borda):
    for v, preferences in enumerate(distance):
        for i, c in enumerate(np.argsort(preferences)):
            # voter grants m - i - 1 points to candidate at position i in their preference ranking
            borda[c] += len(distance[0]) - i - 1
    return


def borda_winner(distance, candidates):
    borda = np.zeros(len(distance))
    borda_scores(distance, borda)
    return candidates[np.argmax(borda)]

