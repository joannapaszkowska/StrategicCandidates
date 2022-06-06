import numpy as np


# copeland_winner_idx returns an index of a winner under Copeland method
def copeland_winner_idx(distance, candidates):
    return np.argmax(copeland_score(distance, candidates))


def copeland_score(distance, candidate):
    copeland = np.zeros(len(distance[0]))
    for i in range(len(candidate)):
        defeats = np.zeros(len(candidate))  # defeats[x] = n -> 'i' was better than 'x' n times
        for v, preferences in enumerate(distance):  # check in every voter's preferences
            ranking = np.argsort(preferences)
            for c in reversed(ranking):
                if i == c:
                    break
                defeats[c] += 1
        for c, no_wins in enumerate(defeats):
            if no_wins > (len(distance) / 2):
                copeland[i] += 1
    return copeland
