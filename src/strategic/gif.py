import os
import imageio
import random
from matplotlib import pyplot as plt
from src.strategic import random_select
from src.strategic.calculate import calc_winners

eps = [0.1, 0.2, 0.3, 0.4, 0.5]


def simulation_gif(loc1, size1, loc2, size2, rule,
                   repeats, voters_sets_num, out_filename):

    # randomly select candidates with accordance with given normal distributions
    candidates = random_select.get_candidates(loc1, size1, loc2, size2)
    # prepare sample sets of voters with the same distribution as candidates
    voters_probe = random_select.get_voter_sets(loc1, size1, loc2, size2, voters_sets_num)

    filenames = []
    for j in range(repeats):
        arr = {}
        for i in range(-40, 40):
            arr[round(i * 0.1, 1)] = 0
        for v in candidates:
            arr[round(v, 1)] += 1 / len(candidates)

        density, counts_all = calc_winners(candidates, voters_probe, rule)

        # single gif frame
        plt.plot(arr.keys(), arr.values(), color='red')  # red plot- distribution of candidates
        plt.plot(density.keys(), density.values(), alpha=0.3)  # bue plot - winner density

        # create file name and append it to a list
        filename = f'{j}.png'
        filenames.append(filename)

        # repeat last frame
        if j == repeats - 1:
            for i in range(15):
                filenames.append(filename)

        # save frame
        plt.savefig(filename)
        plt.close()

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
        candidates[c_to_move] = new_max

    # build gif
    with imageio.get_writer(out_filename, mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    # remove files
    for filename in set(filenames):
        os.remove(filename)

    return
