from network import Handler, poll
import sys, math, random, os
from random import randint
import operator
from threading import Thread
from time import sleep
import pygame, copy

from pygame.locals import KEYDOWN,KEYUP, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE

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
    dead=False

    def __init__(self, x, y, image_string):
        
        BaseClass.__init__(self, x, y, image_string)
        Player.List.add(self)
    def destroy(self):
        Player.List.remove(self)
        super(Player,self).destroy()
class Enemies(BaseClass):
    List = pygame.sprite.Group()
    going_right = True
    dead=False
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

myname = raw_input('What is your name? ')
#myname="Lucy"


player = Player(-100, -100, "images/player1.png")
host, port = 'localhost', 8888
class Client(Handler):
    scoreboard={}
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
                
                if enemy.dead!=(enemypositions[i][3]>0):
                    if enemypositions[i][3]>0:
                        enemy.dead=True
                        enemy.image = pygame.image.load("images/enemie1snow.png")
                    else:
                        enemy.dead=False
                        enemy.going_right=enemypositions[i][2]
                        if enemy.going_right:
                            enemy.image = pygame.image.load("images/enemie1.png")
                        else:
                            enemy.image = pygame.image.load("images/enemie1flip.png")
                elif enemy.going_right!=enemypositions[i][2]:
                    enemy.going_right=enemypositions[i][2]
                    if enemy.going_right:
                        enemy.image = pygame.image.load("images/enemie1.png")
                    else:
                        enemy.image = pygame.image.load("images/enemie1flip.png")
                
            player.rect.x=msg[2][msg[1]][0]
            player.rect.y=msg[2][msg[1]][1]
            
            if player.dead!=(msg[2][msg[1]][3]>0):
                if msg[2][msg[1]][3]>0:
                    player.dead=True
                    player.image = pygame.image.load("images/player1snow.png")
                else:
                    player.dead=False
                    player.going_right=msg[2][msg[1]][2]
                    if player.going_right:
                        player.image = pygame.image.load("images/player1.png")
                    else:
                        player.image = pygame.image.load("images/player1flip.png")
            elif player.going_right!=msg[2][msg[1]][2]:
                player.going_right=msg[2][msg[1]][2]
                if player.going_right:
                    player.image = pygame.image.load("images/player1.png")
                else:
                    player.image = pygame.image.load("images/player1flip.png")
            show_snowballs(msg[4])
            self.scoreboard=msg[5]
client = Client(host, port)
client.do_send({'join': myname})



##########################################   Main   ##################################################

pygame.init()
# screen = pygame.display.set_mode((400, 300))     
SCREENWIDTH,SCREENHEIGHT = 1200,800
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32) #Initialize a window or screen for display. Sets the size of the screen (640, 360), the flags 0, and the color 32.
clock = pygame.time.Clock() # create an object to help track time
FPS = 24 #Frames Per Second
total_frames = 0 #keeps track of all the frames ever created in the game

background = pygame.Surface(screen.get_size())
background = background.convert()
background = pygame.image.load("images/snow.png")


font = pygame.font.Font(None, 36)
def printScore(background):
    #print client.scoreboard
    background2=copy.copy(background)
    sortedScores=sorted(client.scoreboard.iteritems(), key=operator.itemgetter(1), reverse=True)
    for (i,(username,score)) in enumerate(sortedScores[0:3]):
        text = font.render(username+" - "+str(score), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = SCREENWIDTH/2
        textpos.y=i*36+5
        background2.blit(text,textpos)
    return background2
        
while 1:
    poll()
    sleep(.02)
    total_frames += 1
    #LOGIC
    #DRAW
    screen.blit(printScore(background), (0,0) )    
    BaseClass.allsprites.draw(screen)
    Snowballs.List.draw(screen)
    pygame.display.flip() #Update the full display Surface to the screen
    #DRAW
    clock.tick(FPS)
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