import pygame, math, sys, random
from pygame.locals import *
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()

class Map:

	def __init__(self, name, background_image):
		self.name = name 
		self.background_image = pygame.image.load(background_image)

	def draw(self):
		screen.blit(self.background_image, (0,0))
		#self.screen

	def rect(self):
		return Rect(0, 0, 1024, 580)


image = "../resources/space.jpg"
map1 = Map("Final Destination", image)

while 1:
	deltat = clock.tick(30)
	for event in pygame.event.get():
		if not hasattr(event, 'key'): continue
		down = event.type == KEYDOWN
		if event.key == K_ESCAPE:
			sys.exit(0)
	pygame.display.update()
	map1.draw()


# file = open("test.csv", "r")
# print(file.readline().split(","))

