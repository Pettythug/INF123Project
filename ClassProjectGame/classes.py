

import pygame, math
from random import randint
allsprites = pygame.sprite.Group()

class BaseClass(pygame.sprite.Sprite):

	def __init__(self, x, y, image_string):
		
		pygame.sprite.Sprite.__init__(self)
		allsprites.add(self)

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

		#Stops the image from leaving the screen but has a little bounce back when 
		#screen edge is reached
		# if  self.rect.x < 0:
		# 	self.rect.x = 0
		# elif self.rect.x + self.rect.width > SCREENWIDTH:
		# 	self.rect.x = SCREENWIDTH - self.rect.width
		# if self.rect.y < 0:
		# 	self.rect.y = 0 
		# elif self.rect.y + self.rect.height > SCREENHEIGHT:
		# 	self.rect.y = SCREENHEIGHT - self.rect.height

		self.rect.x += self.velx
		self.rect.y += self.vely

	 	self._jump(SCREENHEIGHT)

	def _jump(self, SCREENHEIGHT):
	 	
		max_jump =  75 	# how many pixels down from the top the 
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
					enemies.rect.y += enemies.vely # if true it drops down
			else:
				enemies.enemies(SCREENWIDTH) # if false it continues to move.

			
			# if enemies.health <= 0: #destorys the enemie if the health is less than or eaqual to zero
			# 	enemies.destroy(Enemies)

	def enemies(self, SCREENWIDTH):
		#Keeps the enemy from being dropped outside the screen
		if self.rect.x + self.rect.width > SCREENWIDTH or self.rect.x < 0:
			self.image = pygame.transform.flip(self.image, True, False)
			self.velx = -self.velx

		self.rect.x += self.velx

		#Sin couve is -- (a * sin( bx + c ) + y)

		self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + 140

	# @staticmethod
	# def movement(SCREENWIDTH):
	# 	for enemies in Enemies.List:
	# 		enemies.enemies(SCREENWIDTH)

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