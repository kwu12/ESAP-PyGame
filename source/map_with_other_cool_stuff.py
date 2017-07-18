import pygame, math, sys, random
from pygame.locals import *
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()

class Platform:

	def __init__(self, position, image, fall_through = False):
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		image_rect = self.image.get_rect()
		self.x = position[0]
		self.y = position[1]
		num = image_rect.width / 30
		self.rect = Rect(self.x - image_rect.width / 2, self.y, image_rect.width, image_rect.height)
		boundary_top = Rect(self.rect.left, self.rect.top + num, self.rect.width, num)
		boundary_bottom = Rect(self.rect.left + num, self.rect.bottom - num, self.rect.width - 2 * num, num)
		boundary_left = Rect(self.rect.left, self.rect.top + 2 * num, num, self.rect.height - 2 * num)
		boundary_right = Rect(self.rect.right - num, self.rect.top + 2 * num, num, self.rect.height - 2 * num)
		self.boundaries = [boundary_top, boundary_bottom, boundary_left, boundary_right]
		self.fall_through = fall_through 

	def draw(self):
		screen.blit(self.image, self.rect)
		colors = [(255,255,0), (255,0,0), (0,255,0), (0,0,255)]
		for i in range(len(self.boundaries)):
			pygame.draw.rect(screen, colors[i], self.boundaries[i], 0) #uncomment to see center 


class Map:
	MAP_MASTER = {"Final Destination": ("../resources/Backgrounds/BG_SPACE.png", (Platform((screen.get_width() / 2, screen.get_height() / 2), "../resources/Platforms/Final_Dest.png"),)),
	"Battlefield": ("../resources/Backgrounds/BG_Dark.png", (Platform((screen.get_width() / 2, screen.get_height() / 2), "../resources/Platforms/Battlefield_Bottom.png"),
	Platform((3 * screen.get_width() / 8, 3 * screen.get_height() / 8), "../resources/Platforms/Battlefield_Left.png", fall_through = True), Platform((5 * screen.get_width() / 8, 3 * screen.get_height() / 8), "../resources/Platforms/Battlefield_Right.png", fall_through = True),
	Platform((screen.get_width() / 2, 1 * screen.get_height() / 4), "../resources/Platforms/Battlefield_Top.png", fall_through = True)))}
	def __init__(self, name, background_image = "default"):
		self.name = name
		self.platforms = []
		if background_image == "default":
			background_image = self.MAP_MASTER[name][0]
			self.platforms.extend(self.MAP_MASTER[name][1])
		self.background_image = pygame.image.load(background_image)
		
	def draw(self):
		pygame.display.set_caption(self.name)
		screen.blit(self.background_image, (0,0))
		for plat in self.platforms:
			plat.draw()
		#self.screen

class Ball:
	ACCELERATION = 0.5
	max_forward_speed = 7.8
	MAX_X_SPEED = 5

	IDLE = 0
	RUNNING = 1
	JUMPING = 2
	NEUTRAL_B = 3
	JAB = 4
	ANIM_NAME = ["Idle","Running","Jumping","Neutral_B","Jab"]
	ANIM_INC = [20,30,14,19,18]
	ANIM_LOOP = [False, False, True, False, False]
	ANIM_MOD = [5,4,7,5,6]
	#ACCELERATION = 0.5
	#MAX_FORWARD_SPEED = 1
	MAX_REVERSE_SPEED = -5


	def __init__(self, position, platforms = []):
		#pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.speed = 0
		self.k_up = self.k_down = 0
		self.platforms = platforms
		self.radius = 4
		self.touching_platform = False
		self.velx = 0
		self.jump_ctr = 2
		self.fast_falling = False
		self.accx = 0
		self.anim_mode = self.IDLE
		self.state_mode = self.IDLE
		self.falling = True
		self.direction = "right"
		self.anim_ctr = 0
		self.image = pygame.image.load("../resources/Mario/Mario_" + self.ANIM_NAME[self.IDLE] + "/Mario_"+ self.ANIM_NAME[self.IDLE] +"1.png")
		self.rect = self.get_rect()


	def draw(self):
		#pygame.draw.circle(screen, (255, 0, 0), (int(self.position[0]), int(self.position[1])), self.radius, 0)
		#pygame.draw.rect(screen, (255,255,255), self.rect, 0)

		x,y = self.position
		self.anim_incrementer_no_loop(self.ANIM_INC[self.anim_mode], self.ANIM_LOOP[self.anim_mode])
		self.image = pygame.image.load("../resources/Mario/Mario_" + self.ANIM_NAME[self.anim_mode] + "/Mario_"+ self.ANIM_NAME[self.anim_mode] + str(1+self.anim_ctr//self.ANIM_MOD[self.anim_mode]) + ".png")
		# if(self.falling):
		# 	self.image = pygame.image.load("../resources/Mario/Mario_Jumping/Mario_Jumping5.png")
		# elif(self.anim_mode == self.JUMPING):
		# 	self.anim_incrementer_no_loop(14, True)
		# 	self.image = pygame.image.load("../resources/Mario/Mario_" + ANIM_NAME[anim_mode] + "/Mario_"+ ANIM_NAME[anim_mode] + str(1+self.anim_ctr//7) + ".png")
		# elif self.anim_mode == self.RUNNING:
		# 	self.anim_incrementer(30)
		# 	self.image = pygame.image.load("../resources/Mario/Mario_Running/Mario_Running"+str(1+self.anim_ctr//4)+".png")
		# elif self.anim_mode == self.IDLE:
		# 	self.anim_incrementer(20)
		# 	self.image = pygame.image.load("../resources/Mario/Mario_Idle/Mario_Idle"+str(1+self.anim_ctr//5)+".png")
		
		if(self.direction == "left"):
			self.image = pygame.transform.flip(self.image,True,False)
		#self.rect = self.get_rect()
		screen.blit(self.image, self.position)

	def add_platforms(self, platforms):
		self.platforms.extend(platforms)

	def get_rect(self):
		#return Rect(self.position, (self.radius, self.radius))
		return Rect(self.position, (self.image.get_rect().width, self.image.get_rect().height))

	def jump(self):
		# x, y = self.position
		# if self.jump_ctr == 2:
		# 	#self.move(x, y - 30)
		# 	self.speed = -10
		# 	self.jump_ctr -= 1
		# elif self.jump_ctr == 1:
		# 	self.speed = -8
		# 	self.jump_ctr -= 1

		x, y = self.position
		if self.jump_ctr == 2:
			#self.move(x, y - 30)
			self.speed = -10
			self.jump_ctr -= 1
			self.anim_mode = self.JUMPING
			self.state_mode = self.JUMPING
			self.falling = False
			self.anim_ctr = 0
		elif self.jump_ctr == 1:
			self.speed = -8
			self.jump_ctr -= 1


	def move(self, x, y):
		self.position = (x, y)
		self.rect = self.get_rect()
		if(self.speed>2):
			self.falling = True

	def update(self, deltat):
		# x, y = self.position
		# self.velx *= 0.8
		# self.velx += self.accx

		# x += self.velx
		# y += self.speed
		# #self.acccx = 0
		# if self.velx > abs(self.MAX_X_SPEED) and self.velx < 0:
		# 	self.velx = -self.MAX_X_SPEED
		# elif self.velx > abs(self.MAX_X_SPEED) and self.velx > 0:
		# 	self.velx = self.MAX_X_SPEED

		self.velx *= 0.7
		self.velx += self.accx
		self.move(self.position[0] + self.velx, self.position[1])
		if self.speed > self.max_forward_speed:
			speed = self.max_forward_speed
		if not self.touching_platform:
			self.speed += self.ACCELERATION
		x, y = self.position
		y += self.speed
		self.move(x, y)

		#self.move(x, y)
		if not self.touching_platform and self.fast_falling:
			self.speed += self.ACCELERATION * 2
		elif not self.touching_platform:
			self.speed += self.ACCELERATION
		if self.speed > self.max_forward_speed:
			self.speed = self.max_forward_speed
		self.max_forward_speed = 7.8
		#self.move(x, y)

		# if len(pygame.sprite.spritecollide(self, self.platforms, False)) > 0:
		# print(self.rect.left, self.rect.top)
		# print(self.platforms[0].boundary_rect.left, self.platforms[0].boundary_rect.top)
		
		if y >= 570:
			self.move(screen.get_width() / 2, 0)
			self.speed = 0
			self.velx = 0



		for platform in self.platforms:
			boundary_rect = platform.boundaries[0]
			if self.rect.colliderect(boundary_rect) and self.speed >= 0 and (not self.fast_falling or not platform.fall_through): #and not platform.fall_through: 
				#if self.rect.bottom > boundary_rect.top and self.rect.bottom - boundary_rect.top > 0:
				#print(2)
				self.touching_platform = True
				self.speed = 0 
				self.move(x, boundary_rect.top - self.rect.height + 1)		
				self.jump_ctr = 2	
				# self.speed *= -1
				#self.velx = 0
			if not self.rect.colliderect(boundary_rect) and not platform.fall_through:
				if self.rect.colliderect(platform.boundaries[1]):
					self.speed = 0 
					self.move(x, platform.boundaries[1].bottom + self.rect.height)		
					#self.velx = 0
					self.touching_platform = False
				elif self.rect.colliderect(platform.boundaries[2]):
					#self.speed = 0 
					self.move(platform.boundaries[2].left - self.rect.height, y)		
					self.velx = 0
					self.touching_platform = False
				elif self.rect.colliderect(platform.boundaries[3]):
					#self.speed = 0 
					self.move(platform.boundaries[3].right + self.rect.height, y)		
					self.velx = 0
					self.touching_platform = False
				else:
					self.touching_platform = False
			else:
				self.touching_platform = False
	def anim_incrementer_no_loop(self, max, dont_loop):
		if(self.anim_ctr==max):
			self.state_mode = self.IDLE
		if(self.anim_ctr>max):
			self.anim_ctr = max
		if(self.anim_ctr<max):
			self.anim_ctr+=1
		elif(dont_loop!=True):
			self.anim_ctr = 0

class Projectile(pygame.sprite.Sprite):
	def __init__(self, position, image, direction):
		super().__init__()
		self.position = position
		self.xspeed = 15
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = position 
		self.direction = direction
		self.life_ctr = 0
		
	def update(self):
		self.image = pygame.transform.rotate(self.image, 90)
		screen.blit(self.image, self.rect)
		self.life_ctr += 1
		if(self.life_ctr>45):
			self.kill()
		if shoot == True:
			if self.direction != "right":
				self.rect.x -= self.xspeed
			else:
				self.rect.x += self.xspeed

#460 x 171

plat_image1 = "../resources/Platforms/Battlefield_Top.png"
image1= "../resources/Backgrounds/CastleBG.jpg"
map1 = Map("Battlefield")
#map1 = Map("Final Destination")
#pygame.sprite.spritecollide(, surface_group, False)
ball = Ball((screen.get_width() / 2, 100), map1.platforms)
shoot = False

# while 1:
# 	deltat = clock.tick(30)
# 	for event in pygame.event.get():
# 		if event.type == QUIT:
# 			sys.exit(0)
# 		if not hasattr(event, 'key'): continue
# 		if event.type == KEYDOWN:
# 			if event.key == K_UP and ball.jump_ctr == 1:
# 				ball.jump()
# 			if event.key == K_UP and ball.jump_ctr == 2:
# 				ball.jump()
# 		if event.key == K_ESCAPE:
# 			sys.exit(0)

# 		if pygame.key.get_pressed()[pygame.K_LEFT]:
# 			ball.accx = -2

# 		if pygame.key.get_pressed()[pygame.K_RIGHT]:
# 			ball.accx = 2

# 		if not(pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]):
# 			ball.accx = 0

# 	if pygame.key.get_pressed()[pygame.K_DOWN]:
# 		ball.fast_falling = True
# 		ball.max_forward_speed *= 2
# 	else:
# 		ball.fast_falling = False
# 	pygame.display.update()
# 	map1.draw()
# 	ball.update(deltat)
# 	ball.draw()

shot_list = pygame.sprite.Group()
while 1:
	deltat = clock.tick(30)

	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit(0)
		if not hasattr(event, 'key'): continue
		if event.type == KEYDOWN:
			if event.key == K_UP and ball.jump_ctr == 1:
				ball.jump()
			if event.key == K_UP and ball.jump_ctr == 2:
				ball.jump()
			elif event.key == K_SPACE:
				#if shoot == False:
					if(ball.anim_mode!=ball.NEUTRAL_B):
						ball.anim_ctr = 0
					ball.anim_mode = ball.NEUTRAL_B
					proj = Projectile(ball.position, '../resources/Mario/Mario_Neutral_B/Mario_Fireball.png', ball.direction)
					ball.state_mode = ball.NEUTRAL_B
					# proj.rect.x = 
					# proj.rect.y = 
					#all_sprites.add(proj)
					shot_list.add(proj)
					shoot = True
		if event.type == KEYUP:
			if (event.key == K_LEFT or event.key == K_RIGHT) and ball.touching_platform:
				ball.anim_mode = ball.IDLE
		if event.key == K_ESCAPE:
			sys.exit(0)
	if(ball.touching_platform and ball.state_mode == ball.IDLE):
		if(ball.falling == True):
			ball.state_mode = ball.IDLE
			ball.falling = False
		if(ball.state_mode == ball.IDLE):
			ball.anim_mode = ball.IDLE
		if pygame.key.get_pressed()[pygame.K_LEFT] and ball.falling == False:
			ball.accx = -3
			if(pygame.key.get_pressed()[pygame.K_UP] and ball.jump_ctr == 2):
				ball.jump()
				ball.anim_mode = ball.JUMPING
				ball.touching_platform = False
			elif(ball.touching_platform and ball.anim_mode!=ball.JUMPING):
				ball.anim_mode = ball.RUNNING
				ball.direction = "left"
		if pygame.key.get_pressed()[pygame.K_RIGHT] and ball.falling == False:
			ball.accx = 3
			if(pygame.key.get_pressed()[pygame.K_UP] and ball.jump_ctr == 2):
				ball.jump()
				ball.anim_mode = ball.JUMPING
				ball.touching_platform = False
			elif(ball.touching_platform and ball.anim_mode!=ball.JUMPING):
				ball.anim_mode = ball.RUNNING
				ball.direction = "right"
		if not(pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]):
			ball.accx = 0
		if(pygame.key.get_pressed()[pygame.K_p]):
			if(ball.anim_mode!=ball.JAB):
				ball.anim_ctr = 0
			ball.anim_mode = ball.JAB
			ball.state_mode = ball.JAB
	else:
		if pygame.key.get_pressed()[pygame.K_LEFT]:
			ball.accx = -1.4
		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			ball.accx = 1.4
		if pygame.key.get_pressed()[pygame.K_DOWN]:
			ball.fast_falling = True
			ball.max_forward_speed *= 2
		else:
			ball.fast_falling = False

	for shot in shot_list:
		shot.update()
    # Remove the bullet if it flies up off the screen
		# if shot.rect.x >= 1024 or shot.rect.x <= -20:
		# 	shot.kill()
		# 	#all_sprites.remove(shot)
		# 	shot_list.remove(shot)
		# 	shoot = False
	pygame.display.update()
	map1.draw()
	ball.update(deltat)
	ball.draw()	

	#pygame.draw.rect(screen, (0,255,0), ((screen.get_width() / 2, screen.get_height() / 2, 4, 4)), 0) #uncomment to see center 


