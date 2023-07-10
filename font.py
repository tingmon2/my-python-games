import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    sysfont = pygame.font.SysFont(None, 72)
    message = sysfont.render("Hello Python!", True, (0, 128, 128))
    message_rect = message.get_rect()
    message_rect.center = (200, 100)
    theta = 0
    scale = 1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                SURFACE.fill((255, 255, 255))
                pygame.display.update()
                theta += 5
                scale = (theta % 360) / 180
                tmp_msg = pygame.transform.rotozoom(message, theta, scale)
                tmp_rect = tmp_msg.get_rect()
                tmp_rect.center = (200, 150)
                SURFACE.blit(tmp_msg, tmp_rect)
                pygame.display.update()
                FPSCLOCK.tick(60)


if __name__ == '__main__':
    main()