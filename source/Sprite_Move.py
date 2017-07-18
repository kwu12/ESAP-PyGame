#INIT
import pygame, math, sys, random
from pygame.locals import *
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

class Sprite(pygame.sprite.Sprite):
	MAX_FORWARD_SPEED = 20
	MAX_REVERSE_SPEED = 20
	Right = True
	def __init__(self, image, position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.src_image = pygame.image.load(image)
		self.rect = self.src_image.get_rect()
		# self.speed = self.direction = 0
		self.speedx = 0
		self.speedy = 0
		self.k_x = self.k_y = 0
		self.acceleration = .5
		self.direction = "right"

	def update(self, deltat):
			#SIMULATION
			self.speedx*=0.8
			#self.speedy*=0.8
			self.speedx += self.k_x
			self.speedy += self.acceleration
			if self.speedx > self.MAX_FORWARD_SPEED: 
						self.speedx = self.MAX_FORWARD_SPEED
			if self.speedx < -self.MAX_REVERSE_SPEED:
						self.speedx = -self.MAX_REVERSE_SPEED
			if self.speedy > self.MAX_FORWARD_SPEED: 
						self.speedy = self.MAX_FORWARD_SPEED
			if self.speedy < -self.MAX_REVERSE_SPEED:
						self.speedy = -self.MAX_REVERSE_SPEED

			# self.direction += (self.k_right + self.k_left)
			x, y = self.position
			
			x += -self.speedx
			y += self.speedy
			self.position = (x, y)
			self.image = self.src_image
			if facing != "right":
				self.image = pygame.transform.flip(self.image, True, False) 
				#self.direction = facing
			self.rect = self.image.get_rect()
			self.rect.center = self.position


#Create a turtle and run
rect = screen.get_rect()
turtle = Sprite('Turtle.jpg', rect.center)
#create a sprite group that contains just that image
turtle_group = pygame.sprite.RenderPlain(turtle)
facing = "right"
while 1:
	deltat = clock.tick(60)
	for event in pygame.event.get():
		if not hasattr(event, 'key'): continue
		down = event.type == KEYDOWN
		if event.key == K_RIGHT:
			facing = "right"
			# if turtle.direction == "left":
			# 	turtle.image = pygame.transform.flip(turtle.image, True, False) 
			# 	turtle.direction = "right"
			# 	print("hello")
			turtle.k_x = down * -5
		elif event.key == K_LEFT:
			facing = "left"
			# if turtle.direction == "right":
			# 	turtle.image = pygame.transform.flip(turtle.image, True, False)
			# 	turtle.direction = "left"
			# 	print("aoweig")
			turtle.k_x = down * 5
		elif event.key == K_UP:
			turtle.speedy = -10
		elif event.key == K_DOWN:
			turtle.k_y = down * -2
		elif event.key == K_ESCAPE:
			sys.exit(0)
		else:
			turtle.k_x = 0
			turtle.k_y = 0
	#RENDERING

	screen.fill((255, 255, 255))
	turtle_group.update(deltat)
	turtle_group.draw(screen)
	pygame.display.flip()

