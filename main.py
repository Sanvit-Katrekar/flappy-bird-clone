import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from utils import *
import pygame
from widgets import Label
from sprites import Bird, Pipe

pygame.init()

#Defining game variables
WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird!')
icon = pygame.image.load(resourcePath('icon.png'))
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

FONT1 = ('SuperScript', 45, True)
FONT2 = ('Arial', 50, True)
titleLabel = Label(
    'Flappy Bird!',
    (WIDTH//2, FONT2[1]),
    fg=WHITE,
    center=1,
    pad=4
    )
playLabel = Label(
    'Press SPACE to play!',
    (WIDTH//2, HEIGHT//4 + 20),
    fg=WHITE,
    bg=None,
    center=1
    )
background = ScrollingBackground('bg.png', speed=0.5)
#Game play again loop
run = True
#Events that will make the bird jump
jumpEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]

def redrawWindow(window):
    ''' Redraws the game window '''
    window.blit(background.img, (int(background.relX - background.width), 0))
    if background.relX < WIDTH:
        window.blit(background.img, (int(background.relX), 0))
    #pygame.draw.rect(screen, (255, 0, 0), bird.rect)
    window.blit(bird.img, (int(bird.x), int(bird.y)))
    for pipe in pipes:
        window.blit(pipe.img, (pipe.x, pipe.y))
        if pipe.rect.right < bird.x and not pipe.isScored:
            pipe.isScored = True
            bird.score += 1
        #pygame.draw.rect(screen, RED, pipe.rect)
    window.blit(floor.img, (floor.relX - floor.width, floor.y))
    if floor.relX < WIDTH:
        window.blit(floor.img, (floor.relX, floor.y))
    if not bird.start:
        titleLabel.draw(window)
        playLabel.draw(window)
    else:
        score = Label(
            f'Score: {bird.score}',
            (WIDTH//2, FONT2[1]),
            font=FONT1,
            bg=None,
            fg=WHITE,
            center=1
            )
        score.draw(window)
    all_sprites.update()
    floor.update()
    background.update()
    pygame.display.update()

def gameOver(window):
    ''' Checks if the game is over '''
    global run
    if not run:
        return True
    if bird.rect.bottom > floor.y or bird.isCollided(pipes):
        gameover = Label(
            'Game Over!',
            (WIDTH//2, HEIGHT//3),
            font=FONT2,
            fg=WHITE,
            center=1,
            pad=6
            )
        gameover.draw(window)

        pygame.display.update()
        pygame.time.delay(1000)
        return True

while run:
    bird = Bird(200, 200, 60, background.speed)
    floor = ScrollingBackground('flappyBirdFloor.png', 2, width=WIDTH)
    floor.y = HEIGHT - HEIGHT//10
    pipes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bird)
    #Main game loop
    while not gameOver(screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type in jumpEvents:
                if event.type == jumpEvents[0] or event.key == pygame.K_SPACE:
                    bird.isJump = bird.start = True
        #Loop to add pipes      
        while len(pipes) < bird.maxPipes and bird.start:
            #Setting x position to end of window
            while True:
                pipe = Pipe(bird.x+WIDTH, floor.y, floor.speed)
                if all(p.x != pipe.x for p in pipes):
                    break
            pipes.add(pipe)
            all_sprites.add(pipe)
        if bird.y < 0:
            bird.y = 0
        redrawWindow(screen)
        clock.tick(60)

pygame.quit()
