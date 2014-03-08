from pygame import *
from pygame.sprite import *
from pygame.time import *
from pygame.locals import *
import math
import random



class Model:
    def __init__(self,screen):
        self.screen = screen
        self.buttons = Group(Button(700,450,"1P"),Button(900,450,"2P"))

    def initGame(self):
        self.map = {}
        self.blocks = Group()
        self.Coins =Group()
        self.players = Group()
        self.player1 = Player(75,825,1)
        self.players.add(self.player1)
        if self.playernum == 2:
            self.player2 = Player(1525,75,2)
            self.players.add(self.player2)
        else:
            self.player2 = False

    def createMap(self):
        map = {}
        for rows in xrange(0,(size[1]/50)):
            for columns in xrange(0,(size[0]/50)):
                if rows == (size[1]/50)-1 or rows == 0 or columns== (size[0]/50)-1 or columns==0:
                    map.update({(rows,columns):"block"})
                elif(rows%3 == 0):
                    map.update({(rows,columns):random.choice(map_options)})
                else:
                    map.update({(rows,columns):random.choice(map_options[:1])})

        self.map = map

    def drawMap(self):
        for position, contain in self.map.items():
            if contain is "block":
                self.blocks.add(Block(position[1]*50,position[0]*50))
            elif contain is "Coins":
                self.Coins.add(Coins(position[1]*50+10,position[0]*50+10))
        
    def update(self):
        self.blocks.update()
        self.players.update()
        self.Coins.update()

    def checkPlayerBlockCollisions(self,player,blocks):

        for collision in spritecollide(player, blocks, False):

            if 21 <= abs(player.rect.bottom - collision.rect.centery) <= 26:
                player.onGround = True
            elif player.rect.top - collision.rect.centery < 25:
                player.hittingCeilling = True
            if abs(player.rect.right - collision.rect.centerx) < 32 and abs(player.rect.centery - collision.rect.centery) < 28:
                player.hittingWallRight = True
            if abs(player.rect.left - collision.rect.centerx) < 32 and abs(player.rect.centery - collision.rect.centery) < 28:
                player.hittingWallLeft = True

            print "hittingWallLeft: " + str(self.player1.hittingWallLeft)
            print "hittingWallRight: " + str(self.player1.hittingWallRight)
    def checkPlayerCoinsCollisions(self, player, Coins):
        for collision in spritecollide(player, Coins, True):
            player.score += 1

class View():
    def __init__(self,screen, model):
        self.screen = screen
        self.screen.fill(blackColor)
        self.model = model


    def displayStartScreen(self):
        self.model.buttons.draw(self.screen)
        pygame.display.update()


    def update(self):
        self.screen.fill(blackColor)
        self.model.blocks.draw(self.screen)
        self.model.players.draw(self.screen)
        self.model.buttons.draw(self.screen)
        self.model.Coins.draw(self.screen)
        p1Score = myfont.render("Player 1 Score:"+str(self.model.player1.score), 1, whiteColor)
        self.screen.blit(p1Score,(100,15))
        if self.model.playernum==2:
            p2Score = myfont.render("Player 2 Score:"+str(self.model.player2.score), 1,whiteColor)
            self.screen.blit(p2Score,(1200,15))
        pygame.display.update()



class Controller():
    def __init__(self,model):
        self.model = model

    def checkPlayerSelection(self):
        starting = True
        for button in self.model.buttons.sprites():
            if button.rect.collidepoint(mouse.get_pos()) and mouse.get_pressed()[0]:
                if button.function == "1P":
                    self.model.playernum = 1
                    starting = False
                else:
                    self.model.playernum = 2
                    print self.model.playernum
                    starting = False


        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Quit"

        return starting


    def handleOneTimeKeys(self):
        running = True
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP and self.model.player1.jumpCount < 3:
                    self.model.player1.jump()
                    self.model.player1.jumpCount +=1
                if self.model.playernum == 2 and event.key == pygame.K_w and self.model.player2.jumpCount < 3:
                    self.model.player2.jump()
                    self.model.player2.jumpCount +=1
        return running

    def handleHeldKeys(self):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_RIGHT]: 
            m.player1.moveForward()
        elif self.keys[pygame.K_LEFT]:
            m.player1.moveBackward()

        if self.model.playernum == 2:
            if self.keys[pygame.K_d]: 
                m.player2.moveForward()
            elif self.keys[pygame.K_a]:
                m.player2.moveBackward()

class Coins(Sprite):
    def __init__(self, x, y, pictures=["Pictures/Coin1.png","Pictures/Coin2.png","Pictures/Coin3.png","Pictures/Coin4.png","Pictures/Coin5.png","Pictures/Coin6.png","Pictures/Coin7.png","Pictures/Coin8.png"]):
        Sprite.__init__(self)
        self.imagecounter = 0
        self.pictures=pictures
        self.image     =pygame.image.load(pictures[0])
        self.rect      =self.image.get_rect()
        self.mask      =pygame.mask.from_surface(self.image)#not necessary right now, but for later

        self.x = x
        self.y = y
        self.rect.left =x
        self.rect.top  =y
    def update(self):
        self.imagecounter +=1
        if self.imagecounter > 7:
            self.imagecounter = 0
        self.image     = pygame.image.load(self.pictures[self.imagecounter])
        self.rect      = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top  = self.y


class Block(Sprite):
    def __init__(self,x,y,picture = "Pictures/CobbleStoneBlock.png"):
        Sprite.__init__(self)

        self.image     = pygame.image.load(picture)
        self.rect      = self.image.get_rect()
        self.mask      = pygame.mask.from_surface(self.image)
        
        self.rect.left = x
        self.rect.top  = y

class Button(Sprite):
    def __init__(self,x,y,function,picture = "Pictures/CobbleStoneBlock.png"):
        Sprite.__init__(self)

        self.image       = pygame.image.load(picture)
        self.rect        = self.image.get_rect()
        self.mask        = pygame.mask.from_surface(self.image)
        self.function    = function
        self.rect.center = (x,y)

class Player(Sprite):
    """docstring for Player"""
    def __init__(self, x,y, playernum,picture = "Pictures/testSprite.png"):
        Sprite.__init__(self)

        if playernum == 1:
            self.image = pygame.image.load(picture)
            self.rect  = self.image.get_rect()
            self.mask  = pygame.mask.from_surface(self.image)
        else:
            self.image = pygame.image.load(picture)
            self.image = transform.flip(self.image,True,False)
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

        self.jumpCount        = 0
        self.terminalVelocity = 5
        self.score            = 0


    def moveForward(self):
        if self.onGround:
            self.vx = 5
    def moveBackward(self):
        if self.onGround:
            self.vx = -5
    def jump(self):
        self.vy = -10
    def setFriction(self):
        if int(self.vx) != 0:
            self.ff = -abs(self.vx)/self.vx*self.mu*abs(self.fn)
        else:
            self.ff = 0
    def setGravity(self):
        self.fg =  .5*self.mass
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
            self.vx = -3-.2*abs(self.vx)
        if self.hittingWallLeft:
            self.fn = 1
            self.vx = 3+.2*abs(self.vx)
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

map_options = ["empty","Coins","block"]

pygame.init()
clock = Clock()
myfont = pygame.font.SysFont("Liberation Mono",35,True, False)
screen = pygame.display.set_mode((1600,900),pygame.FULLSCREEN)
info = pygame.display.Info()
size = (info.current_w, info.current_h)
m = Model(screen)
v = View(screen, m)
c = Controller(m)
starting = True
running  = False
new_room = True

while starting:
    v.displayStartScreen()
    starting = c.checkPlayerSelection()
    if starting is "Quit":
        running = False
    elif not starting:
        running = True
    pygame.display.update()

if running:
    m.initGame()
    m.buttons.remove(m.buttons.sprites())
    m.update()
    for player in m.players.sprites():
        player.setGravity()

while running:
    if new_room:
        m.createMap()
        m.drawMap()
        new_room = False

    for player in m.players.sprites():
        m.checkPlayerBlockCollisions(player, m.blocks)
        m.checkPlayerCoinsCollisions(player, m.Coins)                

        player.setNormalForce()
        player.setFriction()
    
        if player.onGround:
            player.jumpCount = 0

    c.handleHeldKeys()
    running = c.handleOneTimeKeys()

    m.update()
   
    for player in m.players.sprites():
        player.lastx  = player.x
        player.lasty  = player.y
        player.lastVx = player.vx
        player.lastVy = player.vy
        player.lastFx = player.fx
        player.lastFy = player.fy

    v.update()

    if len(m.Coins.sprites())==0:
        running=False

    clock.tick(60)