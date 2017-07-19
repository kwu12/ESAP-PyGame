import pygame, sys
from pygame.locals import *

screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()
pygame.font.init()
pygame.display.set_caption("Smeesh")

class Button:

	def __init__(self, position, image):
		self.position = position
		self.image = pygame.image.load(image)
		self.rect = Rect(position[0], position[1], self.image.get_rect().width, self.image.get_rect().height)
		self.hover = False

	def draw(self):
		screen.blit(self.image, self.rect)
		if self.hover:
			pygame.draw.rect(screen, (255, 0, 0), (self.rect.left - 3, self.rect.top - 3, self.rect.width + 6, self.rect.height + 6), 1)

	def action(self):
		print(self.position)

def game_end():

	end = pygame.font.Font(None, 80)
	endfont = end.render("Game Over! PLACEHOLDER wins", True, (0, 0, 0))
	size = end.size("Game OverPLACEHOLDER wins")
	screen.blit(endfont, ((screen.get_width()//2) - (size[0]//2), (screen.get_height()//3) - (size[1]//2)))

	BG = pygame.image.load("../resources/Backgrounds/Stage_Select.png")

	b1 = Button((212, 250), "../resources/GUI/restart-button.png")

	button_list = [b1]

	while 1:
		deltat = clock.tick(30)
		mouse = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				for button in button_list:
					if button.rect.collidepoint(mouse):
						button.action()
			if event.type == MOUSEMOTION:
				for button in button_list:
					if button.rect.collidepoint(mouse):
						button.hover = True
					else:
						button.hover = False
			if not hasattr(event, 'key'): continue
			if event.key == K_ESCAPE:
				sys.exit(0)

		mouse = pygame.mouse.get_pos()


		pygame.display.update()
		screen.blit(BG, (0,0))
		screen.blit(endfont, ((screen.get_width()//2) - (size[0]//2), (screen.get_height()//3) - (size[1]//2)))
		#screen.blit(battlefield, battlefieldrect)
		#screen.blit(Final, Finalrect)
		#screen.blit(Brawl, Brawlrect)
		for button in button_list:
			button.draw()

def game_intro():

	title = pygame.font.Font(None, 80)
	titlefont = title.render("Pick a stage!", True, (0, 0, 0))
	size = title.size("Pick a stage!")
	screen.blit(titlefont, ((screen.get_width()//2) - (size[0]//2), (screen.get_height()//2) - (size[1]//2)))

	BG = pygame.image.load("../resources/Backgrounds/Stage_Select.png")


	battlefield = pygame.image.load("../resources/GUI/Battlefield_Bottom_Icon.png")
	battlefieldrect = battlefield.get_rect()
	battlefieldrect.x = (screen.get_width()//3 - battlefieldrect.width)
	battlefieldrect.y = (2 * screen.get_height()//3 - battlefieldrect.height//2)

	Final = pygame.image.load("../resources/GUI/Final_Dest_Icon.png")
	Finalrect = Final.get_rect()
	Finalrect.x = (2 * screen.get_width()//3)
	Finalrect.y = (2 * screen.get_height()//3 - Finalrect.height//2)

	Brawl = pygame.image.load("../resources/GUI/Battlefield_Stage_Icon.png")
	Brawlrect = Brawl.get_rect()
	Brawlrect.x = (screen.get_width()//3 - Brawlrect.width)
	Brawlrect.y = (screen.get_height()//3 - Brawlrect.height//2)



	#Brawlrect.x = (screen.get_width()//3 - Brawlrect.width)
	#Brawlrect.y = (screen.get_height()//3 - Brawlrect.height//2)

	# mouse = pygame.mouse.get_pos()

	# if 
	b1 = Button((100, 100), "../resources/GUI/Battlefield_Stage_Icon.png")
	b2 = Button((100, 350), "../resources/GUI/Battlefield_Bottom_Icon.png")
	b3 = Button((725, 350), "../resources/GUI/Final_Dest_Icon.png")
	button_list = [b1, b2, b3]

	while 1:
		deltat = clock.tick(30)
		mouse = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				for button in button_list:
					if button.rect.collidepoint(mouse):
						button.action()
			if event.type == MOUSEMOTION:
				for button in button_list:
					if button.rect.collidepoint(mouse):
						button.hover = True
					else:
						button.hover = False
			if not hasattr(event, 'key'): continue
			if event.key == K_ESCAPE:
				sys.exit(0)

		mouse = pygame.mouse.get_pos()


		pygame.display.update()
		screen.blit(BG, (0,0))
		screen.blit(titlefont, ((screen.get_width()//2) - (size[0]//2), (screen.get_height()//2) - (size[1]//2)))
		#screen.blit(battlefield, battlefieldrect)
		#screen.blit(Final, Finalrect)
		#screen.blit(Brawl, Brawlrect)
		for button in button_list:
			button.draw()


		#pygame.display.flip()

game_end()