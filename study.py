import sys
from math import sin, cos, radians
import pygame
import random
from pygame.locals import QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        """
        SURFACE.fill((255, 255, 255))   

        pygame.draw.rect(SURFACE, (255, 0, 0), (10, 20, 100, 50))
        
        pygame.draw.rect(SURFACE, (255, 0 , 0), (150, 10, 100, 30), 3)
        
        pygame.draw.rect(SURFACE, (0, 255, 0), ((100, 80), (80, 50)))
        
        rect0 = Rect(200, 60, 140, 80)
        pygame.draw.rect(SURFACE, (0, 0, 255), rect0) 
        
        rect1 = Rect(30, 160, 100, 50)
        pygame.draw.rect(SURFACE, (255, 255, 0), rect1)
        
        pygame.draw.circle(SURFACE, (255, 0 , 0), (50, 50), 20)
        pygame.draw.circle(SURFACE, (255, 0, 0), (150, 50), 20, 10)
        pygame.draw.circle(SURFACE, (0, 255, 0), (50, 150), 10)
        pygame.draw.circle(SURFACE, (0, 255, 0), (300, 300), 20, 10)
        pygame.draw.circle(SURFACE, (255, 255, 0), (250, 150), 30)

        pygame.draw.ellipse(SURFACE, (124, 251, 142), (50, 50, 140, 60)) 
        pygame.draw.ellipse(SURFACE, (142, 49, 89), (250, 30, 90, 90))
        pygame.draw.ellipse(SURFACE, (57, 82, 244), (200, 100, 80, 120), 20)
        pygame.draw.ellipse(SURFACE, (255, 123, 123), (500, 500, 100, 100), 20)
        
        pygame.draw.line(SURFACE, (255, 0, 0), (180, 180), (500, 180))
        pygame.draw.line(SURFACE, (255, 0, 0), (220, 200), (220, 400), 10)
        pygame.draw.line(SURFACE, (0, 255, 0), (250, 420), (250, 600), 5)
        start_pos = (300, 300)
        end_pos = (420, 550)
        pygame.draw.line(SURFACE, (0, 0, 255), start_pos, end_pos, 10)
        """
        """
        SURFACE.fill((0, 0, 0))
        
        for xpos in range(0, 800, 25):
            pygame.draw.line(SURFACE, 0xFFFFFF, (xpos, 0), (xpos, 600))
        
        for ypos in range(0, 600, 25):
            pygame.draw.line(SURFACE, 0xFFFFFF, (0, ypos), (800, ypos))
        """
        """
        SURFACE.fill((0, 0, 0))
        
        pointlist = []
        for _ in range(30):
            xpos = random.randint(0, 800)
            ypos = random.randint(0, 600)
            pointlist.append((xpos, ypos))
            
        pygame.draw.lines(SURFACE, (255, 255, 255), True, pointlist, 5)
        """

        SURFACE.fill((0, 0, 0))
        
        pointlist0 = []
        pointlist1 = []
        for theta in range(0, 360, 72):
            rad = radians(theta)
            pointlist0.append((cos(rad)*100 + 100, sin(rad)*100 + 150))
            pointlist1.append((cos(rad)*100+ 400, sin(rad)*100 + 150))
        
        pygame.draw.lines(SURFACE, (255, 255, 255), True, pointlist0)
        pygame.draw.polygon(SURFACE, (255, 255, 255), pointlist1)


        
        
        pygame.display.update()
        FPSCLOCK.tick(10)
        
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    