from sudoku import *
from Solver import *
import random

def generate_complete_sudoku(board):
    """Generates a complete, random sudoku board"""

    numbers = list(range(1,10))
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

def random_reduce(board, free_spaces = None, depth = 0, max_depth = 60):
    if free_spaces == None:
        free_spaces = [(i, j) for  i in range(9) for j in range(9)]

    if depth >= max_depth:
        return board

    space = free_spaces[random.randrange(len(free_spaces))]

    temp_board = board.change(space[0], space[1], 0)
    if(has_unique_solution(temp_board)):
        free_spaces.remove(space)
        return random_reduce(temp_board, free_spaces, depth=depth +1, max_depth = max_depth)

    return random_reduce(board, free_spaces, depth=depth +1, max_depth = max_depth)

def generate_sudoku(max_depth):
    board = Board([[ 0 for j in range(9)] for i in range(9)])
    generate_complete_sudoku(board)
    boardr = random_reduce(board, max_depth = max_depth)

    return Sudoku(boardr, board)


def test():
    board = Board([[ 0 for j in range(9)] for i in range(9)])
    t1 = time.process_time()
    if generate_complete_sudoku(board):
        t2 = time.process_time()
        print("Generating a complete board took {}\n{}".format((t2-t1),board))
        board1 = random_reduce(board)
        t3 = time.process_time()
        print("Reducing the board took {}\n{}".format((t3-t2),repr(board1)))
    else:
        print("Failed!!")

def test2():
    t1 = time.process_time()
    sudoku = generate_sudoku(6)
    t2 = time.process_time()
    print("Generating a reduced board took {}\n{}".format((t2-t1),sudoku.board))
    print("heres its solution \n{}".format(sudoku.solution))
if __name__ == "__main__":
    test2()
