from pygame import *
from pygame.sprite import *
from pygame.locals import *
import time
import random



class Model:
    def __init__(self,screen):
        self.screen = screen
        self.map = {}
        self.blocks = Group()

    def createMap(self):
        map = {}
        for rows in xrange(0,size[1]/50):
            for columns in xrange(0,size[0]/50):
                if rows == (size[1]/50)-1 or rows == 0:
                    map.update({(rows,columns):"block"})
                elif(rows%5 == 0):
                    map.update({(rows,columns):random.choice(map_options)})
                else:
                    map.update({(rows,columns):"empty"})

        self.map = map

    def drawMap(self):
        blocks = Group()
        for position, contain in self.map.items():
            if contain is "block":
                blocks.add(Block(position[1]*50,position[0]*50,"Pictures/CobbleStoneBlock.png"))

        self.blocks.add(blocks.sprites())

    def draw(self):
        self.screen.fill(whiteColor)
        self.blocks.update
        self.blocks.draw(self.screen)

class Block(Sprite):
    def __init__(self,x,y,picture):
        Sprite.__init__(self)
        self.image  = pygame.image.load(picture)
        self.rect   = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

whiteColor = pygame.Color(255,255,255)
redColor   = pygame.Color(255,0,0)
blueColor  = pygame.Color(0,0,255)
greenColor = pygame.Color(0,255,0)

map_options = ["empty","block"]

pygame.init()

size = (1600,900)
screen = pygame.display.set_mode(size)
m = Model(screen)

running  = True
new_room = True
while running:
    if new_room:
        m.createMap()
        m.drawMap()
        new_room = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    m.draw()
    pygame.display.update()
    time.sleep(.001)
