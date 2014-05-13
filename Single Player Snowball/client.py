from network import Handler, poll
import sys, math, random
from random import randint

from threading import Thread
from time import sleep
import pygame

from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE
class BaseClass(pygame.sprite.Sprite):

    allsprites = pygame.sprite.Group()
    def __init__(self, x, y, image_string):
        
        pygame.sprite.Sprite.__init__(self)
        BaseClass.allsprites.add(self)

        self.image = pygame.image.load(image_string)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.rect.height


    def destroy(self, ClassName):
        
        ClassName.List.remove(self)
        allsprites.remove(self)
        del self

class Player(BaseClass):

    List = pygame.sprite.Group()
    going_right = True
    keys_pressed=[False, False, False, False]

    def __init__(self, x, y, image_string):
        
        BaseClass.__init__(self, x, y, image_string)
        Player.List.add(self)
        self.velx, self.vely = 0, 5 #The image will move 5 pixels every frame refresh
        self.jumping, self.go_down = False, False #jumping needs to be true if image is going up or down and 
        # go_down is for if the image has hit the max_jump pixel limit set
        

    def motion(self, SCREENWIDTH, SCREENHEIGHT):

        #Stops the image from leaving the screen
        #There is a little bounce back so this keeps that from happening
        #by checking to see where it is and where it will be before 
        #the image gets to the wall
        predicted_locationx = self.rect.x + self.velx
        predicted_locationy = self.rect.y + self.vely

        if  predicted_locationx < 0:
            self.velx = 0
        elif predicted_locationx + self.rect.width > SCREENWIDTH:
            self.velx = 0
        if predicted_locationy < 0:
            self.vely = 0 
        elif predicted_locationy + self.rect.height > SCREENHEIGHT:
            self.vely = 0 

        
        self.rect.x += self.velx
        self.rect.y += self.vely

        self._jump(SCREENHEIGHT)

    def _jump(self, SCREENHEIGHT):
         
        max_jump =  75     # how many pixels down from the top the 
                        # max jump is the height the image can jump to

        if self.jumping:

            if self.rect.y < max_jump:
                self.go_down = True # our cue to start going down

            if self.go_down:
                self.rect.y += self.vely #going down

                predicted_locationy = self.rect.y + self.vely # helps to predict where the player is going to be next. 

                if predicted_locationy + self.rect.height > SCREENHEIGHT: #is it past our screen bottom
                    self.jumping = False #Stops the jumping 
                    self.go_down = False #resets our going down varible

            else:
                self.rect.y -= self.vely # going up till hit max_jump

class Enemies(BaseClass):

    List = pygame.sprite.Group()
    def __init__(self, x, y, image_string):
        BaseClass.__init__(self, x, y, image_string)
        Enemies.List.add(self)
        self.health = 100
        self.half_health = self.health ## / 2.0 will make it so you have to hit the enemy twice in order to kill it
        self.velx, self.vely = randint(1, 4), 2
        self.amplitude, self.period = randint(20, 140), randint(4, 5)/ 100.0

    @staticmethod
    def update_all(SCREENWIDTH, SCREENHEIGHT):
        
        for enemies in Enemies.List:

            if enemies.health <= 0: # if our enemies is dead
                if enemies.rect.y + enemies.rect.height < SCREENHEIGHT: # check to see if it is still above the bottom 
                    enemies.velx = 0 # if true it drops down
            else:
                enemies.enemies(SCREENWIDTH) # if false it continues to move.
        

    def enemies(self, SCREENWIDTH):
        #Keeps the enemy from being dropped outside the screen
        if self.rect.x + self.rect.width > SCREENWIDTH or self.rect.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.velx = -self.velx

        self.rect.x += self.velx

        #Sin couve is -- (a * sin( bx + c ) + y)

        self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + 140

    
class PlayerProjectile(pygame.sprite.Sprite):  #Extended with sprite which contains all the infor we need for a rect and image

    List = pygame.sprite.Group() # allows more functionality

    normal_list = [] #Better to manipulate with than the List

    freeze = True
    
    def __init__(self, x, y, if_this_variable_is_true_then_freeze, image_string):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_string)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.if_this_variable_is_true_then_freeze = if_this_variable_is_true_then_freeze


        try:
            last_element = PlayerProjectile.normal_list[-1]
            difference = abs(self.rect.x - last_element.rect.x)

            if difference < self.rect.width  * 45: #spaces out the projectiles
                return

        except Exception:
            pass


        PlayerProjectile.normal_list.append(self)
        PlayerProjectile.List.add(self)
        self.velx = None
    
    @staticmethod
    def movement():
            #Looping through all the projectiles in the PlayerProjectiles List which is line 123 List = pygame.sprite.Group()
            for projectile in PlayerProjectile.List:
                    projectile.rect.x += projectile.velx


    def destroy(self):
        PlayerProjectile.List.remove(self)
        PlayerProjectile.normal_list.remove(self)
        del self

def process(player, FPS, total_frames):

    #processing
    for event in pygame.event.get(): #This is a list of all possible that can happen within the pygame framework. Loops through them
        if event.type == pygame.QUIT:#if the type of event is that the program wants to quit,
            
            pygame.quit()#closes pygame
            sys.exit()#system closes properly and allows the program to terminate

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                PlayerProjectile.freeze = not PlayerProjectile.freeze


    keys = pygame.key.get_pressed()

    #Sets the a and d keys to move the image a moves left
    #d moves the image right when w is pressed it goes up and when 
    #x is pressed the image moves down
    
    player.velx = 0
    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        Player.going_right = True
        player.image = pygame.image.load("images/player1.png")
        player.velx = 5
        Player.keys_pressed[0]=True
    else:
        if Player.keys_pressed[0]:
            client.do_send({'speak': myname, 'txt': "released Right key"})
        Player.keys_pressed[0]=False
    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        Player.going_right = False
        player.image = pygame.image.load("images/player1flip.png")
        player.velx = -5
        Player.keys_pressed[1]=True
    else:
        if Player.keys_pressed[1]:
            client.do_send({'speak': myname, 'txt': "released Left key"})
        Player.keys_pressed[1]=False

    player.vely = 0
    if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        player.vely = -5
        Player.keys_pressed[2]=True
    else:
        
        if Player.keys_pressed[2]:
            client.do_send({'speak': myname, 'txt': "released Up key"})
        Player.keys_pressed[2]=False

    if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
        player.vely = 5
        Player.keys_pressed[3]=True
    else:
        
        if Player.keys_pressed[3]:
            client.do_send({'speak': myname, 'txt': "released Down key"})
        Player.keys_pressed[3]=False

    if keys[pygame.K_SPACE]:

        def direction():
            if Player.going_right:
                p.velx = 8
            else:
                p.image = pygame.transform.flip(p.image, True, False)#flips the image when shooting the other direction
                p.velx = -8
        if (PlayerProjectile.freeze):
            p = PlayerProjectile(player.rect.x, player.rect.y, True, "images/projectiles/snowball1.png")
            direction()
        else:
            p = PlayerProjectile(player.rect.x, player.rect.y, False, "images/projectiles/snowballFace.png")
            direction()

    
    #Enemies(640 - 40, 130, 26, 40, "images/enemie1flip.png")
    spawn(FPS, total_frames) #calls the enemie so it spawns a new one according to the time.
    collisions()

    #Creates enemies 
def spawn(FPS, total_frames):

    sixty_seconds = FPS * 15 #spaws a new enemy every sixty seconds

    if total_frames % sixty_seconds == 0:

    
        r = random.randint(1,2)
        x = 1
        if r == 2:
            x = 640 - 40
        Enemies(x, 130, "images/enemie1.png")

def collisions():

    

    for enemies in Enemies.List:

        projectiles = pygame.sprite.spritecollide(enemies, PlayerProjectile.List, True) # when a player projectile collides with a enemy it returns the projectiles in the projectiles list

        for projectile in projectiles:


            enemies.health = 0
        
            enemies.image = image = pygame.image.load("images/enemie1snow.png") # regular snowball

            
            projectile.rect.x = 2 * -projectile.rect.width
            projectile.destroy()

#myname = raw_input('What is your name? ')
myname="Lucy"
class Client(Handler):
    
    def on_close(self):
        print "** Disconnected from server **"
        sys.exit(0)
    
    def on_msg(self, msg):
        print msg
        
host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds


##########################################   Main   ##################################################

                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

pygame.init()
# screen = pygame.display.set_mode((400, 300))     
SCREENWIDTH,SCREENHEIGHT = 640, 322
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32) #Initialize a window or screen for display. Sets the size of the screen (640, 360), the flags 0, and the color 32.
clock = pygame.time.Clock() # create an object to help track time
FPS = 24 #Frames Per Second
total_frames = 0 #keeps track of all the frames ever created in the game

background = pygame.image.load("images/white.png")
player = Player(0, SCREENHEIGHT - 40, "images/player1.png")




while 1:
    process(player, FPS, total_frames)
    #LOGIC
    player.motion(SCREENWIDTH, SCREENHEIGHT)
    Enemies.update_all(SCREENWIDTH, SCREENHEIGHT)
    PlayerProjectile.movement()
    total_frames += 1
    #LOGIC
    #DRAW
    screen.blit(background, (0,0) )    
    BaseClass.allsprites.draw(screen)    
    PlayerProjectile.List.draw(screen)    
    pygame.display.flip() #Update the full display Surface to the screen
    #DRAW

    clock.tick(FPS)
    cmd = None
    for event in pygame.event.get():  # inputs
        if event.type == QUIT:
            cmd = 'quit'
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                cmd = 'quit'
                client.do_close()
            elif key == K_UP:
                cmd = 'up'
                client.do_send({'speak': myname, 'txt': "Up key"})
            elif key == K_DOWN:
                cmd = 'down' 
                client.do_send({'speak': myname, 'txt': "Down key"})
            elif key == K_LEFT:
                cmd = 'left'
                client.do_send({'speak': myname, 'txt': "Left key"})
            elif key == K_RIGHT:
                cmd = 'right'
                client.do_send({'speak': myname, 'txt': "Right key"})
            elif key == K_SPACE:
                cmd = 'space'
                client.do_send({'speak': myname, 'txt': "Spacebar key"})
    if cmd:
        print cmd
