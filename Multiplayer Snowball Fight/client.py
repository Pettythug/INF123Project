from network import Client, poll
import sys, math, random
from random import randint

from threading import Thread
from time import sleep
import pygame
import asyncore
from collections import OrderedDict

from pygame.locals import KEYDOWN, KEYUP, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE

# This controls the main loop running
# Set it to false to stop the main while loop
RUNNING = True

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
        BaseClass.allsprites.remove(self)
        del self

class Player(BaseClass):

    List = pygame.sprite.Group()
    going_right = True
    keys_pressed=[False, False, False, False]

    def __init__(self, x, y, image_string, player_id):

        BaseClass.__init__(self, x, y, image_string)
        Player.List.add(self)
        self.player_id = player_id
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

    def destroy(self):
        BaseClass.destroy(self, Player)

class Enemies(BaseClass):

    List = pygame.sprite.Group()
    def __init__(self, id, x, y, velx=None, vely=None, amplitude=None, period=None, health=100, going_right=False, image_string='images/enemie1.png'):
        BaseClass.__init__(self, x, y, image_string)
        Enemies.List.add(self)
        self.health = health
        self.id = id
        self.going_right = going_right

        if not self.going_right:
            self.image = pygame.transform.flip(self.image, True, False)

        self.half_health = self.health ## / 2.0 will make it so you have to hit the enemy twice in order to kill it
        self.velx, self.vely = velx or randint(1, 4), vely  or 2
        self.amplitude, self.period = amplitude or randint(20, 140), period or randint(4, 5)/ 100.0

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
            if self.velx < 0:
                self.going_right = False
            else:
                self.going_right = True

        self.rect.x += self.velx

        #Sin couve is -- (a * sin( bx + c ) + y)

        self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + 140


    def destroy(self):
        BaseClass.destroy(self, Enemies)

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

def process(player, FPS, total_frames, client):

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
        player.going_right = True
        player.image = pygame.image.load("images/player1.png")
        player.velx = 5
        Player.keys_pressed[0]=True
    else:
        if Player.keys_pressed[0]:
            client.do_send({'speak': myname, 'txt': "released Right key"})
        Player.keys_pressed[0]=False
    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        player.going_right = False
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
            if player.going_right:
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

#Creates enemies on client-side 
def spawn(FPS, total_frames):

    sixty_seconds = FPS * 15 #spaws a new enemy every sixty seconds

    if total_frames % sixty_seconds == 0:

        r = random.randint(1,2)
        x = 1
        if r == 2:
            x = 640 - 40
        y = 130

        velx, vely = randint(1, 4), 2
        amplitude, period = randint(20, 140), randint(4, 5)/ 100.0
        #Enemies(x, 130, "images/enemie1.png")
        health = 100
        client.do_send({'spawn': [x, y, velx, vely, amplitude, period, health, True, "images/enemie1.png"]})

def collisions():

    for enemies in Enemies.List:

        projectiles = pygame.sprite.spritecollide(enemies, PlayerProjectile.List, True) # when a player projectile collides with a enemy it returns the projectiles in the projectiles list

        for projectile in projectiles:


            enemies.health = 0

            enemies.image = image = pygame.image.load("images/enemie1snow.png") # regular snowball


            projectile.rect.x = 2 * -projectile.rect.width
            projectile.destroy()

# Use an ordered dict so that the first player we add is at the 0 index
# this is to make sure we don't update the player's position when the player
# is updated, or else we won't be able to move
players = OrderedDict()

myname = raw_input('What is your name? ')

class GameClient(Client):

    def __init__(self, *args, **kwargs):
        Client.__init__(self, *args, **kwargs)

        self.events = {'join': self.do_join,
                       'quit': self.do_quit,
                       'space': self.throw_snowball,
                       'update_players': self.update_players,
                       'move': self.do_move,
                       'input': self.do_change_dir,
                       'create_enemy': self.do_create_enemy}
        self.enemy_ids = []

    def do_join(self, sender_id, data):
        """Adds another player to the game."""
        global players
        players[sender_id] = Player(0, 0, "images/player1.png", sender_id)

        #Spawn the enemies for everyone!
        player = players[sender_id]
        local_player = players.values()[0]
        for enemies in Enemies.List:
            velx, vely = enemies.velx, enemies.vely
            if enemies.health <= 0:
                image = "images/enemie1snow.png"
                velx, vely = 0, 0
            else:
                image = "images/enemie1.png"
            self.do_send({'create_enemy': [enemies.id, enemies.rect.x, enemies.rect.y,
                                            enemies.velx, enemies.vely,
                                            enemies.amplitude, enemies.period,
                                            enemies.health, enemies.going_right,
                                            image]})

    def do_quit(self, sender_id, data):
        """Quits the game."""
        global players
        global RUNNING
        player = players[sender_id]
        local_player = players.values()[0]
        if player == local_player:
            RUNNING = False
            self.do_close()
        player.destroy()


    def throw_snowball(self, sender_id, data):
        """Throws a snowball from the player specified by the sender_id."""
        player = players[sender_id]
        def direction():
            if player.going_right:
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

    def do_create_enemy(self, sender_id, data):
        """Spawns an enemy with the data specified."""
        id, x, y, velx, vely, amp, period, health, going_right, image = data
        if id not in self.enemy_ids:
            Enemies(id, x, y, velx, vely, amp, period, health, going_right, image)
            self.enemy_ids.append(id)


    def update_players(self, sender_id, data):
        """Updates the players. Not used right now because it is slow."""
        global players
        if sender_id in players:
            for player_id, box in data.items():
                try:
                    player = players[player_id]
                    local_player = players.values()[0]
                    if player != local_player:
                        player.rect.x = box[0]
                        player.rect.y = box[1]
                        direction = data[2]
                        if direction == 'right':
                            player.image = pygame.image.load("images/player1.png")
                        elif direction == 'left':
                            player.image = pygame.image.load("images/player1flip.png")
                except KeyError:
                    pass

    def do_change_dir(self, sender_id, data):
        """Changes the direction of the player."""
        global players
        try:
            player = players[sender_id]
            local_player = players.values()[0]
            if player != local_player:
                direction = data
                if direction == 'right':
                    player.image = pygame.image.load("images/player1.png")
                    player.going_right = True
                elif direction == 'left':
                    player.image = pygame.image.load("images/player1flip.png")
                    player.going_right = False
        except KeyError:
            pass


    def do_move(self, sender_id, data):
        """Moves a player to the specified location in data."""
        global players
        try:
            player = players[sender_id]
            local_player = players.values()[0]
            if player != local_player:
                player.rect.x = data[0]
                player.rect.y = data[1]
        except KeyError:
            pass

    def on_close(self):
        """Handles the close event"""
        print "** Disconnected from server **"
        global players

        #if there are no players create a local one for a local game without
        #multiplayer
        if not players:
            sender_id = '1'
            players[sender_id] = Player(0, 0, "images/player1.png", sender_id)

    def on_msg(self, data):
        """Processes the events inside data and dispatches them."""
        sender_id, data = data

        # Process events
        for event in self.events:
            if event in data:
                self.events[event](sender_id, data[event])


host, port = '169.234.123.52', 8888
client = GameClient(host, port, myname) #create a local client
client.do_send({'join': myname})

##########################################   Main   ##################################################

pygame.init()
# screen = pygame.display.set_mode((400, 300))
SCREENWIDTH,SCREENHEIGHT = 640, 322
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32) #Initialize a window or screen for display. Sets the size of the screen (640, 360), the flags 0, and the color 32.
clock = pygame.time.Clock() # create an object to help track time
FPS = 24 #Frames Per Second
total_frames = 0 #keeps track of all the frames ever created in the game

background = pygame.image.load("images/white.png")
player = None

# This makes it cleaner and easier to handle keys
# it eliminates all the if statements and makes
# it easy to add new functionality
keys = {K_UP: 'up',
        K_DOWN: 'down',
        K_LEFT: 'left',
        K_RIGHT: 'right',
        K_SPACE: 'space',
        K_ESCAPE: 'quit'}

# These are the move_events that we detect
move_events = ['up', 'down', 'left', 'right']

# keep track of all the commands executed
cmds = []

while RUNNING:

    # Poll inside the main loop because it's faster
    poll()

    if not player and len(players.values()) > 0:
        player = players.values()[0]
    elif not player:
        clock.tick(FPS)
        continue

    process(player, FPS, total_frames, client)

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
    for event in pygame.event.get():  # inputs
        if event.type == QUIT:
            cmds.append('quit')
            #client.close()
        if event.type == KEYDOWN: # when the key is held down, we still want it to exist
            key = event.key
            try:
                cmds.append(keys[key])
            except KeyError:
                pass
            # we check the space command here because we only want a snowball
            # thrown once, not rapid fire :)
            if 'space' in cmds:
                msg = {'space': [player.rect.x, player.rect.y]}
                client.do_send(msg)
#         elif event.type == KEYUP: # get rid of the command once the key is up
#             key = event.key
#             try:
#                 cmds.remove(keys[key])
#             except KeyError, ValueError:
#                 pass
    for cmd in cmds:
        #Process the commands and send them to all the children
        if cmd in move_events:
            msg = {'input': cmd, 'move': [player.rect.x, player.rect.y]}
            client.do_send(msg)
        elif cmd == 'quit':
            if len(players) == 1:
                RUNNING = False
                client.do_close()
            else:
                msg = {cmd: ''}
                client.do_send(msg)


