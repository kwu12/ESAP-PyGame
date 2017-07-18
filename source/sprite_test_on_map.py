import pygame, math, sys, random
from pygame.locals import *
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()

class Map:
	def __init__(self, name, background_image):
		self.name = name 
		self.background_image = pygame.image.load(background_image)
		self.platforms = []

	def draw(self):
		pygame.display.set_caption(self.name)
		screen.blit(self.background_image, (0,0))
		for plat in self.platforms:
			plat.draw()

class Platform:
	def __init__(self, position, image, fall_through = False):
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		image_rect = self.image.get_rect()
		self.x = position[0]
		self.y = position[1]
		self.rect = Rect(self.x - image_rect.width / 2, self.y, image_rect.width, image_rect.height)
		self.boundary_rect = Rect(self.rect.left, self.rect.top + 20, self.rect.width, self.rect.height)
		self.fall_through = fall_through

	def draw(self):
		screen.blit(self.image, self.rect)
		#pygame.draw.rect(screen, (255,255,0), self.boundary_rect, 0) #uncomment to see center 


class Ball:
	IDLE = 0
	RUNNING = 1
	JUMPING = 2
	NEUTRAL_B = 3
	JAB = 4
	ANIM_NAME = ["Idle","Running","Jumping","Neutral_B","Jab"]
	ANIM_INC = [20,30,14,19,18]
	ANIM_LOOP = [False, False, True, False, False]
	ANIM_MOD = [5,4,7,5,6]
	ACCELERATION = 0.5
	MAX_FORWARD_SPEED = 1
	MAX_REVERSE_SPEED = -5

	def __init__(self, position):
		#pygame.sprite.Sprite.__init__(self)
		self.position = position
		#self.rect = Rect(position, (4,4))
		self.speed = 0
		self.k_up = self.k_down = 0
		self.platforms = []
		self.touching_platform = False
		self.velx = 0
		self.jump_ctr = 2
		self.anim_ctr = 0
		self.image = pygame.image.load("../resources/Mario/Mario_" + self.ANIM_NAME[self.IDLE] + "/Mario_"+ self.ANIM_NAME[self.IDLE] +"1.png")
		self.rect = self.image.get_rect()
		self.anim_mode = self.IDLE
		self.state_mode = self.IDLE
		self.falling = True
		self.direction = "right"
		self.accx = 0
	def draw(self):
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
		#pygame.draw.rect(screen, (255, 0, 0), self.rect, 0)

		#pygame.draw.circle(screen, (255, 0, 0), (int(self.position[0]), int(self.position[1])), self.radius, 0)

	# def anim_incrementer(self, max):
	# 	if(self.anim_ctr<max):
	# 		self.anim_ctr+=1
	# 	else:
	# 		self.anim_ctr = 0
	def anim_incrementer_no_loop(self, max, dont_loop):
		if(self.anim_ctr==max):
			self.state_mode = self.IDLE
		if(self.anim_ctr>max):
			self.anim_ctr = max
		if(self.anim_ctr<max):
			self.anim_ctr+=1
		elif(dont_loop!=True):
			self.anim_ctr = 0

	def add_platforms(self, platforms):
		self.platforms.extend(platforms)

	def get_rect(self):
		return Rect(self.position, (self.image.get_rect().width,self.image.get_rect().height))

	def jump(self):
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
		self.velx *= 0.7
		self.velx += self.accx
		self.move(self.position[0] + self.velx, self.position[1])
		if self.speed > self.MAX_FORWARD_SPEED:
			speed = self.MAX_FORWARD_SPEED
		if not self.touching_platform:
			self.speed += self.ACCELERATION
		x, y = self.position
		y += self.speed
		self.move(x, y)
		if y >= 570:
			self.move(screen.get_width() / 2, 0)
			self.speed = 0
			self.accx = 0
			self.velx = 0
		if self.rect.colliderect(self.platforms[0].boundary_rect) and not self.platforms[0].fall_through: 
			self.touching_platform = True
			self.speed = 0 
			self.move(x, self.platforms[0].boundary_rect.top + 1 - self.rect.height)		
			self.jump_ctr = 2	
			# self.speed *= -1
			#self.accx = 0
		else:
			self.touching_platform = False
		

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
plat_image = "../resources/Platforms/Stage1.jpg"
plat_image1 = "../resources/Platforms/Battlefield_Bottom.png"
image = "../resources/Backgrounds/SpaceBG.jpg"
image1 = "../resources/Backgrounds/CastleBG.jpg"
map1 = Map("Battlefield", image)
plat1 = Platform((screen.get_width() / 2, screen.get_height() / 2), plat_image1)
map1.platforms.append(plat1)
#pygame.sprite.spritecollide(, surface_group, False)
shot_list = pygame.sprite.Group()
shoot = False
ball = Ball((screen.get_width() / 2, 100))
ball.add_platforms([plat1])

while 1:
	deltat = clock.tick(30)

	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit(0)
		if not hasattr(event, 'key'): continue
		if event.type == KEYDOWN:
			#if event.key == K_UP and ball.jump_ctr == 1:
				#ball.jump()
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