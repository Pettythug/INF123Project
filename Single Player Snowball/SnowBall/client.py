from network import Handler, poll
import sys, math, random, os
from random import randint

from threading import Thread
from time import sleep
import pygame

from pygame.locals import KEYDOWN,KEYUP, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE

hit = False


class BaseClass(pygame.sprite.Sprite):

    allsprites = pygame.sprite.Group()
    def __init__(self, x, y, image_string):
        
        pygame.sprite.Sprite.__init__(self)
        BaseClass.allsprites.add(self)

        self.image = pygame.image.load(image_string)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def destroy(self):
        self.allsprites.remove(self)
        del self
class Player(BaseClass):

    List = pygame.sprite.Group()
    going_right = True

    def __init__(self, x, y, image_string):
        
        BaseClass.__init__(self, x, y, image_string)
        Player.List.add(self)
    def destroy(self):
        Player.List.remove(self)
        super(Player,self).destroy()
class Enemies(BaseClass):
    List = pygame.sprite.Group()
    going_right = True
    def __init__(self, x, y, image_string):
        BaseClass.__init__(self, x, y, image_string)
        Enemies.List.add(self)
    def destroy(self):
        Enemies.List.remove(self)
        super(Enemies,self).destroy()

def enemy_count(count):
    while count>len(Enemies.List)+1:
        Enemies(-100,-100,"images/enemie1.png")
    if count<len(Enemies.List)+1:
        for i,enemy in enumerate(Enemies.List):
            if i<(len(Enemies.List)+1-count):
                enemy.destroy()


def show_snowballs(snowballs):
    while len(snowballs)>len(Snowballs.List):
        Snowballs(-100,-100,"images/projectiles/snowball1.png")
    if len(snowballs)<len(Snowballs.List):
        for i,snowball in enumerate(Snowballs.List):
            if i<(len(Snowballs.List)-len(snowballs)):
                snowball.destroy()
    for i,snowball in enumerate(Snowballs.List):
        snowball.rect.x=snowballs[i][0]
        snowball.rect.y=snowballs[i][1]


class Snowballs(pygame.sprite.Sprite):
    List = pygame.sprite.Group()
    
    def __init__(self, x, y, image_string):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        Snowballs.List.add(self)
        
    def destroy(self):
        Snowballs.List.remove(self)
        del self
"""
    
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
"""
def collisions():

    

    for enemies in Enemies.List:

        projectiles = pygame.sprite.spritecollide(enemies, Snowballs.List, True) # when a player projectile collides with a enemy it returns the projectiles in the projectiles list

        for projectile in projectiles:


            enemies.health = 0
        
            enemies.image = image = pygame.image.load("images/enemie1snow.png") # regular snowball
            
            
            projectile.rect.x = 2 * -projectile.rect.width
            projectile.destroy()
            
            global hit 
            hit = True
            enemies.destroy()
            
            

myname = raw_input('What is your name? ')
#myname="Lucy"


        
player = Player(-100, -100, "images/player1.png")
host, port = 'localhost', 8888
class Client(Handler):
    
    def on_close(self):
        client.do_send({'speak': myname, 'txt': "quit"})
        print "** Disconnected from server **"
        os._exit(0)
    
    def on_msg(self, msg):
        #print msg
        if msg[0]=="userjoin":
            enemy_count(msg[1])
        elif msg[0]=="userleave":
            enemy_count(msg[1])
        elif msg[0]=="positions:":
            enemy_count(msg[3])
            enemypositions=[pos for i,pos in enumerate(msg[2]) if i != msg[1]]
            for i,enemy in enumerate(Enemies.List):
                enemy.rect.x=enemypositions[i][0]
                enemy.rect.y=enemypositions[i][1]
                if enemy.going_right!=enemypositions[i][2]:
                    enemy.going_right=enemypositions[i][2]
                    if enemy.going_right:
                        if hit:
                            enemy.image = pygame.image.load("images/enemie1snow.png")
                        else:
                            enemy.image = pygame.image.load("images/enemie1.png")
                    else:
                        if hit:
                            enemy.image = pygame.image.load("images/enemie1snow.png")
                        else:
                            enemy.image = pygame.image.load("images/enemie1flip.png")
            player.rect.x=msg[2][msg[1]][0]
            player.rect.y=msg[2][msg[1]][1]
            if player.going_right!=msg[2][msg[1]][2]:
                player.going_right=msg[2][msg[1]][2]
                if player.going_right:
                    player.image = pygame.image.load("images/player1.png")
                else:
                    player.image = pygame.image.load("images/player1flip.png")
            show_snowballs(msg[4])
        elif msg[0]=="hit":
            player.image = pygame.image.load("images/player1snow.png")
        
client = Client(host, port)
client.do_send({'join': myname})



##########################################   Main   ##################################################

pygame.init()
# screen = pygame.display.set_mode((400, 300))     
SCREENWIDTH,SCREENHEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32) #Initialize a window or screen for display. Sets the size of the screen (640, 360), the flags 0, and the color 32.
clock = pygame.time.Clock() # create an object to help track time
FPS = 24 #Frames Per Second
total_frames = 0 #keeps track of all the frames ever created in the game

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))







while 1:
    poll()
    sleep(.02)
    """
    process(player, FPS, total_frames)
    #LOGIC
    player.motion(SCREENWIDTH, SCREENHEIGHT)
    Enemies.update_all(SCREENWIDTH, SCREENHEIGHT)
    PlayerProjectile.movement()
    """
    total_frames += 1
    #LOGIC
    #DRAW
    screen.blit(background, (0,0) )    
    BaseClass.allsprites.draw(screen)
    Snowballs.List.draw(screen)
    pygame.display.flip() #Update the full display Surface to the screen
    #DRAW
    clock.tick(FPS)
    collisions()
    if hit:
        client.do_send({'hit': myname, 'txt': "hit"})
        
    cmd = None
    for event in pygame.event.get():  # inputs
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                client.do_close()
            elif key == K_UP:
                client.do_send({'speak': myname, 'txt': "Up"})
            elif key == K_DOWN:
                client.do_send({'speak': myname, 'txt': "Down"})
            elif key == K_LEFT:
                client.do_send({'speak': myname, 'txt': "Left"})
            elif key == K_RIGHT:
                client.do_send({'speak': myname, 'txt': "Right"})
            elif key == K_SPACE:
                client.do_send({'speak': myname, 'txt': "Spacebar"})
        elif event.type == KEYUP:
            key = event.key
            if key == K_UP:
                client.do_send({'speak': myname, 'txt': "NoUp"})
            elif key == K_DOWN:
                client.do_send({'speak': myname, 'txt': "NoDown"})
            elif key == K_LEFT:
                client.do_send({'speak': myname, 'txt': "NoLeft"})
            elif key == K_RIGHT:
                client.do_send({'speak': myname, 'txt': "NoRight"})
    
