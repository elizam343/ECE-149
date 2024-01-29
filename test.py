
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


"""