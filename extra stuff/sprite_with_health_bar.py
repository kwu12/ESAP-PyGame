#INIT
import pygame, math, sys, random
from pygame.locals import *
#from drawingpanel import *
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()
# pygame.mixer.music.load('.mp3')
# pygame.mixer.music.play(-1

# effect = pygame.mixer.Sound('beep.wav')
# effect.play()

class Health(pygame.sprite.Sprite):

	def __init__(self, positionx, hp):
		self.positionx = positionx
		#self.positiondecrease = positiondecrease
		self.hp = 0

	def draw(self):
		#print("true")
		bar = pygame.draw.rect(screen, (200, 10, 90), Rect((0, 546), (self.positionx - self.hp, 576)), 0)
		#bar = pygame.draw.rect(screen, (255, 255, 255), Rect((0, 546), (self.positionx, 576)), 0)
	
	def update(self):
		self.hp += 5
		#canvas.create_rectangle(0, 546, self.positionx, 576, fill = "red", outline = "red")
	
	# def update(self):
	
	# 	bar.draw()
		
		# pygame.draw.rect(screen, (200, 10, 90), Rect((0, 546)))
		# pygame.bar.inflate_ip(self.positiondecrease, -25)

class Player(pygame.sprite.Sprite):
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

	def update(self):
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


class Projectile(pygame.sprite.Sprite):

	def __init__(self, position, image):
		super().__init__()
		self.position = position
		self.xspeed = 15
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		
	def update(self):
		self.image = pygame.transform.rotate(self.image, 90)
		if shoot == True:
			if direction != "right":
				self.rect.x -= self.xspeed
			else:
				self.rect.x += self.xspeed

		

#Create a turtle and run
rect = screen.get_rect()

all_sprites = pygame.sprite.Group()
shot_list = pygame.sprite.Group()

turtle = Player('resources/Mario/Mario_Idle/Mario_Idle1.png', rect.center)
all_sprites.add(turtle)

facing = "right"
direction = "right"
shoot = False

bar = Health(100, 10)

while 1:
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

		elif event.key == K_SPACE:
			bar.update()
			if shoot == False:
				direction = facing
				proj = Projectile(turtle.position, 'resources/Mario/Mario_Neutral_B/Mario_Fireball.png')
				proj.rect.x = turtle.rect.x
				proj.rect.y = turtle.rect.y
				all_sprites.add(proj)
				shot_list.add(proj)
				shoot = True

		elif event.key == K_ESCAPE:
			sys.exit(0)

		else:
			turtle.k_x = 0
			turtle.k_y = 0

	all_sprites.update()

	for shot in shot_list:
        # Remove the bullet if it flies up off the screen
		if shot.rect.x >= 1024 or shot.rect.x <= -20:
			shot.kill()
			all_sprites.remove(shot)
			shot_list.remove(shot)
			shoot = False


	screen.fill((255, 255, 255))
	all_sprites.draw(screen)
	bar.draw()
	#bar.update()
	pygame.display.flip()
	clock.tick(60)

