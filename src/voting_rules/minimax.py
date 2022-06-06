import numpy as np


# minimax_winner_idx returns an index of a winner under Minimax method
def minimax_winner_idx(distance, candidates):
    return np.argmax(minimax_score(distance, candidates))


def net_score(distance, candidate):
    net = np.zeros([len(candidate), len(candidate)], dtype=int)
    rankings = np.zeros([len(distance), len(distance[0])], dtype=int)

    for v, preferences in enumerate(distance):
        rankings[v] = np.argsort(preferences)

    for c_idx, c in enumerate(candidate):
        for ranking in rankings:
            for c_prim in reversed(ranking):
                if c_prim == c_idx:
                    break
                net[c_idx][c_prim] += 1
    return net


def minimax_score(distance, candidate):
    minimax = np.zeros([len(candidate)])
    net = net_score(distance, candidate)
    for c_idx, c_nets in enumerate(net):
        n = np.concatenate((c_nets[:c_idx], c_nets[c_idx+1:]))
        minimax[c_idx] = np.min(n)
    return minimax
