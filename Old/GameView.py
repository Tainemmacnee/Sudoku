import pygame
import AAfilledRoundedRect as rr
from Sudoku import Board

class GameView():

    def __init__(self, surface, board):
        self.surface = surface
        self.digits = []
        self.panels = []
        self.selected = None
        self.noting = False
        self.components = [coolButton(self.surface)]

        self.preRenderDigits(fontSize = 20)
        self.loadBoard(board.get())
        # self.loadBoard([[3,0,6,5,0,8,4,0,0],
        # [5,2,0,0,0,0,0,0,0],
        # [0,8,7,0,0,0,0,3,1],
        # [0,0,3,0,1,0,0,8,0],
        # [9,0,0,8,6,3,0,0,5],
        # [0,5,0,0,9,0,6,0,0],
        # [1,3,0,0,0,0,2,5,0],
        # [0,0,0,0,0,0,0,7,4],
        # [0,0,5,2,0,6,3,0,0]])
        #self.generatePanels()

    def loadBoard(self, board):
        self.panels = []
        for i in range(9):
            row = []
            for j in range(9):
                if board[i][j] == 0:
                    row.append(GridPanel(self.digits, i, j, False))
                else:
                    row.append(GridPanel(self.digits, i, j, False))
                    row[j].fillNumber(board[i][j])
                    row[j].locked = True
            self.panels.append(row)

    def preRenderDigits(self, fontSize = 20):
        font = pygame.font.SysFont('Arial', fontSize)
        for i in range(1, 10):
            self.digits.append(font.render("{}".format(i), True, (0,0,0)))

    def generatePanels(self):
        for i in range(9):
            row = []
            for j in range(9):
                row.append(GridPanel(self.digits, i, j, False))
            self.panels.append(row)

    def handleMouseUp(self):
        self.clearPanels()
        #Handle clicks on panels
        for panel in (panel for row in self.panels for panel in row):
            if pygame.Rect(panel.rect).collidepoint(pygame.mouse.get_pos()):
                panel.setSelected(True)
                self.selected = panel
                adjacentPanels = self.findAdjacentPanels(panel.getRowCol())
                for adjPanel in adjacentPanels:
                    adjPanel.setHighlighted(True)

        #Handle Clicks on other components
        for component in self.components:
            component.handleMouseUp(self)

    def findAdjacentPanels(self, pos):
        """returns list of cells that are in row, col or box of cell"""
        row, col = pos
        box_x = (row // 3)*3
        box_y = (col // 3)*3
        panels = []
        for i in range(9):
            for j in range(9):
                if i == row:
                    panels.append(self.panels[i][j])
                if j == col:
                    panels.append(self.panels[i][j])
        for i in range(box_x, box_x+3):
            for j in range(box_y, box_y+3):
                panels.append(self.panels[i][j])
        return panels


    def clearPanels(self):
        for panel in (panel for row in self.panels for panel in row):
            panel.setSelected(False)
            panel.setHighlighted(False)

    def onKeyPress(self, value):
        if self.selected != None:
            if value == 0: #delete
                self.selected.filled = None
            elif self.noting:
                self.selected.noteNumber(value)
            else:
                self.selected.fillNumber(value)

    def handleMouseDown(self):
        for component in self.components:
            component.handleMouseDown()

    def draw(self): #20, 70, 140
        self.surface.fill((255,255,255))
        pygame.draw.rect(self.surface, (20, 70, 140), (0,0,500, 500))
        for component in self.components:
            component.draw()
        for panel in (panel for row in self.panels for panel in row):
            pos = panel.getPos()
            self.surface.blit(panel.draw(), pos)

class GridPanel():
    """panel for each cell in sudoku"""
    def __init__(self, digits, row, col, locked):
        self.row = row
        self.col = col
        self.width = 54
        self.noted = [[False for j in range(3)] for i in range(3)]
        self.filled = None
        self.selected = False
        self.highlighted = False
        self.surface = pygame.Surface((self.width, self.width))
        self.digits = digits
        self.locked = locked

        spacingX = 2 + self.row + (self.row // 3)
        spacingY = 2 + self.col + (self.col // 3)
        self.xPos = (self.row * self.width) + spacingX
        self.yPos = (self.col * self.width) + spacingY

        self.rect = (self.xPos, self.yPos, self.width, self.width)
        self.white = (255, 255, 255)
        self.selectedColor = (130, 162, 255)#(89, 150, 247)
        self.highlightedColor = (181, 200, 255)#(245, 217, 215)
        self.mouseOverColor = (204, 217, 255)#(201, 224, 255)
        """
        font = pygame.font.SysFont('Arial', 30)
        self.filled = font.render("1", True, (0,0,0))
        """

    def setSelected(self, value):
        self.selected = value

    def setHighlighted(self, value):
        self.highlighted = value

    def getPos(self):
        """Returns the position of this panel on the game window"""
        return (self.xPos, self.yPos)

    def getRowCol(self):
        return (self.row, self.col)

    def noteNumber(self, num):
        if not self.locked:
            x = (num-1) % 3
            y = (num-1) // 3
            self.noted[x][y] = True

    def fillNumber(self, num):
        if not self.locked:
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
            #pygame.draw.rect(self.surface, self.white, self.surface.get_rect())

        if self.filled != None:
            textMidX = (self.width // 2)
            textMidY = (self.width // 2)
            textBox = self.filled.get_rect(center=(textMidX, textMidY))
            self.surface.blit(self.filled, textBox)

        else:
            for i in range(3):
                for j in range(3):
                    if self.noted[i][j]:
                        textMidX = (i * 18) + 9
                        textMidY = (j * 18) + 9
                        textBox = self.digits[(i*3)+j].get_rect(center=(textMidX, textMidY))
                        self.surface.blit(self.digits[(j*3)+i], textBox)

        return self.surface

class coolButton():

    def __init__(self, surface):
        self.color = (71, 151, 255)
        self.textColor = (0 ,0 ,0)
        self.xPos = 50
        self.yPos = 520
        self.width = 400
        self.height = 25
        self.surface = surface
        self.down = False
        self.font = pygame.font.SysFont('Arial', 18)
        self.text = self.font.render("Notes Off", True, self.textColor)

    def handleMouseUp(self, parent):
        if pygame.Rect(self.getRect()).collidepoint(pygame.mouse.get_pos()):
            self.down = False
            if parent.noting:
                parent.noting = False
                self.text = self.font.render("Notes Off", True, self.textColor)
            else:
                parent.noting = True
                self.text = self.font.render("Notes On", True, self.textColor)

    def handleMouseDown(self):
        if pygame.Rect(self.getRect()).collidepoint(pygame.mouse.get_pos()):
            self.down = True

    def getPos(self):
        return (self.xPos, self.yPos)

    def getRect(self):
        return (self.xPos, self.yPos, self.width, self.height)

    def getShadowRect(self):
        return (self.xPos +1, self.yPos +1, self.width, self.height)

    def draw(self):
        if self.down:
            rr.AAfilledRoundedRect(self.surface, self.getShadowRect(), self.color, 0.5)
        else:
            #draw shadow.
            rr.AAfilledRoundedRect(self.surface, self.getShadowRect(), (0,0,0), 0.5)
            #Draw Box.
            rr.AAfilledRoundedRect(self.surface, self.getRect(), self.color, 0.5)

        textMidX = 50 + (400//2)
        textMidY = 521 + (25//2)
        textBox = self.text.get_rect(center=(textMidX, textMidY))
        self.surface.blit(self.text, textBox)
