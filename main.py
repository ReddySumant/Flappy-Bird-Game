import random #for generating randomness
import sys #To exit the game
import pygame
from pygame.locals import *



# Global variables for the game
FPS = 32 #Frames per second
SCREENWIDTH = 289
SCREENHEIGHT = 511
PIPEGAPSIZE = 100
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.86
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'media/sprites/bird.png'
BACKGROUND = 'media/sprites/background.png'
PIPE = 'media/sprites/pipe.png'


def welcomeScreen():
    """
    shows welcome image on screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross butten to close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if user preses space or up key, then start the game
            elif event.type==KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()  # To blit the game screen
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/5)
    basex = 0 

    # Create 2 pipes for blitting on screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']}
    ]
    #list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[1]['y']}
    ]

    playerVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playreAccY = 1

    PlayerflapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true when bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = PlayerflapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
    

        # Check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos + 4:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
        
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # It will check if function is crashed
        if crashTest:
            return

        if playerVelY <    playerMaxVelY  and not playerFlapped:
            playerVelY +=playreAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY , GROUNDY - playery - playerHeight)

        # Move pipes to left
        for upperPipe, lowerpipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += playerVelX
            lowerpipe['x'] += playerVelX

        # add new pipe when first pipe is about to touch left of screen
        if len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if len(upperPipes) > 0 and upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)


        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe, lowerpipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'],lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0

        for digit in myDigits:
            width+= GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset,SCREENHEIGHT*0.1))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY-25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    
    
   

            

def getRandomPipe():
    """
    Generates positions of two pipes (one bottom straight and one top rotated) for blitting on the screen
    """
    offset = random.randrange(0, int(GROUNDY * 0.6 - PIPEGAPSIZE))
    offset += int(GROUNDY *0.2)
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return[
        {'x': pipeX, 'y': offset - pipeHeight},
        {'x': pipeX, 'y': offset + PIPEGAPSIZE}
    ]



if __name__ == "__main__":
    #game starts here
    pygame.init() # initialising pygame module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('media/sprites/0.png').convert_alpha(),
        pygame.image.load('media/sprites/1.png').convert_alpha(),
        pygame.image.load('media/sprites/2.png').convert_alpha(),
        pygame.image.load('media/sprites/3.png').convert_alpha(),
        pygame.image.load('media/sprites/4.png').convert_alpha(),
        pygame.image.load('media/sprites/5.png').convert_alpha(),
        pygame.image.load('media/sprites/6.png').convert_alpha(),
        pygame.image.load('media/sprites/7.png').convert_alpha(),
        pygame.image.load('media/sprites/8.png').convert_alpha(),
        pygame.image.load('media/sprites/9.png').convert_alpha()  
    )

    GAME_SPRITES['message'] = pygame.image.load('media/sprites/start.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('media/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )

    # Game Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('media/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('media/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('media/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('media/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('media/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() #shows welcome screen to user until he press a button
        mainGame() #This is main game fuction