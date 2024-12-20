import unittest
from main import check_and_mark_squares, count_scores

class TestCondotGame(unittest.TestCase):

    def test_check_and_mark_squares(self):
        board = [[0 for _ in range(13)] for _ in range(13)]
        for r in range(1, 13):
            for c in range(1, 13):
                if r % 2 != 0 and c % 2 != 0:
                    board[r][c] = -50

        board[4][3] = 1
        board[4][5] = 1
        board[3][4] = 1
        board[5][4] = 1


        check_and_mark_squares(board, 1)

        self.assertEqual(board[4][4], 'A')

    def test_count_scores(self):
        board = [[0 for _ in range(13)] for _ in range(13)]
        for r in range(1, 13):
            for c in range(1, 13):
                if r % 2 != 0 and c % 2 != 0:
                    board[r][c] = -50

        board[4][4] = 'A'
        board[6][6] = 'B'
        board[8][8] = 'A'  #


        human_score, computer_score = count_scores(board)


        self.assertEqual(human_score, 2)
        self.assertEqual(computer_score, 1)

if __name__ == '__main__':
    unittest.main()