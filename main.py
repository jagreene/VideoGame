from pygame import *
from pygame.sprite import *
from pygame.locals import *
import math
import time
import random



class Model:
    def __init__(self,screen):
        self.screen = screen
        self.map = {}
        self.blocks = Group()
        self.player = Player(25,825)
        self.players = Group()
        self.players.add(self.player)

    def createMap(self):
        map = {}
        for rows in xrange(0,(size[1]/50)):
            for columns in xrange(0,(size[0]/50)):
                if rows == (size[1]/50)-1 or rows == 0:
                    map.update({(rows,columns):"block"})
                elif(rows%5 == 0):
                    map.update({(rows,columns):random.choice(map_options)})
                else:
                    map.update({(rows,columns):"empty"})

        self.map = map

    def drawMap(self):
        for position, contain in self.map.items():
            if contain is "block":
                self.blocks.add(Block(position[1]*50,position[0]*50))

    def draw(self):
        self.screen.fill(blackColor)
        self.blocks.draw(self.screen)
        self.players.draw(self.screen)

    def update(self):
        self.blocks.update()
        self.players.update()

    def checkPlayerBlockCollisions(self,players,blocks):

        print self.player.onGround
        for collision in spritecollide(self.player, self.blocks, False):
            print "COLISION!!!"

            if 22 <= abs(self.player.rect.bottom - collision.rect.centery) <= 25:
                self.player.onGround = True
            if abs(self.player.rect.bottom - collision.rect.centery) < 25:
                self.player.onGround = True
            elif self.player.rect.top - collision.rect.centery < 25:
                self.player.hittingCeilling = True
            if abs(self.player.rect.right - collision.rect.centerx) < 27 and abs(self.player.rect.centery - collision.rect.centery) < 30:
                self.player.hittingWallRight = True
            if abs(self.player.rect.left - collision.rect.centerx) < 27 and abs(self.player.rect.centery - collision.rect.centery) < 30:
                self.player.hittingWallLeft = True
        print self.player.onGround


class Block(Sprite):
    def __init__(self,x,y,picture = "Pictures/CobbleStoneBlock.png"):
        Sprite.__init__(self)

        self.image     = pygame.image.load(picture)
        self.rect      = self.image.get_rect()
        self.mask      = pygame.mask.from_surface(self.image)
        
        self.rect.left = x
        self.rect.top  = y

class Player(Sprite):
    """docstring for Player"""
    def __init__(self, x,y,picture = "Pictures/testSprite.png"):
        Sprite.__init__(self)

        self.image = pygame.image.load(picture)
        self.rect  = self.image.get_rect()
        self.mask  = pygame.mask.from_surface(self.image)


        self.x      =  x
        self.y      =  y
        self.vx     =  0
        self.vy     =  0
        self.fx     =  0
        self.fy     =  0
        self.lastX  =  x
        self.lastY  =  y
        self.lastVx =  0
        self.lastVy =  0
        self.lastFx =  0
        self.lastFy =  0
        self.mass   =  5
        self.fg     =  0
        self.ff     =  0
        self.fn     =  0
        self.mu     = .6
    
        self.rect.center=(self.x,self.y)

        self.onGround         = False
        self.inGround         = False
        self.hittingCeilling  = False
        self.hittingWallRight = False
        self.hittingWallLeft  = False

        self.jumpCount = 0
        self.terminalVelocity = 3


    def moveForward(self):
        self.vx = 3
    def moveBackward(self):
        self.vx = -3
    def jump(self):
        self.vy = -8
    def setFriction(self):
        if int(self.vx) != 0:
            self.ff = -abs(self.vx)/self.vx*self.mu*abs(self.fn)
        else:
            self.ff = 0
    def setGravity(self):
        self.fg =  .25*self.mass
    def setNormalForce(self):
        if self.onGround:
            self.fn = -self.fg
            self.vy = 0
        if self.inGround:
            self.fn = -self.fg
            self.vy = -5
        if self.hittingCeilling:
            self.fn = 1
            self.vy = 2
        if self.hittingWallRight:
            self.fn = -1
            self.vx = -3
        if self.hittingWallLeft:
            self.fn = 1
            self.vx = 3
        elif (not self.onGround) and (not self.hittingCeilling) and (not self.hittingWallLeft) and (not self.hittingWallRight):
            self.fn = 0

    def update(self):
        if self.hittingCeilling or self.onGround:
            self.fx = self.ff
            self.fy = self.fg + self.fn
        else:
            self.fx = self.ff + self.fn
            self.fy = self.fg

        self.vx += self.fx/self.mass
        self.vy += self.fy/self.mass

        if self.vy > self.terminalVelocity:
            self.vy = self.terminalVelocity

        self.lastX = self.x
        self.lastY = self.y
        self.x += int(self.vx)
        self.y += int(self.vy)

        self.onGround         = False
        self.hittingCeilling  = False
        self.hittingWallRight = False
        self.hittingWallLeft  = False
        # print "Force in Y is " + str(self.fy)
        # print "V in Y is " + str(self.vy)
        # print "Collision Ground "     + str(self.onGround)
        # print "Collision Ceilling "   + str(self.hittingCeilling)
        # print "Collision Wall Left "  + str(self.hittingWallLeft)
        # print "Collision Wall Right " + str(self.hittingWallRight)

        if self.lastVx != 0:
            if self.vx/self.lastVx < 0:
                self.image = transform.flip(self.image,True,False)
                self.rect  = self.image.get_rect()

        self.rect.center = ((int(self.x)),int(self.y))


whiteColor = pygame.Color(255,255,255)
redColor   = pygame.Color(255,0,0)
blueColor  = pygame.Color(0,0,255)
greenColor = pygame.Color(0,255,0)
blackColor = pygame.Color(0,0,0)

map_options = ["empty","block"]

pygame.init()

size = (1600,900)
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
m = Model(screen)

running  = True
new_room = True
m.player.setGravity()

while running:
    if new_room:
        m.createMap()
        m.drawMap()
        new_room = False

    keys = pygame.key.get_pressed()
    m.checkPlayerBlockCollisions(m.player, m.blocks)


    if keys[pygame.K_ESCAPE]:
        running = False
    if m.player.onGround:
        if keys[pygame.K_RIGHT]: 
            m.player.moveForward()
        elif keys[pygame.K_LEFT]:
            m.player.moveBackward()                

    m.player.setNormalForce()
    print m.player.onGround
    m.player.setFriction()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_UP and m.player.jumpCount < 2:
                m.player.jump()
                m.player.jumpCount +=1
            if (m.player.hittingWallRight or m.player.hittingWallLeft):
                m.player.jumpCount -= 1
            elif m.player.onGround:
                m.player.jumpCount = 0

    m.update()

    m.player.lastx  = m.player.x
    m.player.lasty  = m.player.y
    m.player.lastVx = m.player.vx
    m.player.lastVy = m.player.vy
    m.player.lastFx = m.player.fx
    m.player.lastFy = m.player.fy

    m.checkPlayerBlockCollisions(m.player, m.blocks)
    m.player.setNormalForce()
    m.player.setFriction()
    m.update()

    m.player.lastx  = m.player.x
    m.player.lasty  = m.player.y
    m.player.lastVx = m.player.vx
    m.player.lastVy = m.player.vy
    m.player.lastFx = m.player.fx
    m.player.lastFy = m.player.fy

    m.draw()
    pygame.display.update()