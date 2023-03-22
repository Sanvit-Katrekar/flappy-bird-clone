''' This module contains common classes and functions used in the game '''
import os
import sys
import pygame

#Defining some colours
WHITE = (255, 255, 255)
ORANGE = (255, 120, 0)
RED = (255, 0, 0)

def resourcePath(relativePath, subdir='', path=False):
    ''' Returns the path to game resource '''
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = 'Images'
        basePath = os.path.join(basePath, subdir)
    if path:
        return basePath
    return os.path.join(basePath, relativePath)

def resizeImg(img, width=None, height=None):
    sizeRatio = img.get_width()/img.get_height()
    if width and height:
        size = (width, height)
    elif width:
        size = (width, int(width/sizeRatio))
    elif height:
        size = (int(height*sizeRatio), height)
    else:
        size = (img.get_width(), img.get_height())
    return pygame.transform.scale(img, size)

class ScrollingBackground:
    ''' Class for defining a background that gives a scrolling effect '''
    def __init__(self, imgName, speed=1, width=None, height=None):
        self.x = self.y = 0
        self.speed = speed
        self.img = resizeImg(
            pygame.image.load(resourcePath(imgName)).convert(),
            width,
            height
            )
        self.width = width or self.img.get_width()
        self.relX = 0

    def update(self):
        ''' Continously updates the image position within the screen frame '''
        self.relX = self.x % self.width
        self.x -= self.speed
    