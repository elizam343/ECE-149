import unittest
import numpy as np
from ComputeValue import ComputeValue 

class TestComputeValue(unittest.TestCase):

    def test_symmetric_game(self):
        """
        Test a symmetric game where the optimal strategy is (0.5, 0.5) for both players.
        """
        M = np.array([[1, -1], [-1, 1]])
        P1, P2, V1, V2 = ComputeValue(M)
        print(f"Symmetric game result: P1={P1}, P2={P2}, V1={V1}, V2={V2}")  # Display results
        self.assertAlmostEqual(P1, 0.5)
        self.assertAlmostEqual(P2, 0.5)
        self.assertAlmostEqual(V1, 0)
        self.assertAlmostEqual(V2, 0)

    def test_dominated_strategy(self):
        """
        Test a game where one strategy dominates the other for one player.
        """
        M = np.array([[3, 2], [1, 4]])
        P1, P2, V1, V2 = ComputeValue(M)
        print(f"Dominated strategy result: P1={P1}, P2={P2}, V1={V1}, V2={V2}")  # Display results
        self.assertGreaterEqual(P1, 0)
        self.assertGreaterEqual(P2, 0)
        self.assertLessEqual(P1, 1)
        self.assertLessEqual(P2, 1)
        self.assertNotEqual(V1, 0)  # In a non-symmetric game, the value should not be zero.
        self.assertEqual(V1, -V2)  # Confirming it's a zero-sum game.

    def test_all_positive_payoffs(self):
        """
        Test a game with all positive payoffs.
        """
        M = np.array([[4, 3], [2, 5]])
        P1, P2, V1, V2 = ComputeValue(M)
        print(f"All positive payoffs result: P1={P1}, P2={P2}, V1={V1}, V2={V2}")  # Display results
        self.assertGreaterEqual(P1, 0)
        self.assertGreaterEqual(P2, 0)
        self.assertLessEqual(P1, 1)
        self.assertLessEqual(P2, 1)
        self.assertNotEqual(V1, 0)  # Ensuring non-zero game value.
        self.assertEqual(V1, -V2)  # Zero-sum game check.

if __name__ == '__main__':
    unittest.main(verbosity=2)
