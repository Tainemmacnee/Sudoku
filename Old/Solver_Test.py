import unittest
from Solver import *
from Sudoku import Board


class TestSolverMethods(unittest.TestCase):

    def test_valid_in_row(self):
        board = Board([[3,0,6,5,0,8,4,0,0], 
                        [5,2,0,0,0,0,0,0,0], 
                        [0,8,7,0,0,0,0,3,1], 
                        [0,0,3,0,1,0,0,8,0], 
                        [9,0,0,8,6,3,0,0,5], 
                        [0,5,0,0,9,0,6,0,0], 
                        [1,3,0,0,0,0,2,5,0], 
                        [0,0,0,0,0,0,0,7,4], 
                        [0,0,5,2,0,6,3,0,0]])
        
        self.assertTrue(valid_in_row(board, 0, 2))
        self.assertFalse(valid_in_row(board, 0, 3))

    def test_valid_in_col(self):
        board = Board([[3,0,6,5,0,8,4,0,0], 
                        [5,2,0,0,0,0,0,0,0], 
                        [0,8,7,0,0,0,0,3,1], 
                        [0,0,3,0,1,0,0,8,0], 
                        [9,0,0,8,6,3,0,0,5], 
                        [0,5,0,0,9,0,6,0,0], 
                        [1,3,0,0,0,0,2,5,0], 
                        [0,0,0,0,0,0,0,7,4], 
                        [0,0,5,2,0,6,3,0,0]])

        self.assertTrue(valid_in_col(board, 0, 2))
        self.assertFalse(valid_in_col(board, 0, 1))

    def test_valid_in_box(self):
        board = Board([[3,0,6,5,0,8,4,0,0], 
                        [5,2,0,0,0,0,0,0,0], 
                        [0,8,7,0,0,0,0,3,1], 
                        [0,0,3,0,1,0,0,8,0], 
                        [9,0,0,8,6,3,0,0,5], 
                        [0,5,0,0,9,0,6,0,0], 
                        [1,3,0,0,0,0,2,5,0], 
                        [0,0,0,0,0,0,0,7,4], 
                        [0,0,5,2,0,6,3,0,0]])

        self.assertTrue(valid_in_box(board, 0, 0, 1))
        self.assertFalse(valid_in_box(board, 0, 0, 7))


if __name__ == '__main__':
    unittest.main()
