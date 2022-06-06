import numpy as np
from src.utils.utils import conditional_jit
from src.voting_rules.borda import borda_winner_idx
from src.voting_rules.codorcet import condorcet_winner_idx
from src.voting_rules.plurality import plurality_winner_idx
from src.voting_rules.positional import scoring_func_winner_idx, \
    harmonic_vector, harmonic_vector_rev
from src.voting_rules.irv import irv_winner_idx
from enum import Enum


# set of possible offsets
eps = [0.1, 0.2, 0.3]


class VotingRule(Enum):
    PLURALITY = 'plurality'
    BORDA = 'borda'
    HARMONIC = 'harmonic'
    HARMONIC_REVERSE = 'harmonic_reversed'
    CONDORCET = 'condorcet'
    IRV = 'irv'

    def __str__(self):
        return self.value


# calc_distances returns an array of distances between each voter and candidate
# distances[v][c] determines a distance between voter with index v and candidate with index c
@conditional_jit()
def calc_distances(candidates, voters, distances):
    for c, c_loc in enumerate(candidates):
        for v, v_loc in enumerate(voters):
            distances[v][c] = abs(c_loc - v_loc)
    return


# calc_winners returns dictionaries of winner densities and number of candidates per location rounded to two
# according to given voting rule
def calc_winners(candidates, voters_probe, rule):
    match rule:
        case VotingRule.PLURALITY:
            voting_rule_func = plurality_winner_idx
        case VotingRule.BORDA:
            voting_rule_func = borda_winner_idx
        case VotingRule.HARMONIC:
            voting_rule_func = scoring_func_winner_idx(harmonic_vector(len(candidates)))
        case VotingRule.HARMONIC_REVERSE:
            voting_rule_func = scoring_func_winner_idx(harmonic_vector_rev(len(candidates)))
        case VotingRule.CONDORCET:
            voting_rule_func = condorcet_winner_idx
        case VotingRule.IRV:
            voting_rule_func = irv_winner_idx
        case _:
            raise Exception("voting rule not implemented")

    wins = np.zeros(len(candidates))
    for voters in voters_probe:
        distances = np.zeros([len(voters), len(candidates)])
        calc_distances(candidates, voters, distances)
        winner = voting_rule_func(distances, candidates)
        wins[winner] += 1

    counts_winners = {round(i * 0.1, 2): 0 for i in range(-30, 35)}
    counts_all = {round(i * 0.1, 2): 0 for i in range(-30, 35)}

    for c, cval in enumerate(candidates):
        counts_winners[round(cval, 1)] += wins[c]
        counts_all[round(cval, 1)] += 1

    prob = {}
    for i, p in counts_winners.items():
        prob[i] = p / len(voters_probe)

    return prob, counts_all
