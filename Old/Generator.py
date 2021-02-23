from Sudoku import Board
from Solver import *
import random

numbers = list(range(1,10))

def generate_complete_sudoku(board):
    """Generates a complete, random sudoku board"""
    random.shuffle(numbers)
    space = find_empty_space(board)

    if space == None:
        return True

    for num in numbers:
        if check_value_valid(board, num, space):
            board.get()[space[0]][space[1]] = num

            if (generate_complete_sudoku(board)):
                return True
            board.get()[space[0]][space[1]] = 0
    return False

def list_spaces():
    spaces = []
    for i in range(9):
        for j in range(9):
            spaces.append([i,j])
    return spaces

def reduce_sudoku(board):
    """Reduces the number of filled in spaces in a sudoku while maintining a uniquesolution"""
    spaces = list_spaces()
    random.shuffle(spaces)
    for space in spaces:
        value = board.get()[space[0]][space[1]]
        board.get()[space[0]][space[1]] = 0
        t1 = time.process_time()
        if(not has_unique_solution(board)):
            board.get()[space[0]][space[1]] = value
        t2 = time.process_time()
        print("testing for uniqueness took {}".format(t2-t1))

def random_reduce_sudoku(board, depth = 0, max_depth = 60):
    if depth >= max_depth:
        return board

    depth = depth + 1
    space = get_random_filled_space(board)
    value = board.get()[space[0]][space[1]]

    tempboard = board.change(space[0], space[1], 0)
    if(has_unique_solution(tempboard)):
        return random_reduce_sudoku(tempboard, depth=depth, max_depth = max_depth)

    return random_reduce_sudoku(board, depth=depth, max_depth = max_depth)

def get_random_filled_space(board):
    spaces = []
    for i in range(9):
        for j in range(9):
            if board.get()[i][j] != 0:
                spaces.append([i,j])
    return spaces[random.randrange(len(spaces))]

def test():

    board = Board([[ 0 for j in range(9)] for i in range(9)])
    t1 = time.process_time()
    if generate_complete_sudoku(board):
        t2 = time.process_time()
        print("Generating a complete board took {}\n{}".format((t2-t1),board))
        board = random_reduce_sudoku(board)
        t3 = time.process_time()
        print("Reducing the board took {}\n{}".format((t3-t2),repr(board)))
    else:
        print("Failed!!")

if __name__ == "__main__":
    test()
