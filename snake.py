from json.encoder import ESCAPE
import pygame
import time
import random
import sys
from pygame.locals import *

pygame.init()
windowSurface = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Snake')

#Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


basicFont = pygame.font.SysFont(None, 48)
text = basicFont.render('Snake', True, WHITE, BLACK)
textRect = text.get_rect()

#game + Food + Snake Setup
snake = [{'rect': pygame.Rect(300, 100, 20, 20), 'dir': 'up'},
            {'rect': pygame.Rect(300, 120, 20, 20), 'dir': 'up'},
            {'rect': pygame.Rect(300, 140, 20, 20), 'dir': 'up'}]

food = {'rect': pygame.Rect(100, 100, 20, 20), 'color': GREEN}
direction = 'right'
changeDirection = direction
score = 0
highScore = 0
gameOver = False
speed = 4
fpsClock = pygame.time.Clock()

#start screen
windowSurface.fill(WHITE)
textRect.center = (320, 240)
windowSurface.blit(text, textRect)
pygame.display.update()
time.sleep(2)

quitText = basicFont.render('Press Q to Quit', True, BLACK)
quitRect = quitText.get_rect()
quitRect.center = (320, 300)
windowSurface.blit(quitText, quitRect)
pygame.display.update()
time.sleep(2)

startText = basicFont.render('Press Space to Start', True, BLACK)
startRect = startText.get_rect()
startRect.center = (320, 360)
windowSurface.blit(startText, startRect)
pygame.display.update()

while True:
    random.seed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_w:
                changeDirection = 'up'
            elif event.key == K_s:
                changeDirection = 'down'
            elif event.key == K_a:
                changeDirection = 'left'
            elif event.key == K_d:
                changeDirection = 'right'
            elif event.key == ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_SPACE:
                if gameOver:
                    snake = [{'rect': pygame.Rect(300, 100, 20, 20), 'dir': 'up'},
                                {'rect': pygame.Rect(300, 120, 20, 20), 'dir': 'up'},
                                {'rect': pygame.Rect(300, 140, 20, 20), 'dir': 'up'}]
                    direction = 'right'
                    changeDirection = direction
                    score = 0
                    gameOver = False
                    speed = 4
                    food['rect'].left = random.randint(0, 31) * 20
                    food['rect'].top = random.randint(0, 23) * 20
                    fpsClock = pygame.time.Clock()

    # Collision detection
    if snake[0]['rect'].top < 0 or snake[0]['rect'].bottom > 480 or snake[0]['rect'].left < 0 or snake[0]['rect'].right > 640:
        gameOver = True
    for block in snake[1:]:
        if block['rect'].colliderect(snake[0]['rect']):
            gameOver = True

    if snake[0]['rect'].colliderect(food['rect']):
        score += 1
        if score > highScore:
            highScore = score
        speed += 1
        food['rect'].left = random.randint(0, 31) * 20
        food['rect'].top = random.randint(0, 23) * 20
    
    # Player Movement
    if not gameOver:
        if changeDirection == 'up' and not direction == 'down':
            direction = 'up'
        elif changeDirection == 'down' and not direction == 'up':
            direction = 'down'
        elif changeDirection == 'left' and not direction == 'right':
            direction = 'left'
        elif changeDirection == 'right' and not direction == 'left':
            direction = 'right'
        newHead = {'rect': pygame.Rect(snake[0]['rect'].left, snake[0]['rect'].top, 20, 20), 'dir': direction}
        if direction == 'up':
            newHead['rect'].top -= 20
        elif direction == 'down':
            newHead['rect'].top += 20
        elif direction == 'left':
            newHead['rect'].left -= 20
        elif direction == 'right':
            newHead['rect'].left += 20
        snake.insert(0, newHead)
        if not snake[0]['rect'].colliderect(food['rect']):
            del snake[-1]

    windowSurface.fill(WHITE)
    for block in snake:
        pygame.draw.rect(windowSurface, BLACK, block['rect'])
    pygame.draw.rect(windowSurface, food['color'], food['rect'])
    scoreText = basicFont.render('Score: %s' % score, True, BLACK)
    scoreRect = scoreText.get_rect()
    scoreRect.topleft = (10, 10)
    windowSurface.blit(scoreText, scoreRect)
    highScoreText = basicFont.render('High Score: %s' % highScore, True, BLACK)
    highScoreRect = highScoreText.get_rect()
    highScoreRect.topleft = (10, 40)
    windowSurface.blit(highScoreText, highScoreRect)
    pygame.display.update()
    fpsClock.tick(speed)

    # Game Over Mechanic
    if gameOver:
        gameOverText = basicFont.render('Game Over \n Press Space to Play Again', True, RED)
        gameOverRect = gameOverText.get_rect()
        gameOverRect.center = (320, 240)
        windowSurface.blit(gameOverText, gameOverRect)
        pygame.display.update()
        time.sleep(2)
        windowSurface.fill(WHITE)
        gameOverText = basicFont.render('Press Space to Play Again', True, RED)
        gameOverRect = gameOverText.get_rect()
        gameOverRect.center = (320, 240)
        windowSurface.blit(gameOverText, gameOverRect)
        pygame.display.update()
        continue