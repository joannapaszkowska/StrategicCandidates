import numpy as np


# veto_winner_idx returns an index of a winner under Veto method
def veto_winner(distance, candidates):
    veto = veto_scores(distance)
    return np.argmax(veto)


def veto_scores(distance):
    veto = np.zeros(len(distance[0]))
    for v, preferences in enumerate(distance):
        ranking = np.argsort(preferences)
        for i, c in enumerate(ranking):
            veto[c] += 0 if i == len(ranking) - 1 else 1
    return veto
