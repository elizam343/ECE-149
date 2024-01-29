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
        P1 (numpy.ndarray): An m x n matrix describing the preferences of the agents in Group 1.
        P2 (numpy.ndarray): An m x n matrix describing the preferences of the agents in Group 2.

    Returns:
        Match (numpy.ndarray): An m x n matrix which indicates the matches after running the algorithm.
        NumStages (int): The number of stages that it takes the Gale-Shapley algorithm to return a proposal.
    '''
    group1_preferences = convert_group1_to_dict(P1)
    group2_preferences = convert_group2_to_dict(P2)

    # Initialize proposals and last_choices
    proposals = {chr(65 + i): group1_preferences[chr(65 + i)][0] for i in range(P1.shape[0])}
    last_choices = {chr(65 + i): -1 for i in range(P1.shape[0])}
    proposal_list = [proposals.copy()]  # List to store proposals at each stage

    matches = {chr(97 + i): None for i in range(P2.shape[1])}
    num_stages = 0

    proposers = {chr(65 + i): 0 for i in range(P1.shape[0])}  # Track proposee index for each proposer

    while True:
        num_stages += 1
        new_proposals = {}

        # Process each proposal
        for proposer, proposee_index in proposals.items():
            proposee = group1_preferences[int(ord(proposer) - 65)][proposee_index]

            # Check if proposee is a valid member of Group 2 (0, 1, 2, ...)
            if 0 <= proposee < P2.shape[1]:
                # If the proposee already has a better match (more preferred than proposer), skip
                if matches[chr(proposee + 97)]:
                    proposee_matches = matches[chr(proposee + 97)]
                    if group2_preferences[chr(proposee_matches + 97)].index(
                            group1_preferences[chr(proposee_matches + 65)][0]) < \
                            group2_preferences[chr(proposer + 97)].index(
                                group1_preferences[chr(proposer + 65)][0]):
                        continue
                # Update the match
                matches[chr(proposee + 97)] = proposer
                last_choices[proposer] = proposee  # Update last choice for proposer
            else:
                # Handle the case where proposee is not a valid member of Group 2 (optional)
                print(f"Invalid proposee: {proposee}")

        # Check if any proposer needs to propose to the next choice
        for proposer in proposers:
            if proposers[proposer] < P2.shape[1] - 1:
                last_choice = last_choices[proposer]
                next_choice_index = group1_preferences[int(ord(proposer) - 65)].tolist().index(last_choice) + 1
                while next_choice_index < P1.shape[1]:
                    next_choice = group1_preferences[int(ord(proposer) - 65)][next_choice_index]
                    if not any(new_proposals[p] == next_choice for p in new_proposals) and next_choice >= 0:
                        new_proposals[proposer] = next_choice
                        proposers[proposer] += 1
                        break
                    next_choice_index += 1

        # Add current stage proposals to the list
        if new_proposals:
            proposal_list.append(new_proposals.copy())

        # Break the loop if there are no new proposals
        if not new_proposals:
            break

    # Convert the final matching into a numpy array
    Match = np.zeros((P1.shape[0], P2.shape[1]), dtype=int)
    for proposer, proposee in matches.items():
        if proposer is not None and proposee is not None:
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

    P1 = np.load(P1)  # Load P1 from file
    P2 = np.load(P2)  # Load P2 from file
    
    group1_preferences = convert_group1_to_dict(P1)
    group2_preferences = convert_group2_to_dict(P2)

    # Initialize proposals, last_choices, and Match
    proposals = {chr(65 + i): group1_preferences[chr(65 + i)][0] for i in range(P1.shape[0])}
    last_choices = {chr(65 + i): -1 for i in range(P1.shape[0])}
    Match = {}  # Dictionary to store matches

    matches = {chr(97 + i): None for i in range(P2.shape[1])}
    num_stages = 0

    while True:
        num_stages += 1
        new_proposals = {}

        # Process each proposal
        for proposer in list(proposals.keys()):  # Make a list of keys to avoid dictionary size change error
            proposee = proposals[proposer]
            # Check if proposee is a valid member of Group 2 (0, 1, 2, ...)
            if 0 <= proposee < P2.shape[1]:
                # If the proposee already has a better match (more preferred than proposer), skip
                if matches[chr(proposee + 97)]:
                    proposee_matches = matches[chr(proposee + 97)]
                    if group2_preferences[chr(proposee + 97)].index(group1_preferences[proposee_matches]) < group2_preferences[chr(proposee + 97)].index(proposer):
                        continue
                # Check if the quota for the proposee's college is not full
                if list(Match.values()).count(proposee) < quota[proposee]:
                    Match[proposer] = proposee
                    last_choices[proposer] = proposee  # Update last choice for proposer
                else:
                    # Handle the case where the quota is full
                    least_preferred = min([p for p in list(Match.keys()) if Match[p] != -1], key=lambda x: group2_preferences[chr(proposee + 97)].index(x))
                    Match[least_preferred] = -1
                    new_proposals[least_preferred] = group1_preferences[least_preferred][group2_preferences[chr(proposee + 97)].index(least_preferred) + 1:]
                    Match[proposer] = proposee
                    new_proposals[proposer] = group1_preferences[proposer][group2_preferences[chr(proposee + 97)].index(proposer) + 1:]
            else:
                # Handle the case where proposee is not a valid member of Group 2 (optional)
                print(f"Invalid proposee: {proposee}")
                del proposals[proposer]  # Remove proposer from the list

        # Check if any proposer needs to propose to the next choice
        for proposer in list(proposals.keys()):  # Make a list of keys to avoid dictionary size change error
            if proposer not in Match:
                last_choice = last_choices[proposer]
                next_choice_index = group1_preferences[proposer].index(last_choice) + 1
                while next_choice_index < len(group1_preferences[proposer]):
                    next_choice = group1_preferences[proposer][next_choice_index]
                    if next_choice not in new_proposals.values() and next_choice >= 0:
                        new_proposals[proposer] = next_choice
                        break
                    next_choice_index += 1

        proposals = new_proposals

        # Break the loop if there are no new proposals
        if not proposals:
            break

    return Match, num_stages




"""
def print_proposal_stages(proposal_list):
    
    #Prints the list of proposals at each stage of the Gale-Shapley algorithm.
    
    for stage, proposals in enumerate(proposal_list, start=1):
        print(f"Stage {stage}:")
        for proposer, proposee in proposals.items():
            print(f"  {proposer} proposes to {proposee}")
        print()


# Load the arrays
applicants = np.load('applicants.npy')
colleges = np.load('colleges.npy')
college_quotas = np.load('college_quotas.npy')

# Run the Gale-Shapley algorithm with quotas
Match, NumStages = GaleShapleyAlgorithmQuota(applicants, colleges, college_quotas)

# Print the results
print("Matching Results:")
for student, college in Match.items():
    print(f"Student {student} matched with College {college}")
print(f"Number of Stages: {NumStages}")


# Load the arrays
applicants = np.load('applicants.npy')
colleges = np.load('colleges.npy')
college_quotas = np.load('college_quotas.npy')

# Run the Gale-Shapley algorithm with quotas
Match, NumStages = GaleShapleyAlgorithmQuota(applicants, colleges, college_quotas)

# Print the results
print("Matching Results:")
for student, college in Match.items():
    print(f"Student {student} matched with College {college}")
print(f"Number of Stages: {NumStages}")

# Applicants preferences array
applicants = np.array([
    [1, 2, 3, 4],
    [2, 1, 4, 3],
    [3, 2, 1, 4],
    [4, 3, 2, 1],
    [1, 2, 3, 4],
    [2, 1, 4, 3],
    [3, 2, 1, 4]
])

# Corrected colleges preferences array with unique preferences
colleges = np.array([
    [1, 2, 3, 4],
    [2, 1, 4, 3],
    [3, 4, 1, 2],
    [4, 3, 2, 1]
])

# Quotas for colleges
quotas = np.array([2, 2, 2, 2])

# Save the arrays as .npy files
np.save('applicants.npy', applicants)
np.save('colleges.npy', colleges)
np.save('college_quotas.npy', quotas)



# Load the example files
applicants = np.load('applicants.npy')
colleges = np.load('colleges.npy')
college_quotas = np.load('college_quotas.npy')

# Test the Gale-Shapley Algorithm with Quotas
Match, NumStages = GaleShapleyAlgorithmQuota(applicants, colleges, college_quotas)

# Print the proposal stages and number of stages
print("Proposal Stages:")
for i, stage in enumerate(Match):
    print(f"Stage {i + 1}:")
    for j, match in enumerate(stage):
        print(f"  Applicant {j} matched with College {match}")

print("Number of Stages:", NumStages)
"""


