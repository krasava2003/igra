import unittest
from main import check_and_mark_squares, count_scores

class TestCondotGame(unittest.TestCase):

    def test_check_and_mark_squares(self):
        # Set up a sample game board with some moves
        board = [[0 for _ in range(13)] for _ in range(13)]
        for r in range(1, 13):
            for c in range(1, 13):
                if r % 2 != 0 and c % 2 != 0:
                    board[r][c] = -50

        # Simulate a player's move (1 = Human move)
        board[4][4] = 1  # Example move
        # Check if the function marks the squares correctly after the move
        check_and_mark_squares(board, 1)

        # Check if the square is marked with 'A' for human
        self.assertEqual(board[4][4], 'A')

    def test_count_scores(self):
        # Set up a sample game board with some closed squares
        board = [[0 for _ in range(13)] for _ in range(13)]
        for r in range(1, 13):
            for c in range(1, 13):
                if r % 2 != 0 and c % 2 != 0:
                    board[r][c] = -50

        # Simulate human and computer moves
        board[4][3] = 'A'  # Human's square
        board[6][7] = 'B'  # Computer's square
        board[5][4] = 'A'  # Another human's square

        # Check the scores
        human_score, computer_score = count_scores(board)

        # Assert the scores are correct
        self.assertEqual(human_score, 2)
        self.assertEqual(computer_score, 1)

if __name__ == '__main__':
    unittest.main()