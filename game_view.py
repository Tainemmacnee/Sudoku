import pygame
from button import *
import intro_view
import game_over_view

class GameView():

    def __init__(self, app, sudoku):

        self.surface = pygame.Surface((app.width, app.height))
        self.app = app
        self.sudoku = sudoku

        self.notations = False
        self.selected = None

        self.notations_btn = ToggleShadowButton(25, 505, 450, 50, (71, 151, 255), self.surface, "Notations", self.notation_toggle)
        self.main_menu_btn = ShadowButton(25, 565, 450, 50, (71, 151, 255), self.surface, "Main Menu", self.menu)
        self.quit_btn = ShadowButton(25, 625, 450, 50, (71, 151, 255), self.surface, "Quit", self.quit)

        self.panels = []
        self.btns = [self.notations_btn, self.main_menu_btn, self.quit_btn]

        self.load_sudoku()

    #Button functions
    def notation_toggle(self):
        self.notations = not self.notations

    def quit(self):
        self.app._running = False

    def menu(self):
        self.app.display = intro_view.IntroView(self.app)

    def load_sudoku(self):
        board = self.sudoku.board.grid
        for i in range(9):
            row = []
            for j in range(9):
                row.append(GameTile(i, j, self.sudoku.solution.grid[i][j]))
                if board[i][j] != 0:
                    row[j].fill_number(board[i][j])
                    row[j].locked = True
            self.panels.append(row)

    def clear_selection(self):
        for panel in (panel for row in self.panels for panel in row):
            panel.selected = False
            panel.highlighted = False

    def highlight_adjacnt_panels(self, row, col):
        box_x = (row // 3)*3
        box_y = (col // 3)*3
        for i in range(9):
            for j in range(9):
                if i == row or j == col:
                    self.panels[i][j].highlighted = True
        for i in range(box_x, box_x+3):
            for j in range(box_y, box_y+3):
                self.panels[i][j].highlighted = True

    def handle_mouse_up(self):
        for btn in self.btns:
            btn.handle_mouse_up()

        self.clear_selection()
        for panel in (panel for row in self.panels for panel in row):
            if pygame.Rect(panel.get_rect()).collidepoint(pygame.mouse.get_pos()):
                panel.selected = True
                self.selected = panel
                self.highlight_adjacnt_panels(panel.row, panel.col)

    def handle_mouse_down(self):
        for btn in self.btns:
            btn.handle_mouse_down()

    def handle_key_press(self, key):
        if self.selected != None:
            if key == 0: #delete key
                self.selected.filled = None
                self.sudoku.board.grid[self.selected.row][self.selected.col] = 0
            elif self.notations:
                self.selected.note_number(key)
            else:
                self.selected.fill_number(key)
                self.sudoku.board.grid[self.selected.row][self.selected.col] = key

                #Win condition met
                if self.sudoku.board.grid == self.sudoku.solution.grid:
                    self.app.display = game_over_view.GameOverView(self.app)

    def draw(self):
        self.surface.fill((255,255,255))
        pygame.draw.rect(self.surface, (20, 70, 140), (0,0,500, 500))
        for btn in self.btns:
            btn.draw()
        for panel in (panel for row in self.panels for panel in row):
            rect = panel.get_rect()
            panel.draw()
            self.surface.blit(panel.surface, (rect[0], rect[1]))

class GameTile():

    def __init__(self, row, col, correct_value):
        self.WIDTH = 54
        self.WHITE = (255, 255, 255)
        self.BLACK = (0,0,0)
        self.SELECTED_COLOR = (130, 162, 255)#(89, 150, 247)
        self.HIGHLIGHTED_COLOR = (181, 200, 255)#(245, 217, 215)
        self.MOUSE_OVER_COLOR = (204, 217, 255)#(201, 224, 255)
        self.WRONG_VALUE_COLOR = (252, 28, 3)

        self.surface = pygame.Surface((self.WIDTH, self.WIDTH))
        self.row = row
        self.col = col
        self.correct_value = correct_value

        self.selected = False
        self.highlighted = False
        self.filled = None
        self.noted = [[False for j in range(3)] for i in range(3)]
        self.locked = False



    def get_rect(self):
        spacing_x = 2 + self.row + (self.row // 3)
        spacing_y = 2 + self.col + (self.col // 3)
        xPos = (self.row * self.WIDTH) + spacing_x
        yPos = (self.col * self.WIDTH) + spacing_y

        return (yPos, xPos, self.WIDTH, self.WIDTH)

    def note_number(self, num):
        if not self.locked:
            x = (num) % 3
            y = (num) // 3
            self.noted[x][y] = not self.noted[x][y]

    def fill_number(self, num):
        if not self.locked:
            font = pygame.font.SysFont('Arial', 30)
            if num == self.correct_value:
                self.filled = font.render("{}".format(num), True, self.BLACK)
            else:
                self.filled = font.render("{}".format(num), True, self.WRONG_VALUE_COLOR)

    def draw(self):
        if self.selected:
            self.surface.fill(self.SELECTED_COLOR)
        elif self.highlighted:
            self.surface.fill(self.HIGHLIGHTED_COLOR)
        elif pygame.Rect(self.get_rect()).collidepoint(pygame.mouse.get_pos()):
            self.surface.fill(self.MOUSE_OVER_COLOR)
        else:
            self.surface.fill(self.WHITE)

        if self.filled != None:
            text_mid = (self.WIDTH // 2)
            self.surface.blit(self.filled, self.filled.get_rect(center=(text_mid, text_mid)))
        else:
            for i in range(3):
                for j in range(3):
                    if self.noted[i][j]:
                        font = pygame.font.SysFont('Arial', 20)
                        number = font.render("{}".format((j*3)+i), True, self.BLACK)
                        text_mid_x = (i * 18) + 9
                        text_mid_y = (j * 18) + 9
                        text_box = number.get_rect(center=(text_mid_x, text_mid_y))
                        self.surface.blit(number, text_box)
