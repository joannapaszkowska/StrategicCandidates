import os
import matplotlib.pyplot as plt
from src.strategic.calculate import VotingRule
import argparse
from src.strategic.gif import simulation_gif
from src.strategic.metrics import experiment_metrics_data
from src.utils.utils import set_numba


def plot_metrics(loc1, size1, loc2, size2,
                 rule,
                 iterations, voters_sets_num, reps,
                 dir, pref):
    arr_max = {round(i * 0.1, 2): 0 for i in range(-30, 35)}
    arr_min = {round(i * 0.1, 2): 0 for i in range(-30, 35)}
    arr_max_all = {round(i * 0.1, 2): 0 for i in range(-30, 35)}
    arr_min_all = {round(i * 0.1, 2): 100 for i in range(-30, 35)}
    print(loc1, size1, loc2, size2)
    cand_mov_all = [0 for _ in range(1000)]

    k = reps
    for i in range(k):
        print(i)

        max_in_loc, min_in_loc, cand_mov = experiment_metrics_data(loc1, size1, loc2, size2, rule, iterations,
                                                                   voters_sets_num)
        for num, mov in enumerate(cand_mov):
            cand_mov_all[num] += mov / k

        for loc, count in max_in_loc.items():
            arr_max[loc] += count / k
            if arr_max_all[loc] < count:
                arr_max_all[loc] = count

        for loc, count in min_in_loc.items():
            arr_min[loc] += count / k
            if arr_min_all[loc] > count:
                arr_min_all[loc] = count

    plt.plot(arr_min_all.keys(), arr_min_all.values(), 'b')
    plt.plot(arr_max_all.keys(), arr_max_all.values(), 'r')
    filename = f'{dir}/{pref}minmax_global_{rule}_{loc1}_{size1}_{loc2}_{size2}.png'
    plt.savefig(filename)
    plt.close()
    save_values_txt(f'{dir}/{pref}max_global_{rule}_{loc1}_{size1}_{loc2}_{size2}.txt', arr_max_all)
    save_values_txt(f'{dir}/{pref}min_global_{rule}_{loc1}_{size1}_{loc2}_{size2}.txt', arr_min_all)

    plt.plot(cand_mov_all)
    filename = f'{dir}/{pref}mobility_{rule}_{loc1}_{size1}_{loc2}_{size2}.png'
    plt.savefig(filename)
    plt.close()
    save_values_txt(f'{dir}/{pref}mobility_{rule}_{loc1}_{size1}_{loc2}_{size2}.txt', cand_mov_all)

    plt.plot(arr_min.keys(), arr_min.values(), 'b')
    plt.plot(arr_max.keys(), arr_max.values(), 'r')
    filename = f'{dir}/{pref}minmax_average_{rule}_{loc1}_{size1}_{loc2}_{size2}.png'
    plt.savefig(filename)
    save_values_txt(f'{dir}/{pref}max_average_{rule}_{loc1}_{size1}_{loc2}_{size2}.txt', arr_max)
    save_values_txt(f'{dir}/{pref}min_average_{rule}_{loc1}_{size1}_{loc2}_{size2}.txt', arr_min)

    plt.close()


def generate_gif(loc1, size1, loc2, size2, rule,
                 repeats, voters_sets_num, dir, pref):
    filename = f'{dir}/{pref}gif_{rule}_{loc1}_{size1}_{loc2}_{size2}.gif'
    simulation_gif(loc1, size1, loc2, size2, rule,
                   repeats, voters_sets_num, filename)


def save_values_txt(filename, arr):
    f = open(filename, 'w')
    f.write(arr.__str__())
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-gif", "--gif_mode", help="Determines experiment mode", default=False)

    parser.add_argument("-rule", "--voting_rule", help="Voting rule", type=VotingRule)

    parser.add_argument("-m1", "--mean1", help="Mean of the first Gaussian distribution", type=float, default=0.0)
    parser.add_argument("-s1", "--size1", help="Number of election participants from the first Gaussian distribution",
                        default=100, type=int)
    parser.add_argument("-m2", "--mean2", help="Mean of the second Gaussian distribution", type=float, default=0.0)
    parser.add_argument("-s2", "--size2", help="Number of election participants from the second Gaussian distribution",
                        default=0, type=int)

    parser.add_argument("-i", "--iterations", help="Number of election iterations", type=int, default=1000)
    parser.add_argument("-v_size", "--voters_sets", help="Number of sample voter sets", type=int, default=50)
    parser.add_argument("-reps", "--repetitions", help="Number of independent simulations per experiment", type=int,
                        default=50)

    parser.add_argument("-dir", "--directory", help="Output files directory")
    parser.add_argument("-pref", "--file_prefix", help="Output files prefix", default="")

    parser.add_argument("-numba", "--if_numba", help="Use numba compiler", default=True)

    args = parser.parse_args()
    set_numba(args.if_numba)
    if not os.path.exists(args.directory):
        os.makedirs(args.directory)

    if args.gif_mode:
        generate_gif(args.mean1, args.size1, args.mean2, args.size2,
                     args.voting_rule,
                     args.iterations, args.voters_sets,
                     args.directory, args.file_prefix)
    else:
        plot_metrics(args.mean1, args.size1, args.mean2, args.size2,
                     args.voting_rule,
                     args.iterations, args.voters_sets, args.repetitions,
                     args.directory, args.file_prefix)

