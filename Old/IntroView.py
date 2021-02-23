import pygame
from GameView import *
import AAfilledRoundedRect as rr
import Generator



class IntroView():

    def __init__(self, surface, app):
        self.surface = surface
        self.background = pygame.image.load("Background.png")
        self.backgroundPos = 0
        self.wait = 0
        self.app = app

        self.chooseDif = False

        self.easyReduceSteps = 5
        self.medReduceSteps = 55
        self.hardReduceSteps = 70

        newGameBtn = ShadowButton(120, 200, 250, 50, (71, 151, 255), self.surface, "New Game", self.newGame)

        Easy = ShadowButton(120, 200, 250, 50, (71, 151, 255), self.surface, "Easy", self.newEasyGame)
        Med = ShadowButton(120, 280, 250, 50, (71, 151, 255), self.surface, "Medium", self.newMedGame)
        Hard = ShadowButton(120, 360, 250, 50, (71, 151, 255), self.surface, "Hard", self.newHardGame)
        Back = ShadowButton(120, 440, 250, 50, (71, 151, 255), self.surface, "Back", self.back)

        quitBtn = ShadowButton(120, 280, 250, 50, (71, 151, 255), self.surface, "Quit", self.quit)
        self.mainComponents = [newGameBtn, quitBtn]
        self.diffSelectComponents = [Easy, Med, Hard, Back]
        self.components = [TitleLabel(self.surface)]

    def newGame(self):
        self.chooseDif = True

    def quit(self):
        self.app._running = False

    def generateBoard(self, steps):
        board = Board([[ 0 for j in range(9)] for i in range(9)])
        Generator.generate_complete_sudoku(board)
        return Generator.random_reduce_sudoku(board, max_depth=steps)

    def newEasyGame(self):
        board = self.generateBoard(self.easyReduceSteps)
        self.app.display = GameView(self.surface, board)

    def newMedGame(self):
        board = self.generateBoard(self.medReduceSteps)
        self.app.display = GameView(self.surface, board)

    def newHardGame(self):
        board = self.generateBoard(self.hardReduceSteps)
        self.app.display = GameView(self.surface, board)

    def back(self):
        self.chooseDif = False

    def draw(self):
        self.drawBackground()
        if self.chooseDif:
            for component in self.diffSelectComponents:
                component.draw()
        else:
            for component in self.mainComponents:
                component.draw()
        for component in self.components:
            component.draw()

    def handleMouseDown(self):
        if self.chooseDif:
            for component in self.diffSelectComponents:
                if isinstance(component, Button):
                    component.handleMouseDown()
        else:
            for component in self.mainComponents:
                if isinstance(component, Button):
                    component.handleMouseDown()


    def handleMouseUp(self):
        if self.chooseDif:
            for component in self.diffSelectComponents:
                if isinstance(component, Button):
                    component.handleMouseUp()
        else:
            for component in self.mainComponents:
                if isinstance(component, Button):
                    component.handleMouseUp()

    def drawBackground(self):
        if self.wait == 20:
            self.wait = 0
            self.backgroundPos += 1
            if self.backgroundPos == 500:
                self.backgroundPos = 0
        self.wait += 1

        self.surface.blit(self.background, (self.backgroundPos, 0, 500, 500))
        self.surface.blit(self.background, (self.backgroundPos, 498, 500, 500))
        self.surface.blit(self.background, (self.backgroundPos-498, 0, 500, 500))
        self.surface.blit(self.background, (self.backgroundPos-498, 498, 500, 500))

        pygame.draw.rect(self.surface, (0,0,0), (99, 49, 302, 502))
        pygame.draw.rect(self.surface, (255,255,255), (100, 50, 300, 500))



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


class Button():

    def __init__(self, x, y, width, height, color, surface, text, function):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.surface = surface
        self.text = text
        self.function = function
        self.defaultColor = color
        self.mouseOverColor = color
        self.textColor = (0,0,0)

        font = pygame.font.SysFont('Arial', 18)
        self.render = font.render(text, True, self.textColor)

    def setMouseOverColor(self, color):
        self.mouseOverColor = color

    def mouseUp(self):
        if pygame.Rect(self.getRect()).collidepoint(pygame.mouse.get_pos()):
            self.function()

    def mouseDown(self):
        pass

    def draw(self):
        if pygame.Rect(self.getRect()).collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.surface, self.mouseOverColor, self.getRect())
        else:
            pygame.draw.rect(self.surface, self.defaultColor, self.getRect())

        textMidX = self.x + (self.width//2)
        textMidY = self.y + (self.height//2)
        textBox = self.render.get_rect(center=(textMidX, textMidY))
        self.surface.blit(self.render, textBox)

    def getRect(self):
        return (self.x, self.y, self.width, self.height)

class ShadowButton(Button):

    def __init__(self, x, y, width, height, color, surface, text, function):
        Button.__init__(self, x, y, width, height, color, surface, text, function)
        self.down = False

    def handleMouseUp(self):
        self.down = False
        if pygame.Rect(self.getRect()).collidepoint(pygame.mouse.get_pos()):
            self.function()

    def handleMouseDown(self):
        if pygame.Rect(self.getRect()).collidepoint(pygame.mouse.get_pos()):
            self.down = True

    def draw(self):
        if self.down:
            pygame.draw.rect(self.surface, self.defaultColor, self.getShadowRect())
        else:
            #draw shadow.
            pygame.draw.rect(self.surface, (0,0,0), self.getShadowRect())
            #Draw Box.
            pygame.draw.rect(self.surface, self.defaultColor, self.getRect())

        textMidX = self.x + (self.width//2)
        textMidY = self.y + (self.height//2)
        textBox = self.render.get_rect(center=(textMidX, textMidY))
        self.surface.blit(self.render, textBox)

    def getShadowRect(self):
        return (self.x +2, self.y +2, self.width, self.height)
