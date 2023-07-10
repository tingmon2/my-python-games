import sys
import math
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE, KEYUP, K_DOWN, Rect

pygame.init()
pygame.key.set_repeat(4)
SURFACE = pygame.display.set_mode((600, 800))
FPSCLOCK = pygame.time.Clock()

class Block:
    def __init__(self, color, rect, speed = 0):
        self.color = color
        self.rect =  rect
        self.speed = speed
        self.direction = random.randint(-45, 45) + 270

    def move_ball(self):
        self.rect.centerx += math.cos(math.radians(self.direction)) \
                                * self.speed
        self.rect.centery -= math.sin(math.radians(self.direction)) \
                                * self.speed

    def draw(self):
        if self.speed == 0:
            pygame.draw.rect(SURFACE, self.color, self.rect)
        else:
            pygame.draw.ellipse(SURFACE, self.color, self.rect)

def tick(positionfont):
    global BLOCKS
    global PAUSE
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                PADDLE.rect.centerx -= 10
            elif event.key == K_RIGHT:
                PADDLE.rect.centerx += 10
                
    
    if BALL.rect.centery < 1000:
        BALL.move_ball()

    initial_len = len(BLOCKS)
    BLOCKS = [x for x in BLOCKS if not x.rect.colliderect(BALL.rect)]
    if len(BLOCKS) != initial_len:
        BALL.direction *= -1
    if PADDLE.rect.colliderect(BALL.rect):
        BALL.direction = 90 + (PADDLE.rect.centerx - BALL.rect.centerx) \
                            / PADDLE.rect.width * 80

    if BALL.rect.centerx < 0 or BALL.rect.centerx > 600:
        BALL.direction = 180 - BALL.direction
    if BALL.rect.midtop[1] < 0 :
        BALL.direction *= -1 # changed
        BALL.speed = 15

    ball_message = positionfont.render("ball x-coordinate: {}, {}" \
        .format(BALL.rect.midleft[0], BALL.rect.midright[0]), True, (234, 112, 90))

    return ball_message

BLOCKS = [] # list
PADDLE = Block((242, 142, 50), Rect(300, 700, 100, 30)) # object in Block class
BALL = Block((111, 222, 123), Rect(300, 400, 20, 20), 10) # object in Block class
PAUSE = False

def main():
    global PAUSE
    myfont = pygame.font.SysFont(None, 80)
    positionfont = pygame.font.SysFont(None, 20)
    clear_message = myfont.render("CLEAR!!", True, (231, 21, 111))
    over_message = myfont.render("GAME OVER!!", True, (123, 241, 40))
    fps = 30
    colors = [(255, 0, 0), (255, 165, 0), 
                (242, 242, 0), (0, 128, 0), (128, 0, 128), (0, 0, 250)]

    for ypos, color in enumerate(colors,start=0):
        for xpos in range(5):
            BLOCKS.append(Block(color, Rect(xpos*100+60, ypos*50+40, 80, 30)))

    while not PAUSE:
        ball_message = tick(positionfont)

        SURFACE.fill((0, 0, 0))
        BALL.draw()
        PADDLE.draw()
        for block in BLOCKS:
            block.draw()

        if len(BLOCKS) == 0:
            SURFACE.blit(clear_message, (200, 400))
        if len(BLOCKS) > 0 and BALL.rect.centery > 800:
            SURFACE.blit(over_message, (150, 400))
        else:
            SURFACE.blit(ball_message, (200, 10))

        pygame.display.update()
        FPSCLOCK.tick(fps)

if __name__ == '__main__':
    main()