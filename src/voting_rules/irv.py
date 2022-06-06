import math
import numpy as np
from src.utils.utils import conditional_jit


# irv_winner_idx returns an index of a winner under IRV method
def irv_winner_idx(distance, candidates):
    return irv_algorithm(distance, candidates)


# irv_algorithm simulates subsequent election rounds under IRV rule until one of the candidates reaches quota
def irv_algorithm(distances, candidates):
    quota = math.floor(len(candidates)/2) + 1  # majority of votes
    counts = np.bincount(determine_winners(distances))  # number of received votes in given election round per candidate
    i = len(counts)
    while i < len(candidates):
        counts = np.append(counts, 0)
        i += 1

    while True:  # loop until any candidate reaches quota
        counts = del_zeros(counts)
        if np.max(counts) >= quota:
            return np.argmax(counts)  # quota is reached
        add_points = np.empty(0, dtype=int)
        counts = clean_distances(distances, counts, add_points)  # eliminate the weakest candidate and transfer points


# determine_winners returns a dict of winners per each voter
def determine_winners(distance):
    winners = np.zeros(len(distance), dtype=int)
    winners_per_voters(distance, winners)
    return winners


@conditional_jit()
def winners_per_voters(distance, winners):
    for v, voter_preferences in enumerate(distance):
        winners[v] = np.argmin(voter_preferences)  # winner for 'v' is a candidates closest to its location
    return


# del_zeros eliminates candidates with zero votes
@conditional_jit()
def del_zeros(counts):
    for i, c in enumerate(counts):
        if c == 0:
            counts[i] = -1
    return counts


# clean_distances eliminates candidates with the least amount of voters and transfers its points to the next candidate
# in corresponding preference ranking
@conditional_jit()
def clean_distances(d, counts, add_points):
    sorted_counts = np.sort(counts)
    # determine candidate to eliminate
    min_count = -1
    for c in sorted_counts:
        if c > -1:  # -1 means that candidate was already eliminated so we have to skip them
            min_count = c
            break
    candidate_to_eliminate = -1
    for idx, c in enumerate(counts):
        if c == min_count:
            candidate_to_eliminate = idx
            break

    if counts[candidate_to_eliminate] == 0:
        # there are no votes to transfer
        counts[candidate_to_eliminate] = -1
        return counts

    # transfer votes
    for v, v_preferences in enumerate(d):
        ranking = np.argsort(v_preferences)
        if ranking[0] == candidate_to_eliminate:
            idx = 1
            while idx < len(ranking) and ranking[idx] < len(counts) and counts[ranking[idx]] <= 0:
                idx += 1
            if idx < len(ranking):
                add_points = np.append(add_points, ranking[idx])

    add = counts[candidate_to_eliminate] / len(add_points)
    for c in add_points:
        counts[c] += add
    counts[candidate_to_eliminate] = -1  # mark that candidate was eliminated
    return counts

