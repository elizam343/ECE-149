import numpy as np
'''
Skeleton code for Gale-Shapley algorithm.
Please do not change the filename or the function names!
'''




def convert_group1_to_dict(P1):
    """
    Converts Group 1's preference matrix to a dictionary.
    Rows become key values with uppercase alphabet letters as keys.
    """
    group1_dict = {}
    for i, row in enumerate(P1):
        key = chr(65 + i)  # 65 is ASCII for 'A'
        group1_dict[key] = list(row)
    return group1_dict

def convert_group2_to_dict(P2):
    """
    Converts Group 2's preference matrix to a dictionary.
    Columns become key values with lowercase alphabet letters as keys.
    """
    group2_dict = {}
    for i in range(P2.shape[1]):  # Iterate over columns
        key = chr(97 + i)  # 97 is ASCII for 'a'
        group2_dict[key] = list(P2[:, i])
    return group2_dict

def GaleShapleyAlgorithm(P1, P2):
    '''
    Runs the Gale-Shapley algorithm, where agents in Group 1 (the group corresponding to P1) propose.

    Args:
        P1 (numpy.ndarray): an m x n matrix describing the preferences of the agents in Group 1. Each row is preference of each of m riders.
        P2 (numpy.ndarray): an m x n matrix describing the preferences of the agents in Group 2. Each column is preference of each of n drivers.

    Returns:
        Match (numpy.ndarray): an m x n matrix which indicates the matches after running the algorithm.
        NumStages (int): the number of stages that it takes the Gale-Shapley algorithm to return a proposal.
    '''
    group1_preferences = convert_group1_to_dict(P1)
    group2_preferences = convert_group2_to_dict(P2)

    proposals = {chr(65 + i): 0 for i in range(P1.shape[0])}
    matches = {chr(97 + i): None for i in range(P2.shape[1])}
    num_stages = 0

    while True:
        num_stages += 1
        new_proposals = {}

        for proposer in proposals:
            proposee_index = proposals[proposer]
            if proposee_index < len(group1_preferences[proposer]):
                proposee = group1_preferences[proposer][proposee_index]
                current_match = matches[chr(97 + proposee)]

                if current_match is None or group2_preferences[chr(97 + proposee)].index(proposer) < group2_preferences[chr(97 + proposee)].index(current_match):
                    matches[chr(97 + proposee)] = proposer

        for proposer in proposals:
            proposee_index = proposals[proposer]
            if proposee_index < len(group1_preferences[proposer]):
                proposee = group1_preferences[proposer][proposee_index]
                if matches[chr(97 + proposee)] != proposer:
                    new_proposals[proposer] = proposee_index + 1

        if not new_proposals:
            break

        proposals = new_proposals

    Match = np.zeros((P1.shape[0], P2.shape[1]), dtype=int)
    for proposee, proposer in matches.items():
        if proposer is not None:
            Match[ord(proposer) - 65, ord(proposee) - 97] = 1

    return Match, num_stages





def GaleShapleyAlgorithmQuota(P1, P2, quota):
    '''
    Runs the Gale-Shapley algorithm, where agents in Group 1 (the group corresponding to P1) propose. Each agent in P2 has a number of spots available specified by the variable quota.

    Args:
        P1 (numpy.ndarray): an m x n matrix describing the preferences of the agents in Group 1. Each row is preference of each of m students.
        P2 (numpy.ndarray): an m x n matrix describing the preferences of the agents in Group 2. Each column is preference of each of n hospitals.
        quota (numpy.ndarray): an n x 1 vector describing the quota of each agent in Group 2.

    Returns:
        Match (numpy.ndarray): an m x n matrix which indicates the matches after running the algorithm. See the HW assignment for additional details on the structure of Match.
        NumStages (int): the number of stages that it takes the Gale-Shapley algorithm to return a proposal.
    '''
    group1_preferences = convert_group1_to_dict(P1)
    group2_preferences = convert_group2_to_dict(P2)

    proposals = {chr(65 + i): 0 for i in range(P1.shape[0])}
    matches = {chr(97 + i): [] for i in range(P2.shape[1])}
    num_stages = 0

    while True:
        num_stages += 1
        new_proposals = {}

        for proposer in proposals:
            proposee_index = proposals[proposer]
            if proposee_index < len(group1_preferences[proposer]):
                proposee = group1_preferences[proposer][proposee_index]

                if len(matches[chr(97 + proposee)]) < quota[proposee]:
                    matches[chr(97 + proposee)].append(proposer)
                else:
                    # Check if proposer is preferred over any current match
                    current_matches = matches[chr(97 + proposee)]
                    if proposer in group2_preferences[chr(97 + proposee)]:
                        proposer_rank = group2_preferences[chr(97 + proposee)].index(proposer)
                        for current_match in current_matches:
                            if current_match in group2_preferences[chr(97 + proposee)]:
                                current_match_rank = group2_preferences[chr(97 + proposee)].index(current_match)
                                if proposer_rank < current_match_rank:
                                    matches[chr(97 + proposee)].remove(current_match)
                                    matches[chr(97 + proposee)].append(proposer)
                                    new_proposals[current_match] = group1_preferences[current_match].index(last_choices[current_match]) + 1
                                    break

        for proposer in proposals:
            proposee_index = proposals[proposer]
            if proposee_index < len(group1_preferences[proposer]):
                proposee = group1_preferences[proposer][proposee_index]
                if proposer not in matches[chr(97 + proposee)]:
                    new_proposals[proposer] = proposee_index + 1

        if not new_proposals:
            break

        proposals = new_proposals

    Match = np.zeros((P1.shape[0], P2.shape[1]), dtype=int)
    for proposee, proposers in matches.items():
 




