'''
Skeleton code for finding security strategies.
Please do not change the filename or the function names!
'''

import numpy as np

def ComputeValue(M):
    '''
    Computes the value and security strategies of a two-player, two-move, zero-sum game. Refer to the HW assignment for details on P1, P2, V1, V2, and M.
    '''

    ### WRITE YOUR CODE BELOW
    P1 = None
    P2 = None
    V1 = None
    V2 = None

    # Ensure the matrix M is in the correct shape (2x2)
    assert M.shape == (2, 2), "Matrix M must be of shape 2x2."

    # Calculate the game value and mixed strategies for both players.
    # For player 1 (P1)
    denominator = (M[0,0] - M[0,1] - M[1,0] + M[1,1])
    if denominator != 0:
        P1 = (M[1,1] - M[0,1]) / denominator
    else:
        P1 = 0.5 # Default to equal probability if denominator is 0, indicating possibly degenerate game

    # For player 2 (P2)
    if denominator != 0:
        P2 = (M[1,1] - M[1,0]) / denominator
    else:
        P2 = 0.5 # Default to equal probability if denominator is 0

    # Calculate game values for P1 (V1) and P2 (V2), using the mixed strategies
    V1 = P1 * (M[0,0] * (1-P2) + M[0,1] * P2) + (1-P1) * (M[1,0] * (1-P2) + M[1,1] * P2)
    V2 = -V1 # Since it's a zero-sum game

    ### DO NOT EDIT BELOW THIS LINE
    return P1, P2, V1, V2 