import numpy as np
import random
from src.utils.utils import conditional_jit


# condorcet_winner_idx return an index of randomly chosen candidates that are Condorcet winners
def condorcet_winner_idx(distance, candidates):
    winners = np.zeros(0, dtype=int)
    winners = compare_loop(distance, candidates, winners)
    return random.choice(winners)


# compare_loop returns all candidates that would win or draw with every other opponent
# in a pairwise Plurality election
@conditional_jit()
def compare_loop(distance, candidates, winners):
    for i, _ in enumerate(candidates):
        ok = True
        for j, _ in enumerate(candidates):
            res = compare_two(distance, i, j)
            if res == i or res == -1:
                continue
            ok = False
            break
        if ok:
            winners = np.append(winners, i)
    return winners


# compare_two checks which out of the two candidates would win a pairwise election
# under Plurality rule and returns an index of such winner
# if Plurality score of those two candidates is the same, function returns -1
@conditional_jit()
def compare_two(distance, cand1, cand2):
    score1, score2 = 0, 0
    for v, preferences in enumerate(distance):
        if distance[v][cand1] <= distance[v][cand2]:
            score1 += 1
        if distance[v][cand1] >= distance[v][cand2]:
            score2 += 1
    if score1 == score2:
        return -1
    return cand1 if score1 > score2 else cand2
