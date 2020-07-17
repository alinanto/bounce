import pygame
import sys
from pygame.locals import * 
pygame.init()

#constants

TRUE = 1
FALSE = 0
WIDTH = 800
HEIGHT = 600
BG_COLOR = pygame.Color('black')
BALL_COLOR = 'red'
ANIMATOR = pygame.USEREVENT + 1
PHY_ENG = pygame.USEREVENT + 2
FPS = 60  #max = 100
SPS = 100 #max = 100
BOUNCE_FACTOR = 0.35
GRAVITY = 0.3
VISCOUS_CONST_Y = 0.995
VISCOUS_CONST_X = 0.915
DEAD_ZONE = 0.001
JUMB = 9
SIDE_STEP = 0.32
SPEED_LIMIT = 30

#class definition

class Ball :
    def __init__(self,color_string,x,y,radius,dx,dy):
        self.color = pygame.Color(color_string)
        self.x = x
        self.y = y
        self.pos = (int(x),int(y))
        self.dx = dx
        self.dy = dy
        self.jumbing = FALSE
        self.left = FALSE
        self.right = FALSE
        self.radius = radius
        pygame.draw.circle(screen,self.color,self.pos,radius)
    def update(self):
        #position engine
        self.x += self.dx
        self.y += self.dy
        #bounce engine
        if self.x>=WIDTH-self.radius and self.dx>0 :
            self.dx *= -BOUNCE_FACTOR
            self.x = WIDTH-self.radius
        if self.x<=self.radius and self.dx<0 :
            self.dx *= -BOUNCE_FACTOR
            self.x = self.radius
        if self.y>=HEIGHT-self.radius and self.dy>0 :
            self.dy *= -BOUNCE_FACTOR
            self.y = HEIGHT-self.radius
        elif self.y<=self.radius and self.dy<0 :
            self.dy *= -BOUNCE_FACTOR
            self.y = self.radius
        #gravity engine
        self.dy += GRAVITY
        #viscous engine
        self.dx *= VISCOUS_CONST_X
        self.dy *= VISCOUS_CONST_Y
        #controls
        if self.left :
            self.dx -= SIDE_STEP
            if self.dx < -SPEED_LIMIT :
                self.dx = -SPEED_LIMIT
        if self.right :
            self.dx += SIDE_STEP
            if self.dx > SPEED_LIMIT :
                self.dx = SPEED_LIMIT
        #deadzone engine
        if abs(self.dx) <= DEAD_ZONE :
            self.dx = 0
        if abs(self.dy) <= DEAD_ZONE :
            self.dy = 0
    def draw(self) :
        pygame.draw.circle(screen,BG_COLOR,self.pos,self.radius)
        self.pos = (int(self.x),int(self.y))
        pygame.draw.circle(screen,self.color,self.pos,self.radius)
                               
#initialisation

screen = pygame.display.set_mode((WIDTH,HEIGHT))
RectFullScreen = pygame.Rect(0,0,WIDTH,HEIGHT)
pygame.draw.rect(screen,BG_COLOR,RectFullScreen)
pygame.time.set_timer(ANIMATOR,1000//FPS)
pygame.time.set_timer(PHY_ENG,1000//SPS)
ball1 = Ball(BALL_COLOR,200,20,20,0,0)
pygame.display.update()

#event loops

while 1 :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()
        if event.type == PHY_ENG :
            ball1.update()
        if event.type == ANIMATOR :
            ball1.draw()
            pygame.display.update()
        if event.type == pygame.KEYDOWN :
            if event.key == K_w :
                ball1.dy = -JUMB
            if event.key == K_a :
                ball1.left = TRUE
                ball1.right = FALSE
            if event.key == K_d :
                ball1.right = TRUE
                ball1.left = FALSE
        if event.type == pygame.KEYUP :
            if event.key == K_a :
                ball1.left = FALSE
            if event.key == K_d :
                ball1.right = FALSE
