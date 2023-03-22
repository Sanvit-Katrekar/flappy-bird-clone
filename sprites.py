import pygame
import math
import random
from utils import *

class Bird(pygame.sprite.Sprite):
    ''' Class for the game birdie '''
    def __init__(self, x, y, width, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.img = pygame.image.load(resourcePath('bird.png')).convert_alpha()
        self.originalImg = resizeImg(self.img, width)
        self.img = self.originalImg
        self.rect = self.img.get_rect(topleft=(self.x+5, self.y)) #+5 -> collision correction
        self.gravity = 0.2
        self.isJump = False
        self.jumpcount = 10
        self.start = False
        self.flycount = 0
        self.angle = 0
        self.maxPipes = 10
        self.score = 0
        self.xVel = speed
        self.yVel = self.gravity

    def update(self):
        if self.start:
            self.yVel += self.gravity
            self.y += self.yVel + 0.5 * self.gravity
            self.rect.y = self.y
            self.jump()
            #Bird rotation
            self.angle = math.atan2(-self.yVel, self.xVel) * (180/math.pi) / 2.5
            if self.jumpcount <= 4:
                self.angle = 0
            self.img = pygame.transform.rotate(self.originalImg, self.angle)
            self.rect.y += 10 #Correcting bird's collision rectangle

        else:
            self.y += math.sin(self.flycount)
            self.flycount += math.pi/12
            
    def jump(self):
        if self.isJump:
            self.yVel = -(self.jumpcount**2)//7
            self.rect.y = self.y
            self.jumpcount -= 1
            if self.jumpcount < 0:
                self.jumpcount = 10
                self.isJump = False

    def isCollided(self, spriteGroup):
        return pygame.sprite.spritecollide(self, spriteGroup, False)

class Pipe(pygame.sprite.Sprite):
    ''' Class for the game pipes '''
    def __init__(self, x, groundLevel, groundSpeed):
        super().__init__()
        self.width = 70
        self.isScored = False
        self.img = resizeImg(
            pygame.image.load(resourcePath('pipe.png')).convert_alpha(),
            self.width
            )
        self.x = x + random.randrange(self.width*4, 3000, self.width*4+20)
        self.speed = groundSpeed

        self.inverted = random.randint(0, 1)

        if self.inverted:
            self.img = pygame.transform.rotate(self.img, 180)
            self.y = -(random.randrange(groundLevel - groundLevel//8)) - self.width//2 
        else:
            self.y = groundLevel - random.randrange(groundLevel - groundLevel//6)##
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x
        if self.x + self.width < 0:
            self.kill()
