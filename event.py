import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP

pygame.init()
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    mousepos = []
    mousedown = False
    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousedown = True
                startpos = event.pos
                pygame.draw.circle(SURFACE, (0, 255, 0), startpos, 5)
            elif event.type == MOUSEMOTION:
                if mousedown:
                    mousepos.append(event.pos)
            elif event.type == MOUSEBUTTONUP:
                mousedown = False
                mousepos.clear()
                endpos = event.pos
                pygame.draw.circle(SURFACE, (0, 255, 0), endpos, 5)

        if counter == 0 :
            SURFACE.fill((255, 255, 255)) 
            counter += 1

        if len(mousepos) > 1:
            pygame.draw.lines(SURFACE, (255, 0, 0), False, mousepos, 5)

        pygame.display.update()
        FPSCLOCK.tick(60)

if __name__ == '__main__':
    main()