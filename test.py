
"""
P1 = np.load('P1.npy')
P2 = np.load('P2.npy')

proposal_list, num_stages = GaleShapleyAlgorithm(P1, P2)
print_proposal_stages(proposal_list)
print(num_stages)
"""


"""
def print_npy_file(file_path):
    try:
        # Load the array from the .npy file
        array = np.load(file_path)

        # Print the array
        print(array)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
print_npy_file("example_1.npy")


def array_to_dict(file_path):
    try:
        # Load the array from the .npy file
        array = np.load(file_path)

        # Initialize an empty dictionary
        array_dict = {}

        # Iterate over the rows of the array
        for i, row in enumerate(array):
            # Assign each row to a key in the dictionary
            key = chr(65 + i)  # 65 is the ASCII code for 'A'
            array_dict[key] = row

        return array_dict
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
array_dict = array_to_dict("example_1.npy")
print(array_dict)


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


import numpy as np

# Import the functions from the implementation
from my_gale_shapley import GaleShapleyAlgorithm, GaleShapleyAlgorithmQuota

# Sample preference matrices (you can replace these with your own)
P1 = np.array([[1, 0, 2], [0, 2, 1], [1, 0, 2]])
P2 = np.array([[1, 0, 2], [0, 2, 1], [1, 0, 2]])

# Run Gale-Shapley Algorithm
proposal_list, num_stages = GaleShapleyAlgorithm(P1, P2)
print("Gale-Shapley Algorithm Results:")
print("Proposal List:")
for i, proposals in enumerate(proposal_list):
    print(f"Stage {i + 1}: {proposals}")
print("Number of Stages:", num_stages)

# Sample preference matrices (larger P1 with the same number of hospitals as P2)
Q1 = np.array([[1, 0, 2, 3], [0, 2, 1, 3], [1, 0, 2, 3]])
Q2 = np.array([[1, 0, 2], [0, 2, 1], [1, 0, 2], [2, 1, 0]])

# Sample quotas for Gale-Shapley Algorithm with Quotas (you can replace these with your own)
quota = np.array([1, 2, 1])

# Run Gale-Shapley Algorithm with Quotas
match, num_stages = GaleShapleyAlgorithmQuota(Q1, Q2, quota)
print("\nGale-Shapley Algorithm with Quotas Results:")
print("Matching Matrix:")
print(match)
print("Number of Stages:", num_stages)