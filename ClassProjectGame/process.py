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
	if keys[pygame.K_d]:
		classes.Player.going_right = True
		player.image = pygame.image.load("images/player1.png")
		player.velx = 5

	elif keys[pygame.K_a]:
		classes.Player.going_right = False
		player.image = pygame.image.load("images/player1flip.png")
		player.velx = -5
	else:
		player.velx = 0	

	if keys[pygame.K_w]:
		player.vely = -5

	elif keys[pygame.K_x]:
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

	#Freeze enemies
	#widthpx projectiles


	#pygame.sprite.groupcollide(G1, G2, dokill, dokill) # this takes the first group(G1) and second group(G2) and when they collide it asks if you want to remove the first one (dokill) and do you want to remove the second one (dokill). 
	# for enemies in classes.Enemies.List:
	# # 	enemies_proj = pygame.sprite.spritecollide(enemies, classes.PlayerProjectile.List, True)	
	# # 	if len(enemies_proj) > 0:
	# # 		for hit in enemies_proj:
	# # 			enemies.health -= enemies.half_health

	# 	if pygame.sprite.spritecollide(enemies, classes.PlayerProjectile.List, False):

	# 		if classes.PlayerProjectile.freeze:
	# 			enemies.health -= enemies.half_health
	# 		else:
	# 			enemies.velx = 0
	# 			# enemies.image = "some image" put something here if I find a good frozen pic for the enemie

	# for proj in classes.PlayerProjectile.List:

	# 	if pygame.sprite.spritecollide(proj, classes.Enemies.List, False):

	# 		proj.rect.x = 2 * -proj.rect.width
	# 		proj.destroy()

	for enemies in classes.Enemies.List:

		projectiles = pygame.sprite.spritecollide(enemies, classes.PlayerProjectile.List, True) # when a player projectile collides with a enemy it returns the projectiles in the projectiles list

		for projectile in projectiles:


			enemies.health = 0
		
			enemies.image = image = pygame.image.load("images/snowman3.png") # regular snowball

			# else:

			# 	if enemies.velx > 0: # is dead
			# 		enemies.velx = 0 # enemies is now paralysed
			# 		enemies.image = pygame.image.load("images/snowman3.png") # freeze snowball
			# 	elif enemies.velx < 0:
			# 		enemies.image = pygame.image.load("images/snowman3.png")
			# 		enemies.image = pygame.transform.flip(enemies.image, True, False)

			projectile.rect.x = 2 * -projectile.rect.width
			projectile.destroy()








































































































