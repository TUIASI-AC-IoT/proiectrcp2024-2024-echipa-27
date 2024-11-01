import unittest
from app import sum_of_squares

class TestSumOfSquares(unittest.TestCase):
    def test_sum_of_squares(self):
        self.assertEqual(sum_of_squares(1), 1)
        self.assertEqual(sum_of_squares(2), 5)
        self.assertEqual(sum_of_squares(3), 14)
        self.assertEqual(sum_of_squares(4), 30)
        self.assertEqual(sum_of_squares(5), 55)

if __name__ == "__main__":
    unittest.main()