#PONG pygame

from UDP.UDP import UDP
from Main import Robot
from Dynamics import Dynamics
import time
import math
import random
import pygame, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2


class pong():

    def __init__(self):
        self._ball_pos = [0,0]
        self._ball_vel = [0,0]
        self._paddle1_vel = 0
        self._paddle2_vel = 0
        self._l_score = 0
        self._r_score = 0

        self._window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('Hello World')

        self._paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT / 2]
        self._paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT / 2]

        if random.randrange(0, 2) == 0:
            self.ball_init(True)
        else:
            self.ball_init(False)


        #canvas declaration
#window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
#pygame.display.set_caption('Hello World')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
    def ball_init(self,right):
        self._ball_pos = [WIDTH/2,HEIGHT/2]
        horz = random.randrange(2,4)
        vert = random.randrange(1,3)

        if right == False:
            horz = - horz

        self._ball_vel = [horz,-vert]


#draw function of canvas
    def draw(self):

        canvas = self._window
        canvas.fill(BLACK)
        pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
        pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
        pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

        # update paddle's vertical position, keep paddle on the screen
        if self._paddle1_pos[1] > HALF_PAD_HEIGHT and self._paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            self._paddle1_pos[1] += self._paddle1_vel
        elif self._paddle1_pos[1] == HALF_PAD_HEIGHT and self._paddle1_vel > 0:
            self._paddle1_pos[1] += self._paddle1_vel
        elif self._paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and self._paddle1_vel < 0:
            self._paddle1_pos[1] += self._paddle1_vel

        if self._paddle2_pos[1] > HALF_PAD_HEIGHT and self._paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            self._paddle2_pos[1] += self._paddle2_vel
        elif self._paddle2_pos[1] == HALF_PAD_HEIGHT and self._paddle2_vel > 0:
            self._paddle2_pos[1] += self._paddle2_vel
        elif self._paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and self._paddle2_vel < 0:
            self._paddle2_pos[1] += self._paddle2_vel

        #update ball
        self._ball_pos[0] += int(self._ball_vel[0])
        self._ball_pos[1] += int(self._ball_vel[1])

        #draw paddles and ball
        pygame.draw.circle(canvas, RED, self._ball_pos, 20, 0)
        pygame.draw.polygon(canvas, GREEN, [[self._paddle1_pos[0] - HALF_PAD_WIDTH, self._paddle1_pos[1] \
                                             - HALF_PAD_HEIGHT], [self._paddle1_pos[0] - HALF_PAD_WIDTH, \
                                             self._paddle1_pos[1] + HALF_PAD_HEIGHT], \
                                             [self._paddle1_pos[0] + HALF_PAD_WIDTH, \
                                              self._paddle1_pos[1] + HALF_PAD_HEIGHT],
                                              [self._paddle1_pos[0] + HALF_PAD_WIDTH, self._paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)

        pygame.draw.polygon(canvas, GREEN, [[self._paddle2_pos[0] - HALF_PAD_WIDTH, self._paddle2_pos[1] - HALF_PAD_HEIGHT], [self._paddle2_pos[0] - HALF_PAD_WIDTH, self._paddle2_pos[1] + HALF_PAD_HEIGHT], [self._paddle2_pos[0] + HALF_PAD_WIDTH, self._paddle2_pos[1] + HALF_PAD_HEIGHT], [self._paddle2_pos[0] + HALF_PAD_WIDTH, self._paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

        #ball collision check on top and bottom walls
        if int(self._ball_pos[1]) <= BALL_RADIUS:
            self._ball_vel[1] = - self._ball_vel[1]
        if int(self._ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
            self._ball_vel[1] = -self._ball_vel[1]

        #ball collison check on gutters or paddles
        if int(self._ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(self._ball_pos[1]) in range(self._paddle1_pos[1] - HALF_PAD_HEIGHT,self._paddle1_pos[1] + HALF_PAD_HEIGHT,1):
            self._ball_vel[0] = -self._ball_vel[0]
            self._ball_vel[0] *= 1.1
            self._ball_vel[1] *= 1.1
        elif int(self._ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
            self._r_score += 1
            self.ball_init(True)

        if int(self._ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(self._ball_pos[1]) in range(self._paddle2_pos[1] - HALF_PAD_HEIGHT,self._paddle2_pos[1] + HALF_PAD_HEIGHT,1):
            self._ball_vel[0] = -self._ball_vel[0]
            self._ball_vel[0] *= 1.1
            self._ball_vel[1] *= 1.1
        elif int(self._ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
            self._l_score += 1
            self.ball_init(False)

        #update scores
        myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
        label1 = myfont1.render("Score "+str(self._l_score), 1, (255,255,0))
        canvas.blit(label1, (50,20))

        myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
        label2 = myfont2.render("Score "+str(self._r_score), 1, (255,255,0))
        canvas.blit(label2, (470, 20))
    
    

    def update(self,robot):

        pose1, pose2, pose3 = Dynamics.fk(robot)
        x, y, z  = pose3[0], pose3[1], pose3[2]
        #self._paddle1_vel = -int(math.ceil(x))
        #self._paddle2_vel = int(math.ceil(y))
        print -int(math.ceil(x))
        self.draw()
        pygame.display.update()
        fps.tick(60)
        #return x_ee, y_ee, z_ee




# #game loop
# while True:
#
#     draw(window)
#
#     for event in pygame.event.get():
#
#
#
#
#         x, y, z = read_Data()
#
#         paddle1_vel = -int(math.ceil(x))
#         paddle2_vel = int(math.ceil(y))
#
#         if event.type == KEYDOWN:
#             keydown(event)
#         elif event.type == KEYUP:
#             keyup(event)
#         elif event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#
#
#     pygame.display.update()
#     fps.tick(60)