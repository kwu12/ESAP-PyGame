import pygame
from pygame.locals import *
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
	def __init__(self, position, image):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.src_image = pygame.image.load(image)
		self.xVel = self.yVel = 0

	def update(self, deltat):
		x, y = self.position
		x += self.xVel
		y += self.yVel
		self.position = (x, y)
		self.rect = self.src_image.get_rect()
		self.rect.center = self.position

rect = screen.get_rect()
player = Player((512,288), "box.png")
player_group = pygame.sprite.RenderPlain(player)

while 1:
	deltat = clock.tick(20)
	for event in pygame.event.get():
		if not hasattr(event, 'key'): continue
		down = event.type == KEYDOWN
		if event.key == K_RIGHT: 
			player.xVel = 5
		elif event.key == K_LEFT:
			player.xVel = -5
		elif event.key == K_UP:
			player.yVel = -5
		elif event.key == K_DOWN:
			player.yVel = 5
		elif event.key == K_ESCAPE:
			sys.exit(0)

	screen.fill((255,255,255))
	player_group.update(deltat)
	player_group.draw(screen)
	pygame.display.flip()
	pygame.display.update()