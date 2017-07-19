import pygame, sys
from pygame.locals import *

screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()
pygame.font.init()

def game_intro():

	title = pygame.font.Font(None, 80)
	titlefont = title.render("Pick a stage!", True, (0, 0, 0))
	size = title.size("Pick a stage!")
	screen.blit(titlefont, ((screen.get_width()//2) - (size[0]//2), (screen.get_height()//2) - (size[1]//2)))
	# battlefield = pygame.image.load("../Battlefield_Bottom_Icon.png")
	# battlefieldrect = battlefield.get_rect()
	# battlefieldrect.x = screen.get_width()//3
	# battlefieldrect.y = 2 * screen.get_height()//3

	# screen.blit(battlefield, battlefieldrect)

	# mouse = pygame.mouse.get_pos()

	# if 
	while 1:
		deltat = clock.tick(30)

		for event in pygame.event.get():
			if not hasattr(event, 'key'): continue
			if event.key == K_ESCAPE:
				sys.exit(0)
		pygame.display.update()
		screen.fill((255,0,0))
		screen.blit(titlefont, ((screen.get_width()//2) - (size[0]//2), (screen.get_height()//2) - (size[1]//2)))

		#pygame.display.flip()

game_intro()