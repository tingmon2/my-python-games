"""공격 미사일 진행방향 삼각형 닮음비가 아니라 사인 코사인 구해서 하는 방법있는지 해보기
    방어 미사일 여러 발 발사할 수 있게 만들어보기"""
import sys
from random import randint
from math import sin, cos, radians, hypot
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, Rect, KEYDOWN, K_ESCAPE
import os.path

class House:
    def __init__(self, xpos):
        self.rect = Rect(xpos, 550, 40, 40)
        self.exploded = False
        strip = pygame.image.load(os.path.join(FILEPATH, "strip.png"))
        self.images = (pygame.Surface((20, 20), pygame.SRCALPHA),
                        pygame.Surface((20, 20), pygame.SRCALPHA))
        self.images[0].blit(strip, (0, 0), Rect(0, 0, 20, 20))
        self.images[1].blit(strip, (0, 0), Rect(20, 0, 20, 20))

    def draw(self):
        if self.exploded:
            SURFACE.blit(self.images[1], self.rect.topleft)
        else:
            SURFACE.blit(self.images[0], self.rect.topleft)

class Missile:
    def __init__(self):
        self.max_count = 500
        self.interval = 1000
        self.pos = [0, 0]
        self.cpos = [0, 0]
        self.firetime = 0
        self.radius = 0
        self.reload(0)

    def reload(self, time_count):
        house_x = randint(0, 12) * 60 + 20
        self.pos = (randint(0, 800), house_x)
        self.interval = int(self.interval * 0.9)
        self.firetime = randint(0, self.interval) + time_count
        self.cpos = [0, 0]
        self.radius = 0

    def tick(self, time_count, shoot, houses):
        is_hit = False
        elapsed = time_count - self.firetime
        if elapsed < 0:
            return

        if self.radius > 0:
            self.radius += 1
            if self.radius > 100:
                self.reload(time_count)
        else:
            self.cpos[0] = (self.pos[1]-self.pos[0]) * elapsed / self.max_count + self.pos[0] 
            # 계산 마지막에 self.pos[0] 값을 더하는 이유는 
            # 해당 미사일 시작점의 기준좌표(self.pos[0], 0)에 따라 움직여야 하기 떄문
            # 만약 시작점의 x좌표 값을 더하지 않는다면 기준좌표는 (0, 0)이 되어버림
            self.cpos[1] = 575 * elapsed / self.max_count

            diff = hypot(shoot.shot_pos[0]-self.cpos[0], shoot.shot_pos[1]-self.cpos[1])
            if diff < shoot.radius:
                is_hit = True
                self.radius = 1

            if elapsed > self.max_count:
                self.radius = 1
                for house in houses:
                    if hypot(self.cpos[0]-house.rect.center[0], self.cpos[1]-house.rect.center[1]) < 30:
                        house.exploded = True

        return is_hit

    def draw(self):
        pygame.draw.line(SURFACE, (255, 0, 0), (self.pos[0], 0), self.cpos)

        if self.radius > 0:
            rad = self.radius if self.radius < 50 else 100 - self.radius
            pos = (int(self.cpos[0]), int(self.cpos[1])) # code changed
            pygame.draw.circle(SURFACE, (255, 0, 0), pos, rad)

class Shoot:
    def __init__(self):
        self.scope = (400, 300)
        self.image = pygame.image.load(os.path.join(FILEPATH, "scope.png"))
        self.count = 0
        self.fire = False
        self.radius = 0
        self.shot_pos = (0, 0) # aimed point

    def tick(self):
        if self.fire:
            self.count += 1

            if 50 <= self.count < 100: # code changed
                self.radius += 2
            elif 100 <= self.count < 150:
                self.radius -= 2
            elif self.count >= 150:
                self.fire = False
                self.count = 0

    def draw(self):
        rect = self.image.get_rect()
        rect.center = self.scope # scope = mouse pointer
        SURFACE.blit(self.image, rect)

        if not self.fire:
            return
        
        if self.radius == 0 and self.count < 100:
            ratio = self.count / 50 # code changed
            ypos = 600 - (600 - self.shot_pos[1]) * ratio
            x_left = (self.shot_pos[0]) * ratio
            x_right = 800 - (800 - self.shot_pos[0]) * ratio
            pygame.draw.line(SURFACE, (0, 255, 255), (0, 600), (x_left, ypos))
            pygame.draw.line(SURFACE, (255, 0, 255), (800, 600), (x_right, ypos))

        elif self.radius > 0:
            pygame.draw.circle(SURFACE, (123, 255, 111), self.shot_pos, self.radius)

pygame.init()
SURFACE = pygame.display.set_mode((800, 600))
FPSLOCK = pygame.time.Clock()
FILEPATH = os.path.dirname(__file__)

def main():
    game_over = False
    missiles = []
    score = 0
    time_count = 0
    shoot = Shoot()
    houses = []

    scorefont = pygame.font.SysFont(None, 36)
    sysfont = pygame.font.SysFont(None, 72)
    message_over = sysfont.render("NEW YORK IS DESTROYED!", True, (0, 255, 255))
    message_rect = message_over.get_rect()
    message_rect.center = (100, 300)

    for index in range(13):
        houses.append(House(index * 60 + 20))
    while len(missiles) < 18:
        missiles.append(Missile())

    while True:
        time_count += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                shoot.scope = event.pos 
            elif event.type == MOUSEBUTTONDOWN:
                if not shoot.fire:
                    shoot.shot_pos = shoot.scope
                    shoot.fire = True

        exploded = len(list(filter(lambda x: x.exploded, houses)))
        # exploded = len([x for x in houses if x.exploded])
        game_over = exploded == 13

        if not game_over:
            for missile in missiles:
                is_hit = missile.tick(time_count, shoot, houses)
                if is_hit:
                    score += 119
            shoot.tick()

        SURFACE.fill((0, 0, 0))
        shoot.draw()
        for house in houses:
            house.draw()
        for missile in missiles:
            missile.draw()

        score_str = str(score).zfill(6)
        score_image = scorefont.render(score_str, True, (255, 123, 50))
        SURFACE.blit(score_image, (700, 10))

        if game_over:
            SURFACE.blit(message_over, message_rect)

        pygame.display.update()
        FPSLOCK.tick(40)

if __name__ == '__main__':
    main()

        


