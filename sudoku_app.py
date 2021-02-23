import pygame
from pygame.locals import *
from intro_view import IntroView
from game_over_view import GameOverView

class SudokuApp:
    def __init__(self):
        self._running = True
        self.surface = None
        self.size = self.width, self.height = 500, 700
        self.keys = {
            K_1 : 1, K_2 : 2, K_3 : 3, K_4 : 4,
            K_5 : 5, K_6 : 6, K_7 : 7, K_8 : 8, K_9 : 9, K_DELETE: 0}


    def on_init(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sudoku!')
        self.display = IntroView(self)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            self.display.handle_mouse_up()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.display.handle_mouse_down()
        if event.type == pygame.KEYUP:
            if event.key in self.keys:
                self.display.handle_key_press(self.keys[event.key])

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            self.display.draw()
            self.surface.blit(self.display.surface, (0,0))
            for event in pygame.event.get():
                self.on_event(event)

            pygame.display.update()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = SudokuApp()
    theApp.on_execute()
