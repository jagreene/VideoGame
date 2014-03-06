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
        self.player = Player(25,850)
        self.players = Group()
        self.players.add(self.player)

    def createMap(self):
        map = {}
        for rows in xrange(0,(size[1]/50)):
            for columns in xrange(0,(size[0]/50)):
                if rows == (size[1]/50)-1 or rows == 0:
                    map.update({(rows,columns):"block"})
                elif(rows%3 == 0):
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
        self.blocks.update()
        self.blocks.draw(self.screen)
        self.players.update()
        self.players.draw(self.screen)

    def checkPlayerBlockCollisions(self,players,blocks):
        print "Checking Collision"
        self.onGround         = False
        self.hittingWallRight = False
        self.hittingCeilling  = False

        print self.onGround

        for collision in spritecollide(self.player, self.blocks, False):
            print "COLISION!!!"
            if abs(self.player.rect.bottom - collision.rect.centery) < 25 and abs(self.player.lastY - collision.rect.centery)>25:
                self.player.onGround = True
            elif self.player.rect.top - 1 < collision.rect.centery < 25 and self.player.lastY + 14 - collision.rect.centery > 25:
                self.player.hittingCeilling = True
            elif abs(self.player.rect.right - collision.rect.centerx) < 25:
                self.player.hittingWallRight = True
            elif self.player.rect.left - 1 < collision.rect.y < self.player.rect.left + 1:
                self.player.hittingWallLeft = True


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

        self.lastX = x
        self.lastY = y
        self.x     =  x
        self.y     =  y
        self.vx    =  0
        self.vy    =  0
        self.fx    =  0
        self.fy    =  0
        self.mass  =  5
        self.fg    =  0
        self.ff    =  0
        self.fn    =  0
        self.mu    = .1
    
        self.rect.bottomleft=(self.x,self.y)

        self.onGround         = True
        self.hittingCeilling  = False
        self.hittingWallRight = False
        self.hittingWallLeft  = False


    def moveForward(self):
        self.vx = 5 
    def moveBackward(self):
        self.vx = -5
    def jump(self):
        self.vy = -5
    def setFriction(self):
        if int(self.vx) != 0:
            self.ff = -abs(self.vx)/self.vx*self.mu*abs(self.fn)
        else:
            self.ff = 0
    def setGravity(self):
        self.fg =  2*self.mass
    def setNormalForce(self):
        if self.onGround:
            self.fn = -(self.vy*1)*self.mass-self.fg
        if self.hittingCeilling:
            self.fn =  (self.vy*1)*self.mass+self.fg
        if self.hittingWallRight:
            self.fn = -(self.vx*1)*self.mass
        if self.hittingWallLeft:
            self.fn =  (self.vx*1)*self.mass
        elif (not self.onGround) and (not self.hittingCeilling) and (not self.hittingWallLeft) and (not hittingWallRight):
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

        self.lastX = self.x
        self.lastY = self.y
        self.x += int(self.vx)
        self.y += int(self.vy)
        print "force = " + str(self.fy)
        print "velocity = " + str(self.vy)
        print "Collision Ground "     + str(self.onGround)
        print "Collision Ceilling "   + str(self.hittingCeilling)
        print "Collision Wall Left "  + str(self.hittingWallLeft)
        print "Collision Wall Right " + str(self.hittingWallRight)

        self.rect.bottomleft=((int(self.x)),int(self.y))


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
while running:
    if new_room:
        m.createMap()
        m.drawMap()
        new_room = False

    keys = pygame.key.get_pressed()
    m.checkPlayerBlockCollisions(m.player, m.blocks)
    m.player.setGravity()
    if m.player.onGround:
        m.player.setFriction()
        m.player.setNormalForce()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_UP:
                m.player.jump()

    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_RIGHT]: 
        m.player.moveForward()
    elif keys[pygame.K_LEFT]:
        m.player.moveBackward()

            #elif event.key == pygame.K_UP:
                


    m.draw()
    pygame.display.update()
    time.sleep(1.0/120.0)
