import numpy as np


# return coordinates of randomly selected candidates with accordance to given normal distributions params
def get_candidates(loc1, size1, loc2, size2):
    cand1 = np.random.normal(loc=loc1, scale=0.25, size=size1)  # randomly choose candidate from the first distribution
    cand2 = np.random.normal(loc=loc2, scale=0.25, size=size2)  # randomly choose candidate from the second distribution
    candidates = np.append(cand1, cand2)
    candidates.sort()
    return candidates


# get_voter_sets returns prepared sample sets of voters randomly selected from given normal distributions
def get_voter_sets(loc1, size1, loc2, size2, voters_sets_num):
    voters_probe = []
    for i in range(voters_sets_num):
        vot1 = np.random.normal(loc=loc1, scale=0.25, size=size1)
        vot2 = np.random.normal(loc=loc2, scale=0.25, size=size2)
        voters = np.append(vot1, vot2)
        voters_probe.append(voters)
    return voters_probe
