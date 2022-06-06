from datetime import datetime
import random
import numpy as np
from src.strategic import random_select
from src.strategic.calculate import calc_winners, eps


def experiment_metrics_data(loc1, size1, loc2, size2, rule,
                            repeats, voters_sets_num):

    # randomly select candidates with accordance with given normal distributions
    candidates = random_select.get_candidates(loc1, size1, loc2, size2)
    # prepare sample sets of voters with the same distribution as candidates
    voters_probe = random_select.get_voter_sets(loc1, size1, loc2, size2, voters_sets_num)

    # number of last iterations to take into account for min/max metrics
    valid_reps = repeats / 2 if repeats < 1000 else 500
    # max_cand_in_loc[x] determines maximum number of candidates that were at once at all locations whose coordinates
    # round up to x in the last 'valid_reps' number of iterations
    max_cand_in_loc = {round(i * 0.1, 2): 0 for i in range(-30, 35)}
    # min_cand_in_loc[x] determines minimum number of candidates that were at once at all locations whose coordinates
    # round up to x in the last 'valid_reps' number of iterations
    min_cand_in_loc = {round(i * 0.1, 2): len(candidates) for i in range(-30, 35)}

    cand_movement = []  # array of position shifts of candidates in each iteration
    density = {}  # density of winners based on sample voters sets per coordinates rounded to one

    changed = True
    start = datetime.now()
    for j in range(repeats):
        if changed:
            density, counts_all = calc_winners(candidates, voters_probe, rule)

        c_to_move = random.randint(0, len(candidates) - 1)  # randomly select candidate to move
        # possibilities is a dictionary that determines winner densities at reachable for c_to_move locations
        possibilities = {candidates[c_to_move]: density[round(candidates[c_to_move], 1)]}
        for e in eps:  # fill in possibilities dict
            to_left = candidates[c_to_move] - e
            to_right = candidates[c_to_move] + e
            possibilities[to_right] = density[round(to_right, 1)]
            possibilities[to_left] = density[round(to_left, 1)]

        # choose entry with maximum winner density as new location
        new_max = max(possibilities, key=possibilities.get)
        if new_max != candidates[c_to_move]:
            changed = True
        old = candidates[c_to_move]
        candidates[c_to_move] = new_max
        cand_movement.append(np.abs(new_max - old))  # append candidate's position shift

        if j >= valid_reps:
            # update max/min number of candidates per location
            for loc, count in counts_all.items():
                if count > max_cand_in_loc[loc]:
                    max_cand_in_loc[loc] = count
                if count < min_cand_in_loc[loc]:
                    min_cand_in_loc[loc] = count

    print("time: ", datetime.now() - start)
    return max_cand_in_loc, min_cand_in_loc, cand_movement
