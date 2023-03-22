''' This module contains all game widgets '''
import pygame
from utils import WHITE, ORANGE, RED

class Label:
    ''' Class for a pygame label widget '''
    def __init__(self, text, position, **kwargs):
        self.text = text
        self.position = position
        self.center = kwargs.get('center', False)
        self.fg = kwargs.get('fg', RED)
        self.bg = kwargs.get('bg', ORANGE)
        self.font = pygame.font.SysFont(
            *kwargs.get('font', ('Arial', 50, True))
            )
        self.pad = kwargs.get('pad', 0)
        self.text_render = None

    def draw(self, screen):
        self.text_render = self.font.render(
            self.text.center(len(self.text)+ self.pad),
            1,
            self.fg,
            self.bg
            )
        rect = self.text_render.get_rect()
        #Checking if given position is the position of the center of button
        if self.center:
            rect.center = self.position
        else:
            rect.topleft = self.position
        screen.blit(self.text_render, rect.topleft)
        