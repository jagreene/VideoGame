from pygame import *
from pygame.sprite import *
from pygame.time import *
from pygame.locals import *
import math
import random



class Model:
    """I Am a model, I set the main space of interaction, intermediary between view and controller. Holds sprte groups including "buttons", "Coins", "Players" and "Blocks" 
        """

    def __init__(self,screen):
        """Sets required attributes of model and initalizes buttons for start screen """
        self.screen = screen
        self.buttons = Group(Button(700,450,"1P","Pictures/1P.png"),Button(900,450,"2P","Pictures/2P.png"))
        self.time = 90
        self.endTime = 5

    def initGame(self):
        """ sets required attributes for actual game in which person interacts with game"""
        self.map = {}
        self.blocks = Group()
        self.Coins =Group()
        self.players = Group()
        self.player1 = Player(1525,75,2)
        self.players.add(self.player1)
        if self.playernum == 2:
            self.player2 = Player(75,825,1)
            self.players.add(self.player2)
        else:
            self.player2 = False

    def createMap(self):
        """ segments screen into rows and coloums with the dimensions of the blocks, stores, goes through and randomly assigns each index of the screen some string which coralates to a block, coin, or empty space, 
        Stores the position of box and coins in a dictionary in a tuple representing the position of the object"""
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
        """takes the dictionary in createMap and uses that information to physically place objects on the screen """
        for position, contain in self.map.items():
            if contain is "block":
                self.blocks.add(Block(position[1]*50,position[0]*50))
            elif contain is "Coins":
                self.Coins.add(Coins(position[1]*50+10,position[0]*50+10))
        
    def update(self):
        """ updates the location of the blocks, players, and coins"""
        self.blocks.update()
        self.players.update()
        self.Coins.update()

    def checkPlayerBlockCollisions(self,player,blocks):
        """Uses sprite collide to detect collisions and then uses the relative position of block and player to determine the direction of the collision"""

        for collision in spritecollide(player, blocks, False):

            if collision.rect.height/2 - player.terminalVelocity -1 <= collision.rect.centery-player.rect.bottom < collision.rect.height/2:
                player.onGround = True
            elif collision.rect.height/2 - 6 <= abs(player.rect.top - collision.rect.centery) < collision.rect.height/2:
                player.hittingCeilling = True
            elif player.rect.centerx - collision.rect.centerx < 0:
                player.hittingWallRight = True
            else:
                player.hittingWallLeft = True

    def checkPlayerCoinsCollisions(self, player, Coins):
        """uses sprite collide to detect collisions between the player sprite and the coin sprite, this then destroys the coins from the screen and then adds to the players score."""
        for collision in spritecollide(player, Coins, True):
            player.score += 1


class View():
    """Handles displaying game objects to the screen"""

    def __init__(self,screen, model):
        self.screen = screen
        self.screen.fill(blackColor)
        self.model = model


    def displayStartScreen(self):
        """Displays the opening screen with title (which is amazing) and the two buttons (which are also works of art)"""
        self.model.buttons.draw(self.screen)
        Title=myfont.render("THE WORLD ENDS WITH COINS", 1, random.choice(all_color))
        self.screen.blit(Title, (550, 300))
        pygame.display.update()


    def displayEndingScreen(self):
        """Displays the closing screen and which palyer won"""
        self.screen.fill(blackColor)

        Title = myfont.render("Player %s Wins"%(self.model.winner), 1, random.choice(all_color))
        self.screen.blit(Title, (670, 300))
        pygame.display.update()

    def update(self):
        """displays the buttons, players, blocks, and coins. Also updates the two players scores and displays the timer, which counts down """
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
        timerLimit = myfont.render("Time Limit:" +str(self.model.time), 1, whiteColor)
        self.screen.blit(timerLimit, (700, 15))   
        pygame.display.update()
        
class Controller():
    """reads the button presses and causes the appropriate reactions (i.e press of left arrow casues player to move left) """
    def __init__(self,model):
        self.model = model

    def checkPlayerSelection(self):
        """Checks to see if user has clicked on one of the two game modes (buttons) then sets the appropriate attributes  """
        starting = True
        for button in self.model.buttons.sprites():
            if button.rect.collidepoint(mouse.get_pos()) and mouse.get_pressed()[0]:
                if button.function == "1P":
                    self.model.playernum = 1
                    starting = False
                else:
                    self.model.playernum = 2
                    starting = False


        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Quit"

        return starting


    def handleOneTimeKeys(self):
        """Sets quit button and jump keys"""
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
        """sets movement keys of both players"""
        self.keys = pygame.key.get_pressed()

        m.player1.runningForward = False
        m.player1.runningBackward = False

        if self.keys[pygame.K_RIGHT]: 
            if m.player1.onGround:
                m.player1.moveForward()
                m.player1.runningForward = True
            self.flip = True
        elif self.keys[pygame.K_LEFT]:
            if m.player1.onGround:
                m.player1.moveBackward()
                m.player1.runningBackward = True
            self.flip = False


        if self.model.playernum == 2:
            m.player2.runningForward = False
            m.player2.runningBackward = False
            if self.keys[pygame.K_d]:
                if m.player2.onGround:
                    m.player2.moveForward()
                    m.player2.runningForward = True
                self.flip = False
            elif self.keys[pygame.K_a]:
                if m.player2.onGround:
                    m.player2.moveBackward()
                    m.player2.runningBackward= True
                self.flip = True

class Coins(Sprite):
    """ Creates and animates the coin sprite"""
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
        """Cycles through each image,in effect animating the sprites of the coins"""
        self.imagecounter +=1
        if self.imagecounter > 7:
            self.imagecounter = 0
        self.image     = pygame.image.load(self.pictures[self.imagecounter])
        self.rect      = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top  = self.y


class Block(Sprite):
    """Sets the sprites of the blocks"""
    def __init__(self,x,y,picture = "Pictures/CobbleStoneBlock.png"):
        Sprite.__init__(self)

        self.image     = pygame.image.load(picture)
        self.rect      = self.image.get_rect()
        self.mask      = pygame.mask.from_surface(self.image)
        
        self.rect.left = x
        self.rect.top  = y

class Button(Sprite):
    """ Creates the buttons sprites"""
    def __init__(self,x,y,function,picture = "Pictures/1P.png"):
        Sprite.__init__(self)

        self.image       = pygame.image.load(picture)
        self.rect        = self.image.get_rect()
        self.mask        = pygame.mask.from_surface(self.image)
        self.function    = function
        self.rect.center = (x,y)

class Player(Sprite):
    """Creates and animates the player sprite"""
    def __init__(self, x,y, playernum,pictures = ["Pictures/run1.png", "Pictures/run2.png","Pictures/Run3.png", "Pictures/Run4.png", "Pictures/Run5.png", "Pictures/Run6.png", "Pictures/Run7.png", "Pictures/Run8.png" ]):
        """Creates the sprite"""
        Sprite.__init__(self)

        self.pictures=pictures

        if playernum == 1:
            self.image = pygame.image.load(pictures[0])
            self.rect  = self.image.get_rect()
            self.mask  = pygame.mask.from_surface(self.image)
            self.flip  = False
        else:
            self.image = pygame.image.load(pictures[0])
            self.image = transform.flip(self.image,True,False)
            self.rect  = self.image.get_rect()
            self.mask  = pygame.mask.from_surface(self.image)
            self.flip  = True


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

        self.imagecounter=0
        self.runningForward = False
        self.runningBackward = False

    def moveForward(self):
        """creates velocity while moving forward"""
        if self.onGround:
            self.vx = 4
    def moveBackward(self):
        """creates the velocity while moving backwards """
        if self.onGround:
            self.vx = -4
    def jump(self):
        """creates the velocity in pixels for jumping """
        self.vy = -9
    def setFriction(self):
        """creates the decceleration from blocks on friction """
        if int(self.vx) != 0:
            self.ff = -abs(self.vx)/self.vx*self.mu*abs(self.fn)
        else:
            self.ff = 0
    def setGravity(self):
        """Sets the gravity force on the player sprite """
        self.fg =  .5*self.mass
    def setNormalForce(self):
        """sets normal force on the player sprite"""
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
            self.vx = -.1-abs(self.vx)
        if self.hittingWallLeft:
            self.fn = 1
            self.vx = .1+1*abs(self.vx)
        elif (not self.onGround) and (not self.hittingCeilling) and (not self.hittingWallLeft) and (not self.hittingWallRight):
            self.fn = 0

    def update(self):
        """updates all the forces on the players"""
        if self.runningForward or self.runningBackward:
            self.imagecounter +=1
            if self.imagecounter > 7:
                self.imagecounter = 0
        else: 
            imagecounter=0
        self.image     = pygame.image.load(self.pictures[self.imagecounter])
        if self.flip:
            self.image = transform.flip(self.image,True,False)
        self.rect      = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top  = self.y

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
              self.flip = not self.flip

        self.rect.center = ((int(self.x)),int(self.y))

        

#Colors!!!!!
whiteColor = pygame.Color(255,255,255)
redColor   = pygame.Color(255,0,0)
blueColor  = pygame.Color(0,0,255)
greenColor = pygame.Color(0,255,0)
blackColor = pygame.Color(0,0,0)
all_color  = [whiteColor, redColor, blueColor, greenColor, blackColor]

map_options = ["empty","Coins","block"]

pygame.init()#initalize pygame window
clock= Clock()#creates clock used in frame rate (farther down)

"""Creates Timer events"""
pygame.time.set_timer(25, 7000)
pygame.time.set_timer(26, 1000)
pygame.time.set_timer(27, 5000)

myfont = pygame.font.SysFont("Liberation Mono",35,True, False)#Creates font object for displaying text to screen
screen = pygame.display.set_mode((1600,900),pygame.FULLSCREEN)# Sets the window of pygame
info   = pygame.display.Info()#grabs the current displays information to get size of screen
size   = (info.current_w, info.current_h)#stores size of screen, allows us to divide screen to create rows and columns

m = Model(screen)#creates model 
v = View(screen, m)#creates view
c = Controller(m)# creates controller
starting = True#tells game to enter start screen loop
running  = False#tells game to not enter running game loop
ending   = False#tells game to not enter ending game loop
new_room = True#creates new room, tells game to create new room

while starting:#Starting game loop
    v.displayStartScreen()
    starting = c.checkPlayerSelection()
    if starting is "Quit":
        running = False
    elif not starting:
        running = True
    pygame.display.update()

if running:#initalizes game portion
    m.initGame()
    m.buttons.remove(m.buttons.sprites())
    m.update()
    for player in m.players.sprites():
        player.setGravity()

while running:#enters game loop
    if new_room:#creates new room
        m.createMap()
        m.drawMap()
        new_room = False

    for player in m.players.sprites():#checks collisions for every block, coin, and player
        m.checkPlayerBlockCollisions(player, m.blocks)
        m.checkPlayerCoinsCollisions(player, m.Coins)                

    
        if player.onGround:#resets jump counter
            player.jumpCount = 0

    c.handleHeldKeys()

    for player in m.players.sprites():#sets appropriate forces
        player.setNormalForce()
        player.setFriction()

    running = c.handleOneTimeKeys()

    m.update()
   
    for player in m.players.sprites():# sets previous state variables
        player.lastx  = player.x
        player.lasty  = player.y
        player.lastVx = player.vx
        player.lastVy = player.vy
        player.lastFx = player.fx
        player.lastFy = player.fy

    v.update()#updates screen

    if len(m.Coins.sprites())==0:#ends game if all coins are grabbed
        running = False
        ending  = True

    if pygame.event.get(26):# decrements the timer and handles ending game when timer equals zero
        m.time -=1
        if m.time==0:
            running = False
            ending  = True



    clock.tick(60)#sets max frame rate

if m.playernum == 2:#calculates the winner
    if m.player1.score - m.player2.score > 0:
        m.winner = "1"
    elif m.player1.score - m.player2.score < 0:
        m.winner = "2"
    else:
        m.winner = "Nobody"
else:
    m.winner = "1"

while ending:     #displays ending screen
    v.displayEndingScreen()

    if pygame.event.get(26):
        m.endTime -= 1
        if m.endTime == 0:
            ending = False