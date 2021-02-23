import pygame
import intro_view
from button import *

class GameOverView():

    def __init__(self, app):
        self.app = app
        self.surface = pygame.Surface((app.width, app.height))

        quit_btn = ShadowButton(25, 360, 450, 50, (71, 151, 255), self.surface, "Quit", self.quit)
        main_menu_btn = ShadowButton(25, 280, 450, 50, (71, 151, 255), self.surface, "Main Menu", self.menu)

        self.btns = [quit_btn, main_menu_btn]

    def quit(self):
        self.app._running = False

    def menu(self):
        self.app.display = intro_view.IntroView(self.app)

    def draw(self):
        self.surface.fill((255,255,255))

        font = pygame.font.SysFont('Arial', 50)
        text = font.render('Sudoku Complete!', True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (self.surface.get_width() // 2, 200)
        self.surface.blit(text, textRect)

        for btn in self.btns:
            btn.draw()

    def handle_mouse_down(self):
        for btn in self.btns:
            btn.handle_mouse_down()

    def handle_mouse_up(self):
        for btn in self.btns:
            btn.handle_mouse_up()

    def handle_key_press(self, key):
        pass
