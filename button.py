import pygame

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

    def handle_mouse_up(self):
        self.down = False
        if pygame.Rect(self.getRect()).collidepoint(pygame.mouse.get_pos()):
            self.function()

    def handle_mouse_down(self):
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

class ToggleShadowButton(ShadowButton):

    def __init__(self, x, y, width, height, color, surface, text, function):
        ShadowButton.__init__(self, x, y, width, height, color, surface, text, function)
        self.toggle = False
        self.TOGGLE_COLOR = (252, 81, 66)

    def handle_mouse_up(self):
        self.down = False
        if pygame.Rect(self.getRect()).collidepoint(pygame.mouse.get_pos()):
            self.toggle = not self.toggle
            self.function()

    def get_toggle_rect(self):
        """Rectangle for the position of the toggle section of the button"""
        if self.down:
            return ((2*self.width/3)+self.x + 2, self.y + 2, self.width/3, self.height)
        else:
            return ((2*self.width/3)+self.x, self.y, self.width/3, self.height)

    def get_toggle_text_rect(self):
        """Rectangle for the position of the text toggle section of the button"""
        if self.down:
            return (self.x + 2, self.y + 2, 2*self.width/3, self.height)
        else:
            return (self.x, self.y, 2*self.width/3, self.height)

    def draw(self):
        if self.down:
            pygame.draw.rect(self.surface, self.defaultColor, self.get_toggle_text_rect())
            pygame.draw.rect(self.surface, self.TOGGLE_COLOR, self.get_toggle_rect())
        else:
            #draw shadow.
            pygame.draw.rect(self.surface, (0,0,0), self.getShadowRect())
            #Draw Box.
            pygame.draw.rect(self.surface, self.defaultColor, self.get_toggle_text_rect())
            pygame.draw.rect(self.surface, self.TOGGLE_COLOR, self.get_toggle_rect())
        toggle_render = None
        if self.toggle:
            toggle_render = pygame.font.SysFont('Arial', 18).render("ON", True, self.textColor)
        else:
            toggle_render = pygame.font.SysFont('Arial', 18).render("OFF", True, self.textColor)

        textMidX = self.x + ((2*self.width/3)//2)
        textMidY = self.y + (self.height//2)
        toggle_mid_x = self.x + (2*self.width/3) + ((self.width/3)//2) #Wrong?
        textBox = self.render.get_rect(center=(textMidX, textMidY))
        toggle_box = toggle_render.get_rect(center=(toggle_mid_x, textMidY))
        self.surface.blit(self.render, textBox)
        self.surface.blit(toggle_render, toggle_box)
