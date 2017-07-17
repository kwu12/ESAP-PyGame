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

	def __init__(self, position, image):
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		image_rect = self.image.get_rect()
		self.x = position[0]
		self.y = position[1]
		self.rect = Rect(self.x - image_rect.width / 2, self.y, image_rect.width, image_rect.height)
		self.boundary_rect = Rect(self.rect.left, self.rect.top + 20, self.rect.width, 20)

	def draw(self):
		screen.blit(self.image, self.rect)
		#pygame.draw.rect(screen, (255,255,0), self.boundary_rect, 0) #uncomment to see center 


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

	def draw(self):
		pygame.draw.circle(screen, (255, 0, 0), (int(self.position[0]), int(self.position[1])), self.radius, 0)

	def add_platforms(self, platforms):
		self.platforms.extend(platforms)

	def get_rect(self):
		return Rect(self.position, (self.radius, self.radius))

	def move(self, x, y):
		self.position = (x, y)
		self.rect = self.get_rect()

	def update(self, deltat):
		#SIMULATION
		if True:
			#self.speed += (self.k_up + self.k_down)
			#print(self.speed)
			'''
			if self.speed > self.MAX_FORWARD_SPEED: 
				self.speed = self.MAX_FORWARD_SPEED
			elif self.speed < -self.MAX_REVERSE_SPEED:
				self.speed = -self.MAX_REVERSE_SPEED
				'''
			#if self.speed > self.
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
			if self.rect.colliderect(self.platforms[0].boundary_rect): 
				self.touching_platform = True
				self.speed = 0 
				self.move(x, self.platforms[0].boundary_rect.top - self.radius)			
				# self.speed *= -1
			else:
				self.touching_platform = False

			


#460 x 171
plat_image = "../resources/Stage_images/Stage1.jpg"
plat_image1 = "../resources/Battlefield_Bottom.png"
image = "../resources/space.jpg"
image1= "../resources/CastleBG.jpg"
map1 = Map("Final Destination", image)
plat1 = Platform((screen.get_width() / 2, screen.get_height() / 2), plat_image)
map1.platforms.append(plat1)
#pygame.sprite.spritecollide(, surface_group, False)
ball = Ball((screen.get_width() / 2, 100))
ball.add_platforms([plat1])

while 1:
	deltat = clock.tick(30)
	for event in pygame.event.get():
		if not hasattr(event, 'key'): continue
		down = event.type == KEYDOWN
		if event.key == K_RIGHT:
			ball.move(ball.position[0] + 5, ball.position[1])
		if event.key == K_LEFT:
			ball.move(ball.position[0] - 5, ball.position[1])
		if event.key == K_ESCAPE:
			sys.exit(0)
	pygame.display.update()
	map1.draw()
	ball.update(deltat)
	ball.draw()



	#pygame.draw.rect(screen, (0,255,0), ((screen.get_width() / 2, screen.get_height() / 2, 4, 4)), 0) #uncomment to see center 


