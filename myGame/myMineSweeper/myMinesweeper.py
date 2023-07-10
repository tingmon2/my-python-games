import sys
from math import floor
from random import randint
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE
import os.path

WIDTH = 20
HEIGHT = 15
SIZE = 50
NUM_OF_BOMB = 30
EMPTY = 0
BOMB = 1
OPENED = 2
OPEN_COUNT = 0
CHECKED = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
FILEPATH = os.path.dirname(__file__)
NUMBER = 0

pygame.init()
SURFACE = pygame.display.set_mode([WIDTH*SIZE, HEIGHT*SIZE])
FPSCLOCK = pygame.time.Clock()

def num_of_bomb(field, x_pos, y_pos):
    count = 0
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            xpos = x_pos + x_offset
            ypos = y_pos + y_offset
        if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and field[ypos][xpos] == BOMB:
            count += 1
    return count

def open_tile(field, x_pos, y_pos):
    global OPEN_COUNT
    global NUMBER
    if CHECKED[y_pos][x_pos]:
        return
    
    CHECKED[y_pos][x_pos] = True

    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            xpos = x_pos + x_offset
            ypos = y_pos + y_offset
            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and field[ypos][xpos] == EMPTY:
                field[ypos][xpos] = OPENED
                OPEN_COUNT += 1
                NUMBER += 1
                count = num_of_bomb(field, xpos, ypos)
                if count == 0 and NUMBER < 2:
                    open_tile(field, xpos, ypos)
                else:
                    NUMBER = 0


def main():
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 60)
    message_clear = largefont.render("You Have Rescued Mr.Donald Trump!!", True, (0, 255, 255))
    message_over = largefont.render("Kabooom!! White House is Detonated!!", True, (255, 0 ,0))
    message_rect = message_clear.get_rect()
    message_rect.center = (WIDTH*SIZE/2, HEIGHT*SIZE/2)
    game_over = False
    bang_image = pygame.image.load(os.path.join(FILEPATH, "bang2.png"))

    field = [[EMPTY for xpos in range(WIDTH)] for ypos in range(HEIGHT)]

    count = 0
    while count < NUM_OF_BOMB:
        xpos = randint(0, WIDTH-1)
        ypos = randint(0, HEIGHT-1)
        if field[ypos][xpos] == EMPTY:
            field[ypos][xpos] = BOMB
            count += 1
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                xpos = floor(event.pos[0] / SIZE)
                ypos = floor(event.pos[1] / SIZE)
                if field[ypos][xpos] == BOMB:
                    game_over = True
                else:
                    open_tile(field, xpos, ypos)
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game_over = False
                global OPEN_COUNT
                OPEN_COUNT = 0
                global CHECKED 
                CHECKED = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
                main()
        
        SURFACE.fill((0, 0, 0))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                tile = field[ypos][xpos]
                square = (xpos*SIZE, ypos*SIZE, SIZE, SIZE)
                bang_coordinate = (xpos*SIZE, ypos*SIZE)

                if tile == EMPTY or tile == BOMB:
                    pygame.draw.rect(SURFACE, (192, 192, 192), square)
                    if game_over and tile == BOMB:
                        SURFACE.blit(bang_image, bang_coordinate)
                elif tile == OPENED:
                    count = num_of_bomb(field, xpos, ypos)
                    if count > 0:
                        num_image =  smallfont.render("{}".format(count), True, (255, 255, 0))
                        SURFACE.blit(num_image, (xpos*SIZE+10, ypos*SIZE+10))
            
        for index in range(0, WIDTH*SIZE, SIZE):
            pygame.draw.line(SURFACE, (96, 96, 96), (index, 0), (index, HEIGHT*SIZE))
        for index in range(0, HEIGHT*SIZE, SIZE):
            pygame.draw.line(SURFACE, (96, 96, 96), (0, index), (WIDTH*SIZE, index))
        
        if OPEN_COUNT == WIDTH*HEIGHT - NUM_OF_BOMB:
            SURFACE.blit(message_clear, message_rect)
        elif game_over:
            SURFACE.blit(message_over, message_rect)
        
        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()