import numpy as np
from src.utils.utils import conditional_jit


# plurality_winner_idx returns an index of a winner under Plurality method
def plurality_winner_idx(distance, candidates):
    winners = np.empty(len(distance), dtype=int)
    plurality_loop(distance, winners)
    counts = np.bincount(winners)
    return np.argmax(counts)


# plurality_loop modifies winners array so that winners[voter_idx] is an index of s candidate
# who is most preferred by voter with given index
@conditional_jit()
def plurality_loop(distance, winners):
    for v, voter_preferences in enumerate(distance):
        winners[v] = np.argmin(voter_preferences)
    return
