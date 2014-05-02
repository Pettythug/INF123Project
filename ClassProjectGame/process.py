import pygame, sys, classes, random

def process(player, FPS, total_frames):

	#processing
	for event in pygame.event.get(): #This is a list of all possible that can happen within the pygame framework. Loops through them
		if event.type == pygame.QUIT:#if the type of event is that the program wants to quit,
			
			pygame.quit()#closes pygame
			sys.exit()#system closes properly and allows the program to terminate

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_e:
				classes.PlayerProjectile.freeze = not classes.PlayerProjectile.freeze


	keys = pygame.key.get_pressed()

	#Sets the a and d keys to move the image a moves left
	#d moves the image right when w is pressed it goes up and when 
	#x is pressed the image moves down
	if keys[pygame.K_RIGHT]:
		classes.Player.going_right = True
		player.image = pygame.image.load("images/player1.png")
		player.velx = 5

	elif keys[pygame.K_LEFT]:
		classes.Player.going_right = False
		player.image = pygame.image.load("images/player1flip.png")
		player.velx = -5
	else:
		player.velx = 0	

	if keys[pygame.K_UP]:
		player.vely = -5

	elif keys[pygame.K_DOWN]:
		player.vely = 5

	else:
		player.vely = 0

	


	if keys[pygame.K_SPACE]:


		def direction():
			if classes.Player.going_right:
				p.velx = 8
			else:
				p.image = pygame.transform.flip(p.image, True, False)#flips the image when shooting the other direction
				p.velx = -8
		if (classes.PlayerProjectile.freeze):
			p = classes.PlayerProjectile(player.rect.x, player.rect.y, True, "images/projectiles/snowball1.png")
			direction()
		else:
			p = classes.PlayerProjectile(player.rect.x, player.rect.y, False, "images/projectiles/snowballFace.png")
			direction()

	
	#classes.Enemies(640 - 40, 130, 26, 40, "images/enemie1flip.png")
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
		classes.Enemies(x, 130, "images/enemie1.png")

def collisions():

	

	for enemies in classes.Enemies.List:

		projectiles = pygame.sprite.spritecollide(enemies, classes.PlayerProjectile.List, True) # when a player projectile collides with a enemy it returns the projectiles in the projectiles list

		for projectile in projectiles:


			enemies.health = 0
		
			enemies.image = image = pygame.image.load("images/enemie1snow.png") # regular snowball

			
			projectile.rect.x = 2 * -projectile.rect.width
			projectile.destroy()

















































