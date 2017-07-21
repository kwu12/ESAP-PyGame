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
		#self.screen

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

class Projectile:
	ACCELERATION = 0.5
	MAX_FORWARD_SPEED = 1
	MAX_REVERSE_SPEED = -5

	def __init__(self, position):
		self.position = position

	def draw(self):
		pygame.draw.rect(screen, (255, 255, 255), (int(self.position[0]), int(self.position[1])), 0)

class Ball:
	ACCELERATION = 0.5
	MAX_FORWARD_SPEED = 1
	MAX_REVERSE_SPEED = -5

	def __init__(self, position):
		#pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.rect = Rect(position, (4,4))
		self.speed = 0
		self.k_up = self.k_down = 0
		self.platforms = []
		self.radius = 4
		self.touching_platform = False
		self.velx = 0
		self.jump_ctr = 2

	def draw(self):
		pygame.draw.circle(screen, (255, 0, 0), (int(self.position[0]), int(self.position[1])), self.radius, 0)

	def add_platforms(self, platforms):
		self.platforms.extend(platforms)

	def get_rect(self):
		return Rect(self.position, (self.radius, self.radius))

	def jump(self):
		x, y = self.position
		if self.jump_ctr == 2:
			#self.move(x, y - 30)
			self.speed = -10
			self.jump_ctr -= 1
		elif self.jump_ctr == 1:
			self.speed = -8
			self.jump_ctr -= 1


	def move(self, x, y):
		self.position = (x, y)
		self.rect = self.get_rect()

	def update(self, deltat):
		#SIMULATION
		#self.speed += (self.k_up + self.k_down)
		#print(self.speed)
		'''
		if self.speed > self.MAX_FORWARD_SPEED: 
			self.speed = self.MAX_FORWARD_SPEED
		elif self.speed < -self.MAX_REVERSE_SPEED:
			self.speed = -self.MAX_REVERSE_SPEED
			'''
		#if self.speed > self.
		self.move(self.position[0] + self.velx, self.position[1])
		if self.speed > self.MAX_FORWARD_SPEED:
			speed = self.MAX_FORWARD_SPEED
		if not self.touching_platform:
			self.speed += self.ACCELERATION
		x, y = self.position
		y += self.speed
		self.move(x, y)
		#if len(pygame.sprite.spritecollide(self, self.platforms, False)) > 0:
		#print(self.rect.left, self.rect.top)
		#print(self.platforms[0].boundary_rect.left, self.platforms[0].boundary_rect.top)
		if y >= 570:
			self.move(screen.get_width() / 2, 0)
			self.speed = 0
			self.velx = 0
		if self.rect.colliderect(self.platforms[0].boundary_rect) and not self.platforms[0].fall_through: 
			self.touching_platform = True
			self.speed = 0 
			self.move(x, self.platforms[0].boundary_rect.top - self.radius)		
			self.jump_ctr = 2	
			# self.speed *= -1
			self.velx = 0
		else:
			self.touching_platform = False
		

			


#460 x 171
plat_image = "Stage1.jpg"
plat_image1 = "Battlefield_Bottom.png"
image = "SpaceBG.jpg"
image1= "CastleBG.jpg"
map1 = Map("Final Destination", image)
plat1 = Platform((screen.get_width() / 2, screen.get_height() / 2), plat_image)
map1.platforms.append(plat1)
#pygame.sprite.spritecollide(, surface_group, False)
ball = Ball((screen.get_width() / 2, 100))
projectile = Projectile(ball.position)
ball.add_platforms([plat1])

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
		if event.key == K_ESCAPE:
			sys.exit(0)
	if pygame.key.get_pressed()[pygame.K_LEFT]:
		ball.velx = -5
	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		ball.velx = 5
	if pygame.key.get_pressed()[pygame.K_SPACE]:
		projectile.velx = 5
	pygame.display.update()
	map1.draw()
	ball.update(deltat)
	ball.draw()



	#pygame.draw.rect(screen, (0,255,0), ((screen.get_width() / 2, screen.get_height() / 2, 4, 4)), 0) #uncomment to see center 


