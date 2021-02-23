

class gGameView():

    def __init__(self, surface, board):
        self.surface = surface
        self.board = board
        self.tiles = []

        self.notations = False
        self.selectedTile = None

    def loadPanelsFromBoard(self, board):
        for i in range(9):
            row = []
            for j in range(9):
                if board[i][j] == 0:
                    row.append(SudokuTile(self.digits, i, j, False))
                else:
                    row.append(SudokuTile(self.digits, i, j, False))
                    row[j].fillNumber(board[i][j])
                    row[j].locked = True
            self.tiles.append(row)

    def clearTiles(self):
        for tile in (tile for row in self.tiles for tile in row):
            tile.setSelected(False)
            tile.setHighlighted(False)

    def findAdjacentPanels(self, pos):
        """returns list of cells that are in row, col or box of cell"""
        row, col = pos
        box_x = (row // 3)*3
        box_y = (col // 3)*3
        tiles = []
        for i in range(9):
            for j in range(9):
                if i == row:
                    tiles.append(self.tiles[i][j])
                if j == col:
                    tiles.append(self.tiles[i][j])
        for i in range(box_x, box_x+3):
            for j in range(box_y, box_y+3):
                tiles.append(self.tiles[i][j])
        return tiles

    def handleMouseUp(self):
        self.clearTiles()
        for tile in (tile for row in self.tiles for tile in row):
            if pygame.Rect(tile.rect).collidepoint(pygame.mouse.get_pos()):
                tile.setSelected(True)
                self.selected = tile
                adjacentPanels = self.findAdjacentPanels((tile.row, tile.col))
                for adjPanel in adjacentPanels:
                    adjPanel.setHighlighted(True)

    def onKeyPress(self, value):
        if self.selected != None:
            if value == 0: #delete
                self.selected.filled = None
            elif self.noting:
                self.selected.noteNumber(value)
            else:
                self.selected.fillNumber(value)


class SudokuTile():

    def __init__(self, row, col, locked):
        self.row = row
        self.col = col
        self.locked = locked

        self.noted = [[False for j in range(3)] for i in range(3)]
        self.filled = False
        self.highlighted = False

        self.width = 54
        self.surface = pygame.Surface((self.width, self.width))

        self.white = (255, 255, 255)
        self.selectedColor = (130, 162, 255)#(89, 150, 247)
        self.highlightedColor = (181, 200, 255)#(245, 217, 215)
        self.mouseOverColor = (204, 217, 255)#(201, 224, 255)

    def setSelected(self, bool):
        self.selected = bool

    def setHighlighted(self, bool):
        self.highlighted = bool

    def noteNumber(self, num):
        if self.locked: return
        self.noted[((num-1)%3)][((num-1)//3)]

    def fillNumber(self, num):
        if self.locked: return
        font = pygame.font.SysFont('Arial', 30)
        self.filled = font.render("{}".format(num), True, (0,0,0))

    def draw(self):
        if self.selected:
            self.surface.fill(self.selectedColor)
        elif self.highlighted:
            self.surface.fill(self.highlightedColor)
        elif pygame.Rect(self.rect).collidepoint(pygame.mouse.get_pos()):
            self.surface.fill(self.mouseOverColor)
        else:
            self.surface.fill(self.white)

        if self.filled != None:
            textBox = self.filled.get_rect(center=(self.width // 2, self.width // 2))
            self.surface.blit(self.filled, textBox)

        else:
            for i in range(3):
                for j in range(3):
                    if self.noted[i][j]:
                        digit = pygame.font.SysFont('Arial', 20).render("{}".format((i*3)+j), True, (0,0,0))
                        textBox = digit.get_rect(center=((i * 18) + 9, (j * 18) + 9))
                        self.surface.blit(digit, textBox)

        return self.surface
