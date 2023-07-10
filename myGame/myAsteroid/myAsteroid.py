import sys
from math import radians, sin, cos
from random import randint
import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_RIGHT,K_LEFT, K_DOWN, KEYUP, K_SPACE, K_ESCAPE, Rect
import os.path

pygame.init()
pygame.key.set_repeat(4)
SURFACE = pygame.display.set_mode((800, 800))
FPSCLOCK = pygame.time.Clock()
FILEPATH = os.path.dirname(__file__)

class Drawable:
    def __init__(self, rect):
        self.rect = rect # coordinate and size of the creating object
        self.step = [0, 0] # a number which will be a step for x and y coordinate for each frame
    
    def move(self):
        thing = self.rect.center
        xpos = (thing[0] + self.step[0]) % 800 
        ypos = (thing[1] + self.step[1]) % 800
        self.rect.center = (xpos, ypos)

class Frog(Drawable):
    def __init__(self, pos, size):
        super(Frog, self).__init__(Rect(0, 0, size, size))
        self.rect.center = pos
        self.image = pygame.image.load(os.path.join(FILEPATH, "frog.gif"))
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.theta = randint(0, 360) # direction of movement of rock
        self.size = size
        self.power = 128 / size
        self.step[0] = cos(radians(self.theta)) * self.power
        self.step[1] = sin(radians(self.theta)) * -self.power  

    def draw(self):
        rotated = pygame.transform.rotozoom(self.image, self.theta, self.size / 64)
        rect = rotated.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(rotated, rect)
    
    def tick(self):
        self.theta += randint(3, 10)
        self.move()

class Shot(Drawable):
    def __init__(self):
        super(Shot, self).__init__(Rect(0, 0, 6, 6))
        self.count = 40
        self.power = 10
        self.max_count = 40

    def draw(self):
        if self.count < self.max_count:
            pygame.draw.rect(SURFACE, (255, 0, 0), self.rect)

    def tick(self):
        self.count += 1
        self.move()

class Ship(Drawable):
    def __init__(self):
        super(Ship, self).__init__(Rect(355, 370, 60, 60))
        self.theta = 0
        self.power = 0
        self.accel = 0
        self.explode = False
        self.ship = pygame.image.load(os.path.join(FILEPATH, "rocket.png"))
        self.ship = pygame.transform.scale(self.ship, (60, 60))
        self.bang = pygame.image.load(os.path.join(FILEPATH, "bang.png"))

    def draw(self):
        rotated = pygame.transform.rotate(self.ship, self.theta)
        rect = rotated.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(rotated, rect)
        if self.explode:
            SURFACE.blit(self.bang, rect)

    def tick(self):
        self.power += self.accel
        self.accel *= 0.94 # slow down the speed if there's no command in the keymap
        self.power *= 0.94
        self.step[0] = cos(radians(self.theta)) * self.power
        self.step[1] = sin(radians(self.theta)) * -self.power
        self.move()

def key_event_handler(keymap, ship):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if not event.key in keymap:
                keymap.append(event.key)
            if K_LEFT in keymap:
                ship.theta += 6
            if K_RIGHT in keymap:
                ship.theta -= 6
            if K_UP in keymap:
                ship.accel = min(5, ship.accel + 0.2)
            if K_DOWN in keymap:
                ship.accel = max(-5, ship.accel - 0.1)
            if K_ESCAPE in keymap:
                main()
        elif event.type == KEYUP:
            if event.key in keymap:
                keymap.remove(event.key)
def main():
    sysfont = pygame.font.SysFont(None, 72)
    scorefont = pygame.font.SYsysfont = pygame.font.SysFont(None, 36)
    message_clear = sysfont.render("MISSION COMPLETE!!", True, (255, 0, 255))
    message_over = sysfont.render("CHICKET IS DEAD!!", True, (255, 0, 255))
    message_position = message_clear.get_rect()
    message_position.center = (200, 400)

    keymap = []
    shots = []
    frogs = []
    ship = Ship()
    game_over = False
    score = 0
    background_position = [0, 0]
    back_image = pygame.image.load(os.path.join(FILEPATH, "bg.png"))
    back_image = pygame.transform.scale2x(back_image)

    while len(shots) < 8:
        shots.append(Shot())
    
    while len(frogs) < 5:
        pos = randint(0, 800), randint(0, 800)
        frog = Frog(pos, 60)
        if not frog.rect.colliderect(ship.rect):
            frogs.append(frog)

    while True:
        key_event_handler(keymap, ship)

        if not game_over:
            ship.tick() # change step of ship for each frame, tick method calculates direction and speed
                        # tick method means program will call move method in the Drawable class which
                        # manipulate object's x and y coordinates
            for frog in frogs:
                frog.tick()
                if frog.rect.colliderect(ship.rect):
                    ship.explode = True
                    game_over = True

            fire = False
            for shot in shots:
                if shot.count < shot.max_count:
                    shot.tick()

                    hit_frog = None
                    for frog in frogs:
                        if frog.rect.colliderect(shot.rect):
                            hit_frog = frog
                    if hit_frog != None:
                        score += hit_frog.rect.width * 10
                        shot.count = shot.max_count
                        frogs.remove(hit_frog)
                        if hit_frog.rect.width > 30:
                            frogs.append(Frog(hit_frog.rect.midleft, hit_frog.rect.width/2))
                            frogs.append(Frog(hit_frog.rect.midright, hit_frog.rect.width/2))
                            frogs.append(Frog(hit_frog.rect.midtop, hit_frog.rect.width/2))
                            frogs.append(Frog(hit_frog.rect.midbottom, hit_frog.rect.width/2))
                        if len(frogs) == 0:
                            game_over = True
                elif not fire and K_SPACE in keymap:
                    shot.count = 0
                    shot.rect.center = ship.rect.center
                    shot_x = cos(radians(ship.theta)) * shot.power
                    shot_y = sin(radians(ship.theta)) * -shot.power
                    shot.step = (shot_x, shot_y)
                    fire = True
            
        background_position[0] = (background_position[0] + ship.step[0] / 2) % 1600
        background_position[1] = (background_position[1] + ship.step[1] / 2) % 1600
        SURFACE.fill((0, 0, 0))
        SURFACE.blit(back_image, (-background_position[0], -background_position[1]),
                        (0, 0, 3200, 3200)) # code changed
        
        ship.draw()
        for frog in frogs:
            frog.draw()
        for shot in shots:
            shot.draw()

        score_str = str(score).zfill(6)
        message_score = scorefont.render(score_str, True, (0, 0, 255))
        SURFACE.blit(message_score, (700, 10))

        if game_over:
            if len(frogs) == 0:
                SURFACE.blit(message_clear, message_position.center)
            else:
                SURFACE.blit(message_over, message_position.center)

        pygame.display.update()
        FPSCLOCK.tick(20)

if __name__ == '__main__':
    main()
            
    
     