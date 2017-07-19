'''
-Changed double jumps
-changed jab timing
'''
import pygame, math, sys, random, os
from pygame.locals import *
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,50)
screen = pygame.display.set_mode((1024, 576))
pygame.display.set_caption("Smeesh")
clock = pygame.time.Clock()
pygame.font.init()
shoot = False
map_name = "Battlefield"

pygame.mixer.init()
pygame.mixer.music.load('../resources/Music/stage_select.mp3')
pygame.mixer.music.play(-1, 0.0)


def greenify(surface):
	surface = surface.copy()
	for x in range(surface.get_size()[0]):
		for y in range(surface.get_size()[1]):
			color = surface.get_at([x, y])
			red = Color(255, 0 ,0)
			dist = math.sqrt((red.r - color.r)**2 + (red.g - color.g)**2 + (red.b - color.b)**2)
			#color2 = pygame.color.Color(r,g,b,0)
			#0-30 330-360
			if dist <= 170:
				if color.r - 80 < 0:
					color.r = 0
				else:
					color.r -= 80
				if color.g + 80 > 255:
					color.g = 255
				else:
					color.g += 80
				surface.set_at([x, y], color)
	return surface


class Button:

	def __init__(self, position, image, name):
		self.position = position
		self.image = pygame.image.load(image)
		self.rect = Rect(position[0], position[1], self.image.get_rect().width, self.image.get_rect().height)
		self.hover = False
		self.name = name

	def draw(self):
		screen.blit(self.image, self.rect)
		if self.hover:
			pygame.draw.rect(screen, (255, 0, 0), (self.rect.left - 3, self.rect.top - 3, self.rect.width + 6, self.rect.height + 6), 1)

	def action(self):
		global map_name
		map_name = self.name


def game_intro(bypass = False):

	if not bypass:
		done = False

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

		b1 = Button((100, 100), "../resources/GUI/Battlefield_Stage_Icon.png", "Battlefield Brawl")
		b2 = Button((100, 350), "../resources/GUI/Battlefield_Bottom_Icon.png", "Battlefield")
		b3 = Button((725, 350), "../resources/GUI/Final_Dest_Icon.png", "Final Destination")
		button_list = [b1, b2, b3]


		while not done:
			deltat = clock.tick(30)
			mouse = pygame.mouse.get_pos()

			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					for button in button_list:
						if button.rect.collidepoint(mouse):
							button.action()
							done = True
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
			for button in button_list:
				button.draw()

	return True

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

def create_map_from_file(name):
	plats = []
	plt = []
	with open("../data/map_data/" + (name + ".txt"), "r") as f:
		total_lines = f.readlines()
		total_lines = [ln[:-1] for ln in total_lines]
		for ln in total_lines:
			#ln = f.readLine()
			if ln == "":
				continue
			elif ln.find("name = ") != -1:
				nm = ln.replace("name = ", "")
			elif ln.find("base_image = ") != -1:
				bg = "../resources/Backgrounds/" + ln.replace("base_image = ", "")
			elif ln.find("*PLATFORM*") != -1:
				if len(plt) != 0:
					if plt[4] == "None":
						mp = None
					else:
						mp = (float(plt[4]), float(plt[5]), float(plt[6]))
					ft = plt[3] == "True"
					plats.append(Platform((plt[0],plt[1]), plt[2], fall_through = ft, move_params = mp))
				plt = []
			elif ln.find("platformx = ") != -1:
				plt.append(screen.get_width() * float(ln.replace("platformx = ", "")))
			elif ln.find("platformy = ") != -1:
				plt.append(screen.get_height() * float(ln.replace("platformy = ", "")))
			elif ln.find("plat_image = ") != -1:
				plt.append("../resources/Platforms/" + (ln.replace("plat_image = ", "")))
			elif ln.find("fall_through = ") != -1:
				plt.append((ln.replace("fall_through = ", "")))
			elif ln.find("move_params0 = ") != -1:
				plt.append(ln.replace("move_params0 = ", ""))
			elif ln.find("move_params1 = ") != -1:
				plt.append(ln.replace("move_params1 = ", ""))
			elif ln.find("move_params2 = ") != -1:
				plt.append(ln.replace("move_params2 = ", ""))
	mapp = Map(nm, bg, platforms = plats)
	return mapp
class Platform:

	def __init__(self, position, image, fall_through = False, move_params = None):
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		self.x = position[0]
		self.y = position[1]
		self.fall_through = fall_through 
		self.move(self.x, self. y)
		self.move_params = move_params
		self.dir = 1
		if self.move_params != None:
			self.target = self.x + self.move_params[0] / 2
		self.time = 0

	def draw(self):
		screen.blit(self.image, self.rect)
		# if self.move_params != None:
		# 	pygame.draw.rect(screen, (255,255,255), Rect(self.target - self.move_params[0], self.y, self.move_params[0], 10))
		# colors = [(255,255,0), (255,0,0), (0,255,0), (0,0,255)]
		# for i in range(len(self.boundaries)):
		# 	pygame.draw.rect(screen, colors[i], self.boundaries[i], 0) #uncomment to see center

	def move(self, x, y):
		self.x = x
		self.y = y
		image_rect = self.image.get_rect()
		num = image_rect.width / 25
		self.rect = Rect(self.x - image_rect.width / 2, self.y, image_rect.width, image_rect.height)
		#legacy collision boxes
		# boundary_top = Rect(self.rect.left, self.rect.top + num, self.rect.width, num)
		# boundary_bottom = Rect(self.rect.left + num, self.rect.bottom - num, self.rect.width - 2 * num, num)
		# boundary_left = Rect(self.rect.left, self.rect.top + 2 * num, num, self.rect.height - 2 * num)
		# boundary_right = Rect(self.rect.right - num, self.rect.top + 2 * num, num, self.rect.height - 2 * num)
		boundary_top = Rect(self.rect.left + num, self.rect.top + num, self.rect.width - 2 * num, num)
		boundary_bottom = Rect(self.rect.left + 2 * num, self.rect.bottom - num, self.rect.width - 4 * num, num)
		boundary_left = Rect(self.rect.left + num, self.rect.top + 2 * num, num, self.rect.height - 2 * num)
		boundary_right = Rect(self.rect.right - 2 * num, self.rect.top + 2 * num, num, self.rect.height - 2 * num)
		self.boundaries = [boundary_top, boundary_bottom, boundary_left, boundary_right]

	def mvmnt_inc(self, deltat):
		#return (self.target - self.move_params[0] / 2) + self.move_params[0] / 2* math.sin(self.time * math.pi / (2 * self.target / 2))
		speed = self.move_params[1]
		mod = (math.pi * self.move_params[0]) / (2 * speed)
		return deltat / 1000 * mod * math.cos(math.pi * self.time / (1000 * speed))
 
	def update(self, deltat):
		if self.move_params != None:
			speed = self.move_params[1]
			vel = self.mvmnt_inc(deltat)
			self.time += deltat #* speed 
			self.move(self.x + vel, self.y)

class Map:
	def __init__(self, name, background_image, platforms = []):
		self.platforms = platforms
		self.name = name
		self.background_image = pygame.image.load(background_image)

		
	def draw(self):
		screen.blit(self.background_image, (0,0))
		for plat in self.platforms:
			plat.draw()

	def update(self, deltat):
		for plat in self.platforms:
			plat.update(deltat)
class Ball:
	ACCELERATION = 0.5
	max_forward_speed = 7.8
	MAX_X_SPEED = 5

	IDLE = 0
	RUNNING = 1
	JUMPING = 2
	NEUTRAL_B = 3
	JAB = 4
	DOUBLE_JUMP = 5
	CROUCHING = 6
	FORWARD_TILT = 7
	DOWN_TILT= 8
	UP_B = 9
	ANIM_NAME = ["Idle","Running","Jumping","Neutral_B","Jab","Double_Jump","Crouching","Forward_Tilt", "Down_Tilt", "Up_B"]
	ANIM_INC = [20,30,14,11,8,13,0, 7, 8, 23]
	ANIM_LOOP = [False, False, True, False, False, False, True, False, False, False]
	ANIM_MOD = [5,4,7,3,2,2,1,1,1,4]
	MAX_REVERSE_SPEED = -5


	def __init__(self, position, health_bar, luigi, platforms = []):
		#pygame.sprite.Sprite.__init__(self)
		self.luigi = luigi
		self.health_bar = health_bar
		self.position = position
		self.speed = 0
		self.k_up = self.k_down = 0
		self.platforms = platforms
		self.radius = 4
		self.touching_platform = False
		self.velx = 0
		self.jump_ctr = 2
		self.fast_falling = False
		self.accx = 0
		self.anim_mode = self.IDLE
		self.state_mode = self.IDLE
		self.falling = True
		self.direction = "right"
		self.anim_ctr = 0
		self.image = pygame.image.load("../resources/Mario/Mario_" + self.ANIM_NAME[self.IDLE] + "/Mario_"+ self.ANIM_NAME[self.IDLE] +"1.png")
		self.image = pygame.surface.Surface((self.image.get_rect().width, self.image.get_rect().height), SRCALPHA, self.image)
		self.rect = self.get_rect()


	def draw(self):
		#pygame.draw.circle(screen, (255, 0, 0), (int(self.position[0]), int(self.position[1])), self.radius, 0)
		#pygame.draw.rect(screen, (255,255,255), self.rect, 0)
		self.health_bar.draw()
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
		if(self.falling and not(self.touching_platform)):
			self.image = pygame.image.load("../resources/Mario/Mario_Double_Jump/Mario_Double_Jump7.png")
			
		if(self.direction == "left"):
			self.image = pygame.transform.flip(self.image,True,False)
			
		#self.rect = self.get_rect()

		# n = self.image.convert_alpha()
		# # red at 50%
		# n.fill(()
		# self.image.blit(n, (0,0))
		#self.image = colorize(self.image, (172,255,47))
		#self.image.fill((172,255,47), special_flags=BLEND_RGB_MULT)
		#self.image = pygame.surface.Surface((self.image.get_rect().width, self.image.get_rect().height), SRCALPHA, self.image)
		# cl = Color(100, 100, 100, 0)
		# cl.hsva = (100, 82, 100, 0)
		# self.image.fill(cl, self.rect, BLEND_RGBA_ADD)
		#print(self.image.get_pallete())
		if self.luigi:
			self.image = greenify(self.image)
		screen.blit(self.image, self.position)


	def add_platforms(self, platforms):
		self.platforms.extend(platforms)

	def get_rect(self):
		#return Rect(self.position, (self.radius, self.radius))
		return Rect(self.position, (self.image.get_rect().width, self.image.get_rect().height))

	def jump(self):
		# x, y = self.position
		# if self.jump_ctr == 2:
		# 	#self.move(x, y - 30)
		# 	self.speed = -10
		# 	self.jump_ctr -= 1
		# elif self.jump_ctr == 1:
		# 	self.speed = -8
		# 	self.jump_ctr -= 1

		x, y = self.position
		if self.jump_ctr == 2:
			#self.move(x, y - 30)
			self.speed = -14
			self.jump_ctr -= 1
			self.anim_mode = self.JUMPING
			self.state_mode = self.JUMPING
			self.falling = False
			self.anim_ctr = 0
		elif self.jump_ctr == 1 and self.speed >= -4: 
			self.speed = -12
			self.jump_ctr -= 1
			self.anim_mode = self.DOUBLE_JUMP
			self.state_mode = self.DOUBLE_JUMP
			self.falling = False
			self.anim_ctr = 0

	def move(self, x, y):
		self.position = (x, y)
		self.rect = self.get_rect()
		if(self.speed>2):
			self.falling = True

	def update(self, deltat):
		# x, y = self.position
		# self.velx *= 0.8
		# self.velx += self.accx

		# x += self.velx
		# y += self.speed
		# #self.acccx = 0
		# if self.velx > abs(self.MAX_X_SPEED) and self.velx < 0:
		# 	self.velx = -self.MAX_X_SPEED
		# elif self.velx > abs(self.MAX_X_SPEED) and self.velx > 0:
		# 	self.velx = self.MAX_X_SPEED
		self.velx *= 0.7
		self.velx += self.accx
		self.move(self.position[0] + self.velx, self.position[1])
		if self.speed > self.max_forward_speed:
			speed = self.max_forward_speed
		if not self.touching_platform:
			self.speed += self.ACCELERATION
		x, y = self.position
		y += self.speed
		self.move(x, y)

		#self.move(x, y)
		if not self.touching_platform and self.fast_falling:
			self.speed += self.ACCELERATION * 2
		elif not self.touching_platform:
			self.speed += self.ACCELERATION
		if self.speed > self.max_forward_speed:
			self.speed = self.max_forward_speed
		self.max_forward_speed = 7.1
		#self.move(x, y)
		
		if y >= screen.get_height():
			self.move(screen.get_width() / 2, 0)
			self.speed = 0
			self.velx = 0
			self.accx = 0

		if x >= screen.get_width() + 25:
			self.move(screen.get_width() / 2, 0)
			self.speed = 0
			self.velx = 0
			self.accx = 0

		if x <=  -25:
			self.move(screen.get_width() / 2, 0)
			self.speed = 0
			self.velx = 0
			self.accx = 0


		bools = []
		for platform in self.platforms:
			boundary_rect = platform.boundaries[0]

			if self.rect.colliderect(boundary_rect) and self.speed >= 0 and (not self.fast_falling or not platform.fall_through): #and not platform.fall_through: 
				#if self.rect.bottom > boundary_rect.top and self.rect.bottom - boundary_rect.top > 0:
				#print(2)
				# print(self.rect.bottom)
				# print(boundary_rect.top)

				self.speed = 0 
				self.move(x, boundary_rect.top - self.rect.height) 		
				self.jump_ctr = 2	
				bools.append(True)
				#print(y)
				#print(boundary_rect.top - self.rect.height)
				if platform.move_params != None:
					self.move(x + platform.mvmnt_inc(deltat), boundary_rect.top - platform.rect.height - platform.move_params[2])
				# self.speed *= -1
				#self.velx = 0
			else:
				bools.append(False)
			x, y = self.position
			if not self.rect.colliderect(boundary_rect) and not platform.fall_through:
				#print("Here")
				if self.rect.colliderect(platform.boundaries[1]):
					self.speed = 0 
					self.move(x, platform.boundaries[1].bottom) #+ self.rect.height)		
					#self.velx = 0
				elif self.rect.colliderect(platform.boundaries[2]):
					#self.speed = 0 
					self.move(platform.boundaries[2].left - self.rect.width, y)		
					self.velx = 0
				elif self.rect.colliderect(platform.boundaries[3]):
					#self.speed = 0 
					self.move(platform.boundaries[3].right, y)		
					self.velx = 0
			self.touching_platform = True in bools
				# else:
				# 	self.touching_platform = False
				# else:
				# 	self.touching_platform = False

			

	def anim_incrementer_no_loop(self, max, dont_loop):
		if(self.anim_ctr==max and self.touching_platform):
			self.state_mode = self.IDLE
		if(self.anim_ctr>max):
			self.anim_ctr = max
		if(self.anim_ctr<max):
			self.anim_ctr+=1
		elif(dont_loop!=True):
			self.anim_ctr = 0

	def add_knockback(self, knockbackX, knockbackY):
		self.velx = knockbackX
		self.speed = -knockbackY

class Projectile(pygame.sprite.Sprite):
	def __init__(self, position, image, direction, luigi = False):
		super().__init__()
		self.position = position
		self.xspeed = 15
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = position 
		self.direction = direction
		self.life_ctr = 0
		self.luigi = luigi
		
	def update(self):
		self.image = pygame.transform.rotate(self.image, 90)
		self.image = greenify(self.image)
		screen.blit(self.image, self.rect)
		self.life_ctr += 1
		if(self.life_ctr>30):
			self.kill()

		if self.direction != "right":
			self.rect.x -= self.xspeed
		else:
			self.rect.x += self.xspeed

class Hitbox:
	def __init__(self, xPos, yPos, width, height, damage, knockbackX, knockbackY, owner):
		self.active = False
		self.xPos = xPos
		self.yPos = yPos
		self.width = width
		self.height = height
		self.damage = damage
		self.knockbackX = knockbackX
		self.knockbackY = knockbackY
		self.owner = owner
		self.rect = Rect(self.xPos + self.owner.position[0], self.yPos + self.owner.position[1], self.width, self.height)

	def draw(self):
		pass
		#pygame.draw.rect(screen, (0,0,255), self.rect, 0) 
 
	def update(self):
		self.rect = Rect(self.xPos + self.owner.position[0], self.yPos + self.owner.position[1], self.width, self.height)
		if self.rect.colliderect(ball1.rect) and self.active:
			print("kb")
			ball1.health_bar.update(random.randint(0, 10))
			ball1.add_knockback(self.knockbackX, self.knockbackY)
			self.active = False


class Health:

	def __init__(self, position, color, size, text):
		self.position = position
		self.size = size
		#self.positiondecrease = positiondecrease
		self.hp = 100
		self.color = color
		self.text = text

	def draw(self):
		#print("true")
		pygame.draw.rect(screen, (0, 0, 0), (self.position[0], self.position[1] - 30, self.size, 50))
		pygame.draw.rect(screen, self.color, Rect(self.position, (self.size * (self.hp / 100), 20)), 0)
		title = pygame.font.Font(None, 20)
		#title = pygame.font.SysFont("Arial", 20, bold=False, italic=False) 
		titlefont = title.render(self.text, True, (255, 255, 255))
		size = title.size(self.text)
		screen.blit(titlefont, (self.position[0] + (self.size - size[0]) / 2, self.position[1] - 20))
		#bar = pygame.draw.rect(screen, (255, 255, 255), Rect((0, 546), (self.positionx, 576)), 0)
	
	def update(self, dmg):
		self.hp -= dmg
		if self.hp < 0:
			self.hp = 0
		#canvas.create_rectangle(0, 546, self.positionx, 576, fill = "red", outline = "red")
	
	# def update(self):
	
	# 	bar.draw()
		
		# pygame.draw.rect(screen, (200, 10, 90), Rect((0, 546)))
		# pygame.bar.inflate_ip(self.positiondecrease, -25)

#460 x 171


main_game = False
main_game = game_intro(bypass = False)


map1 = create_map_from_file(map_name)
#map1 = Map("Final Destination")
#pygame.sprite.spritecollide(, surface_group, False)

hbar = Health((0, screen.get_height() - 30), (255, 0, 0), 100, "Player 1 ")
hbar2 = Health((screen.get_width() - 100, screen.get_height() - 30), (0, 255, 0), 100, "Player 2 ")
ball = Ball((screen.get_width() / 2, 100), hbar, True, map1.platforms)
ball1 = Ball((screen.get_width() / 2, 100), hbar2, False, map1.platforms)
hitbox = Hitbox(0,0,10,10,10,10,30, ball)
shot_list = pygame.sprite.Group()

while main_game:
	deltat = clock.tick(30)
	if(ball.touching_platform and ball.ANIM_INC[ball.anim_mode] - ball.anim_ctr < 2):
		ball.state_mode = ball.IDLE
		ball.anim_mode = ball.IDLE
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit(0)
		if event.type == USEREVENT + 1:
			ball.fast_falling = False
		if not hasattr(event, 'key'): continue
		if event.type == KEYDOWN:
			if event.key == K_UP and ball.jump_ctr == 1:
				ball.jump()
			if event.key == K_UP and ball.jump_ctr == 2:
				ball.jump()

		if event.type == KEYUP:
			if (event.key == K_LEFT or event.key == K_RIGHT) and ball.touching_platform:
				ball.anim_mode = ball.IDLE
		if event.key == K_ESCAPE:
			sys.exit(0)


	if(ball.touching_platform and ball.state_mode == ball.IDLE):
		if(ball.touching_platform and ball.falling == True):
			ball.state_mode = ball.IDLE
			ball.falling = False
		if(ball.state_mode == ball.IDLE):
			ball.anim_mode = ball.IDLE
		if pygame.key.get_pressed()[pygame.K_DOWN] and ball.falling == False:
			ball.anim_mode = ball.CROUCHING
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
				hitbox.active = True
			ball.accx = 0
			ball.velx = 0
			ball.anim_mode = ball.JAB
			ball.state_mode = ball.JAB
		if(pygame.key.get_pressed()[pygame.K_p] and (pygame.key.get_pressed()[pygame.K_RIGHT]or pygame.key.get_pressed()[pygame.K_LEFT])):
			if(ball.anim_mode!=ball.FORWARD_TILT):
				ball.anim_ctr = 0
			ball.accx = 0
			ball.velx = 0
			ball.anim_mode = ball.FORWARD_TILT
			ball.state_mode = ball.FORWARD_TILT
		if(pygame.key.get_pressed()[pygame.K_p] and (pygame.key.get_pressed()[pygame.K_DOWN])):
			if(ball.anim_mode!=ball.DOWN_TILT):
				ball.anim_ctr = 0
			ball.accx = 0
			ball.velx = 0
			ball.anim_mode = ball.DOWN_TILT
			ball.state_mode = ball.DOWN_TILT
	elif(ball.falling or ball.jump_ctr<2):
		if pygame.key.get_pressed()[pygame.K_LEFT]:
			ball.accx = -1.4
		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			ball.accx = 1.4
	if pygame.key.get_pressed()[pygame.K_DOWN]:
		ball.fast_falling = True
		ball.max_forward_speed *= 2
		pygame.time.set_timer(USEREVENT + 1, 500)
	if pygame.key.get_pressed()[pygame.K_o] and not(pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]):
		if(ball.anim_mode!=ball.NEUTRAL_B):
			ball.anim_ctr = 0
			ball.anim_mode = ball.NEUTRAL_B
			proj = Projectile(ball.position, '../resources/Mario/Mario_Neutral_B/Mario_Fireball.png', ball.direction, luigi = True)
			ball.state_mode = ball.NEUTRAL_B
			# proj.rect.x = 
			# proj.rect.y = 
			#all_sprites.add(proj)
			shot_list.add(proj)
			shoot = True
	if pygame.key.get_pressed()[pygame.K_o] and pygame.key.get_pressed()[pygame.K_UP]:
		if(ball.anim_mode!=ball.UP_B):
			ball.anim_ctr = 0
			ball.speed = -17
			if(ball.direction == "right"):
				ball.velx = 10
			else:
				ball.velx = -10
		ball.anim_mode = ball.UP_B
		ball.state_mode = ball.UP_B

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
	map1.update(deltat)
	#hbar.draw()
	hbar2.draw()
	ball.update(deltat)
	ball.draw()	
	ball1.update(deltat)
	ball1.draw()	
	if(hitbox!=None):
		hitbox.draw()
		hitbox.update()
	#pygame.draw.rect(screen, (0,255,0), ((screen.get_width() / 2, screen.get_height() / 2, 4, 4)), 0) #uncomment to see center 


