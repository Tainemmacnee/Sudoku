from sudoku import Board
import copy
import time

def find_empty_space(board):
    for i in range(9):
        for j in range(9):
            if board.get()[i][j] == 0:
               return [i,j]
    return None

def valid_in_row(board, row, value):
    if all(board.get()[row][j] != value for j in range(9)):
        return True
    return False

def valid_in_col(board, col, value):
    if all(board.get()[i][col] != value for i in range(9)):
        return True
    return False

def valid_in_box(board, row, col, value):
    box_x = (row // 3)*3
    box_y = (col // 3)*3

    for i in range(box_x, box_x+3):
        for j in range(box_y, box_y+3):
            if board.get()[i][j] == value:
                return False
    return True

def check_value_valid(board, value, space):
    if valid_in_row(board, space[0], value) and valid_in_col(board, space[1], value) and valid_in_box(board, space[0], space[1], value):
        return True
    return False

def find_all_solutions(board):
    solutions = []

    space = find_empty_space(board)
    if space == None:
        solutions.append(board)
        return solutions

    for value in range(1, 10):
        if check_value_valid(board, value, space):

            tempboard = board.change(space[0], space[1], value)
            solutions += find_all_solutions(tempboard)

    return solutions

def find_max2_solutions(board):
    solutions = []

    space = find_empty_space(board)
    if space == None:
        solutions.append(board)
        return solutions

    for value in range(1, 10):
        if check_value_valid(board, value, space):

            tempboard = board.change(space[0], space[1], value)
            solutions += find_max2_solutions(tempboard)

            if(len(solutions) > 1):
                return solutions

    return solutions

def has_unique_solution(board):
    board2 = copy.deepcopy(board)
    return len(find_max2_solutions(board2)) == 1


if __name__ == "__main__":
    board = Board([[3,0,6,5,0,8,4,0,0],
[5,2,0,0,0,0,0,0,0],
[0,8,7,0,0,0,0,3,1],
[0,0,3,0,1,0,0,8,0],
[9,0,0,8,6,3,0,0,5],
[0,5,0,0,9,0,0,0,0],
[1,3,0,0,0,0,2,5,0],
[0,0,0,0,0,0,0,0,4],
[0,0,5,2,0,6,3,0,0]])
    t1 = time.process_time()
    solutions = find_all_solutions(board)
    t2 = time.process_time()
    if len(find_all_solutions(board)) > 0:

        print("Found {} solutions in {}s! Heres one \n{}".format(len(solutions), (t2-t1), solutions[0]))
    else:
        print("No solution exists")
"""
[[3,0,6,5,0,8,4,0,0],
[5,2,0,0,0,0,0,0,0],
[0,8,7,0,0,0,0,3,1],
[0,0,3,0,1,0,0,8,0],
[9,0,0,8,6,3,0,0,5],
[0,5,0,0,9,0,6,0,0],
[1,3,0,0,0,0,2,5,0],
[0,0,0,0,0,0,0,7,4],
[0,0,5,2,0,6,3,0,0]]
"""
