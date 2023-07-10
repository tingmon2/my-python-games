import sys
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_RIGHT, K_LEFT, K_DOWN, Rect

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()
FOODS = []
WIDTH = 20
HEIGHT = 20

class Snake:
    def __init__(self, pos):
        self.bodies = [pos]

    def move(self, key):
        xpos = self.bodies[0][0]
        ypos = self.bodies[0][1]

        if key == K_LEFT:
            xpos -= 1
        elif key == K_RIGHT:
            xpos += 1
        elif  key == K_DOWN:
            ypos += 1
        elif  key == K_UP:
            ypos -= 1
        head = (xpos, ypos)

        is_game_over = head in self.bodies or head[0] < 0 or head[0] >= WIDTH or \
            head[1] < 0 or head[1] >= HEIGHT

        self.bodies.insert(0, head)
        if head in FOODS:
            i = FOODS.index(head)
            del FOODS[i]
            add_food(self)
        else:
            self.bodies.pop()
        return is_game_over
    
    def draw(self):
        for body in self.bodies:
            pygame.draw.rect(SURFACE, (0, 100, 255),
                             Rect(body[0]*30, body[1]*30, 30, 30))
    
def add_food(snake):
    while True:
        pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        if pos in snake.bodies or pos in FOODS:
            continue
        FOODS.append(pos)
        break

def paint(snake, message):
    SURFACE.fill((0, 0, 0))
    framefont = pygame.font.SysFont(None, 20)
    frame = framefont.render("coordinate: {}, {}".format(snake.bodies[0][0]*30, 
                                snake.bodies[0][1]*30), True, (240, 192, 100))
    snake.draw()
    for food in FOODS:
        pygame.draw.ellipse(SURFACE, (170, 100, 240), Rect(food[0]*30, food[1]*30, 30, 30))
    for index in range(20):
        pygame.draw.line(SURFACE, (90, 90, 90), (index*30, 0), (index*30, 600))
        pygame.draw.line(SURFACE, (90, 90, 90), (0, index*30), (600, index*30))
    if message != None:
        SURFACE.blit(message, (150, 300))
    
    SURFACE.blit(frame, (400, 40))

    pygame.display.update()

def main():
    myfont = pygame.font.SysFont(None, 80)
    key = K_DOWN
    message = None
    game_over = False
    snake = Snake((WIDTH/2, HEIGHT/2))

    for _ in range(10):
        add_food(snake)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                key = event.key
        if game_over:
            message = myfont.render("GAME OVER!!", True, (32, 192, 230))
        else:
            game_over = snake.move(key)

        paint(snake, message)
        FPSCLOCK.tick(5)

if __name__ == '__main__':
    main()