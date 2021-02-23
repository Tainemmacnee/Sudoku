import copy

class Sudoku:

    def __init__(self, board, solution):
        self.board = board
        self.solution = solution

class Board:

    def __init__(self, grid):
        self.grid = grid

    def get(self):
        return self.grid

    def change(self, row, col, value):
        new_board = copy.deepcopy(self)
        new_board.grid[row][col] = value
        return new_board

    def __str__(self):
        out = ""
        for i in range(9):
            for j in range(9):
                out += "{} ".format(self.grid[i][j])
            out += '\n'
        return out

    def __repr__(self):
        out = "["
        for i in range(8):
            out += "["
            for j in range(8):
                out += "{},".format(self.grid[i][j])
            out += "{}],\n".format(self.grid[i][8])
        out += "[{},{},{},{},{},{},{},{},{}]]".format(self.grid[8][0], self.grid[8][1], self.grid[8][2],\
                                                     self.grid[8][3], self.grid[8][4], self.grid[8][5],\
                                                     self.grid[8][6], self.grid[8][7], self.grid[8][8])
        return out

if __name__ == "__main__":
    board = Board([[ 0 for j in range(9)] for i in range(9)])
    print(repr(board))
