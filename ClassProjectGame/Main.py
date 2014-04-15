import pygame, sys
from classes import *
from process import process


pygame.init()
SCREENWIDTH,SCREENHEIGHT = 640, 322
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32) #Initialize a window or screen for display. Sets the size of the screen (640, 360), the flags 0, and the color 32.
clock = pygame.time.Clock() # create an object to help track time
FPS = 24 #Frames Per Second
total_frames = 0 #keeps track of all the frames ever created in the game

background = pygame.image.load("images/court1.png")
player = Player(0, SCREENHEIGHT - 40, "images/player1.png")


#-----------------Main Program Loop--------------------
while True:
	#Processing
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

	clock.tick(FPS)#Set the frames Per Second and you can tell how many frames in a second/ 5 sec/ every minute
