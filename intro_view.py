from sudoku_generator import generate_sudoku
import pygame
from button import *
from game_view import *

class IntroView():

    def __init__(self, app):

        self.surface = pygame.Surface((app.width, app.height))
        self.background = pygame.image.load("Background.png")
        self.background_pos = 0
        self.wait = 0
        self.app = app
        self.choose_dif = False

        self.EASY_REDUCE_STEPS = 1 #Testing
        self.MED_REDUCE_STEPS = 45
        self.HARD_REDUCE_STEPS = 70

        new_game_btn = ShadowButton(120, 200, 250, 50, (71, 151, 255), self.surface, "New Game", self.new_game)

        easy_btn = ShadowButton(120, 200, 250, 50, (71, 151, 255), self.surface, "Easy", self.new_easy_game)
        med_btn = ShadowButton(120, 280, 250, 50, (71, 151, 255), self.surface, "Medium", self.new_med_game)
        hard_btn = ShadowButton(120, 360, 250, 50, (71, 151, 255), self.surface, "Hard", self.new_hard_game)
        back_btn = ShadowButton(120, 440, 250, 50, (71, 151, 255), self.surface, "Back", self.back)

        quit_btn = ShadowButton(120, 280, 250, 50, (71, 151, 255), self.surface, "Quit", self.quit)

        self.diff_select_btns = [easy_btn, med_btn, hard_btn, back_btn]
        self.main_components = [TitleLabel(self.surface)]
        self.main_btns = [new_game_btn, quit_btn]

        #Button Functions
    def new_game(self):
        self.choose_dif = True

    def quit(self):
        self.app._running = False

    def new_easy_game(self):
        sudoku = generate_sudoku(self.EASY_REDUCE_STEPS)
        self.app.display = GameView(self.app, sudoku)

    def new_med_game(self):
        sudoku = generate_sudoku(self.MED_REDUCE_STEPS)
        self.app.display = GameView(self.app, sudoku)

    def new_hard_game(self):
        sudoku = generate_sudoku(self.HARD_REDUCE_STEPS)
        self.app.display = GameView(self.app, sudoku)

    def back(self):
        self.choose_dif = False

    #Button helper function
    def generate_board(self, steps):
        return

    #Drawing functions
    def draw(self):
        self.draw_background()
        if self.choose_dif:
            for component in self.diff_select_btns + self.main_components:
                component.draw()
        else:
            for component in self.main_btns + self.main_components:
                component.draw()

    def draw_background(self):
        if self.wait == 20:
            self.wait = 0
            self.background_pos += 1
            if self.background_pos == 500:
                self.background_pos = 0
        self.wait += 1

        self.surface.blit(self.background, (self.background_pos, 0, 500, 500))
        self.surface.blit(self.background, (self.background_pos, 498, 500, 500))
        self.surface.blit(self.background, (self.background_pos-498, 0, 500, 500))
        self.surface.blit(self.background, (self.background_pos-498, 498, 500, 500))

        pygame.draw.rect(self.surface, (0,0,0), (99, 49, 302, 502))
        pygame.draw.rect(self.surface, (255,255,255), (100, 50, 300, 500))

    def handle_mouse_down(self):
        if self.choose_dif:
            for btn in self.diff_select_btns:
                    btn.handle_mouse_down()
        else:
            for btn in self.main_btns:
                    btn.handle_mouse_down()

    def handle_mouse_up(self):
        if self.choose_dif:
            for btn in self.diff_select_btns:
                    btn.handle_mouse_up()
        else:
            for btn in self.main_btns:
                    btn.handle_mouse_up()

    def handle_key_press(self, key):
        pass

class TitleLabel():

    def __init__(self, surface):
        self.surface = surface

        self.x = surface.get_width() // 2
        self.y = 100
        self.fontSize = 50
        font = pygame.font.SysFont('Arial', self.fontSize)
        self.text = font.render('Sudoku', True, (0,0,0))

    def draw(self):
        textRect = self.text.get_rect()
        textRect.center = (self.x, self.y)
        self.surface.blit(self.text, textRect)
