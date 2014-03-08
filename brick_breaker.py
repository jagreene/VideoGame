# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:34:24 2014

@author: pruvolo
"""

import pygame
from pygame.locals import *
import random
import math
import time

class Model:
    def __init__(self, screen):
        self.screen = screen
        self.bricks = []
        for x in range(20,620,120):
            for y in range(20,240,30):
                brick_color = random.choice(all_colors)
                new_brick = Brick(x,y,100,20,brick_color)
                self.bricks.append(new_brick)
        self.paddle = Paddle(200,440,100,20)
    
    def draw(self):
        self.screen.fill(whiteColor)
        for brick in self.bricks:
            pygame.draw.rect(self.screen, brick.color, pygame.Rect(brick.x,brick.y,brick.width,brick.height))
        pygame.draw.rect(self.screen, whiteColor, pygame.Rect(self.paddle.x,self.paddle.y,self.paddle.width,self.paddle.height))

    def update(self):
        self.paddle.update()

    def change_paddle_velocity(self,acceleration):
        self.paddle.velocity_x += acceleration

class Brick:
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
class Paddle:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0.0
    
    def update(self):
        self.x += self.velocity_x
        if self.x < 0 or self.x + self.width > 640:
            self.velocity_x = 0

whiteColor = pygame.Color(255,255,255)
redColor   = pygame.Color(255,0,0)
blueColor  = pygame.Color(0,0,255)
greenColor = pygame.Color(0,255,0)
all_colors = [redColor, blueColor, greenColor]

blackColor = pygame.Color(0,0,0)


pygame.init()

size = (640,480)
screen = pygame.display.set_mode(size)
m = Model(screen)

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT:
                m.change_paddle_velocity(-1)
            elif event.key == pygame.K_RIGHT:
                m.change_paddle_velocity(1)
        
    m.update()
    m.draw()
    pygame.display.update()
    time.sleep(.001)

pygame.quit()
