import numpy as np
'''
Skeleton code for Gale-Shapley algorithm.
Please do not change the filename or the function names!
'''



def convert_preferences(P, min_preference):
    """ Adjust preferences to start from 0 """
    return P - min_preference

def convert_group1_to_dict(P):
    """ Converts Group 1's preference matrix to a dictionary """
    group1_dict = {}
    for i, row in enumerate(P):
        key = chr(65 + i)  # 65 is ASCII for 'A'
        group1_dict[key] = list(row)
    return group1_dict

def convert_group2_to_dict(P):
    """ Converts Group 2's preference matrix to a dictionary """
    group2_dict = {}
    for i in range(P.shape[1]):
        key = chr(97 + i)  # 97 is ASCII for 'a'
        group2_dict[key] = list(P[:, i])
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
    # Determine if preferences start from 0 or 1
    min_preference = min(np.min(P1), np.min(P2))

    # Adjust the preference matrices
    P1_adjusted = convert_preferences(P1, min_preference)
    P2_adjusted = convert_preferences(P2, min_preference)

    # Convert the adjusted preference matrices to dictionaries
    group1_preferences = convert_group1_to_dict(P1_adjusted)
    group2_preferences = convert_group2_to_dict(P2_adjusted)

    proposals = {chr(65 + i): 0 for i in range(P1_adjusted.shape[0])}
    matches = {chr(97 + i): None for i in range(P2_adjusted.shape[1])}
    num_stages = 0

    while True:
        num_stages += 1
        new_proposals = {}

        for proposer in proposals:
            proposer_index = ord(proposer) - 65  # Convert proposer character to index (A -> 0, B -> 1, etc.)
            proposee_index = proposals[proposer]
            if proposee_index < len(group1_preferences[proposer]):
                proposee = group1_preferences[proposer][proposee_index]

                # Debugging print statements
                print("Proposer:", proposer, "Proposee:", proposee)
                print("Group 2 Preferences for proposee:", group2_preferences[chr(97 + proposee)])

                current_match = matches[chr(97 + proposee)]

                # Check if the proposer is preferred over the current match
                if current_match is None or group2_preferences[chr(97 + proposee)].index(proposer_index) < group2_preferences[chr(97 + proposee)].index(ord(current_match) - 65):
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
    # Determine if preferences start from 0 or 1
    min_preference = min(np.min(P1), np.min(P2))

    # Adjust the preference matrices
    P1_adjusted = convert_preferences(P1, min_preference)
    P2_adjusted = convert_preferences(P2, min_preference)

    # Convert the adjusted preference matrices to dictionaries
    group1_preferences = convert_group1_to_dict(P1_adjusted)
    group2_preferences = convert_group2_to_dict(P2_adjusted)

    proposals = {chr(65 + i): 0 for i in range(P1.shape[0])}
    last_choices = {chr(65 + i): None for i in range(P1.shape[0])}
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
                    last_choices[proposer] = proposee
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
                                    last_choices[proposer] = proposee
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
        for proposer in proposers:
            Match[ord(proposer) - 65, ord(proposee) - 97] = 1

    return Match, num_stages



