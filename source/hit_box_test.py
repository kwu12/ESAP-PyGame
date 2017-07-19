import pygame, math, sys, random
from pygame.locals import *
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()

class Dummy:
	def __init__(self):
		self.radius = 50
		self.x = 512
		self.y = 288
		self.rect = Rect(self.x,self.y,self.radius,self.radius)
		self.xVel = 0
		self.yVel = 0
	def draw(self):
		self.x+=self.xVel
		self.y+=self.yVel
		self.xVel*=0.9
		self.yVel*=0.9
		pygame.draw.circle(screen, (255,0,0), (int(self.x), int(self.y)), self.radius, 0) 
		self.rect = Rect(self.x,self.y,self.radius,self.radius)

	def add_knockback(self, knockbackX, knockbackY):
		self.xVel = knockbackX
		self.yVel = knockbackY

class Hitbox:
	def __init__(self, xPos, yPos, width, height, damage, knockbackX, knockbackY):
		self.active = False
		self.xPos = xPos
		self.yPos = yPos
		self.width = width
		self.height = height
		self.damage = damage
		self.knockbackX = knockbackX
		self.knockbackY = knockbackY
		self.rect = Rect(self.xPos, self.yPos, self.width, self.height)

	def draw(self):
		pygame.draw.rect(screen, (0,0,255), self.rect, 0) 
 
	def update(self):
		self.rect = Rect(self.xPos, self.yPos, self.width, self.height)
		if self.rect.colliderect(ball.rect) and self.active:
			print("kb")
			ball.add_knockback(self.knockbackX, self.knockbackY)
			self.active = False


hitbox = Hitbox(512,288,10,10,10,10,30)
ball = Ball()

while 1:
	deltat = clock.tick(30)

	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit(0)
		if pygame.key.get_pressed()[pygame.K_SPACE]:
			hitbox.active = True
			print("true")
	screen.fill((255,255,255))
	ball.draw()
	hitbox.draw()
	hitbox.update()
	pygame.display.flip()
	pygame.display.update()