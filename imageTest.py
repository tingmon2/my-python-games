
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                chicken = pygame.image.load("rocket.png")    
                SURFACE.fill((255, 255, 255))
                pygame.display.update()
                SURFACE.blit(chicken, (50, 50))
        
                pygame.display.update()
                FPSCLOCK.tick(5)
                

        
if __name__ == '__main__':
    main()