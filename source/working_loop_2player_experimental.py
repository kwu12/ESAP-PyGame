while 1:
	game_intro(bypass = False)
	map1 = create_map_from_file(map_name)
	#map1 = Map("Final Destination")
	#pygame.sprite.spritecollide(, surface_group, False)

	hbar = Health((0, screen.get_height() - 30), (255, 0, 0), 100, "Player 1 ", "../resources/GUI/Mario_stock1.png")
	hbar2 = Health((screen.get_width() - 100, screen.get_height() - 30), (0, 255, 0), 100, "Player 2 ", "../resources/GUI/Luigi_stock1.png")
	ball = Ball((screen.get_width() * .625, screen.get_height() * .3), hbar2, True, map1.platforms)
	ball1 = Ball((screen.get_width() *.375, screen.get_height() * .3), hbar, False, map1.platforms)
	ball.direction = "left"
	hitbox = Hitbox(0,0,10,10,10,10,30, ball, ball1)
	hitbox1 = Hitbox(0,0,10,10,10,10,30, ball1, ball)
	shot_list = pygame.sprite.Group()

	while main_game:
		if ball1.health_bar.lives == 0 or ball.health_bar.lives == 0:
			main_game = False
			continue
		deltat = clock.tick(30)

		if(ball.touching_platform and ball.ANIM_INC[ball.anim_mode] - ball.anim_ctr < 1):
			ball.state_mode = ball.IDLE
			ball.anim_mode = ball.IDLE

		if(ball1.touching_platform and ball1.ANIM_INC[ball1.anim_mode] - ball1.anim_ctr < 1):
			ball1.state_mode = ball1.IDLE
			ball1.anim_mode = ball1.IDLE

		if(ball.stunned<1):
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



			if(pygame.key.get_pressed()[pygame.K_p] and not ball.touching_platform):
					if(ball.anim_mode!=ball.AERIAL):
						ball.anim_ctr = 0
						hitbox.change_rect(0,-10,50,25)
						hitbox.change_kb(10,5)
						hitbox.active = True
					ball.accx = 0
					ball.velx = 0
					ball.anim_mode = ball.AERIAL
					ball.state_mode = ball.AERIAL


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
						hitbox.change_rect(0,-10,50,25)
						hitbox.change_kb(10,5)
						hitbox.active = True
					ball.accx = 0
					ball.velx = 0
					ball.anim_mode = ball.JAB
					ball.state_mode = ball.JAB
				if(pygame.key.get_pressed()[pygame.K_p] and (pygame.key.get_pressed()[pygame.K_RIGHT]or pygame.key.get_pressed()[pygame.K_LEFT])):
					if(ball.anim_mode!=ball.FORWARD_TILT):
						ball.anim_ctr = 0
						hitbox.change_rect(15,5,35,20)
						hitbox.change_kb(35,7)
						hitbox.active = True
					ball.accx = 0
					ball.velx = 0
					ball.anim_mode = ball.FORWARD_TILT
					ball.state_mode = ball.FORWARD_TILT
				if(pygame.key.get_pressed()[pygame.K_p] and (pygame.key.get_pressed()[pygame.K_DOWN])):
					if(ball.anim_mode!=ball.DOWN_TILT):
						ball.anim_ctr = 0
						hitbox.change_rect(15,12,35,15)
						hitbox.change_kb(7,14)
						hitbox.active = True
					ball.accx = 0
					ball.velx = 0
					ball.anim_mode = ball.DOWN_TILT
					ball.state_mode = ball.DOWN_TILT
			elif(ball.falling or ball.jump_ctr<2):
				if(ball.accx>1.4 and ball.stunned<1):
					ball.accx = 1.4
				if(ball.accx<-1.4 and ball.stunned<1):
					ball.accx = -1.4
				if pygame.key.get_pressed()[pygame.K_LEFT]:
					ball.accx = -1.4

				if pygame.key.get_pressed()[pygame.K_RIGHT]:
					ball.accx = 1.4

			if pygame.key.get_pressed()[pygame.K_DOWN] and ball.touching_platform:
				ball.fast_falling = True
				pygame.time.set_timer(USEREVENT + 1, 500)
			if pygame.key.get_pressed()[pygame.K_DOWN] and not ball.touching_platform:
				ball.fast_falling = True
				ball.max_forward_speed *= 2
				pygame.time.set_timer(USEREVENT + 1, 500)
			if pygame.key.get_pressed()[pygame.K_o] and not(pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]) and not(ball.anim_mode == ball.NEUTRAL_B or ball.anim_mode == ball.SIDE_B):
				if(ball.anim_mode!=ball.NEUTRAL_B):
					ball.anim_ctr = 0
					ball.anim_mode = ball.NEUTRAL_B
					fball.play()
					proj = Projectile(ball.position, '../resources/Mario/Mario_Neutral_B/Mario_Fireball.png', ball.direction, ball1, True)
					ball.state_mode = ball.NEUTRAL_B
					shot_list.add(proj)
					shoot = True
			if pygame.key.get_pressed()[pygame.K_o] and pygame.key.get_pressed()[pygame.K_UP] and not(ball.anim_mode == ball.NEUTRAL_B or ball.anim_mode == ball.SIDE_B):
				if(ball.anim_mode!=ball.UP_B):
					ball.anim_ctr = 0
					hitbox.change_rect(5,0,25,25)
					hitbox.change_kb(5,13)
					hitbox.active = True
					ball.speed = -13
					if(ball.direction == "right"):
						ball.velx = 10
					else:
						ball.velx = -10
					ball.anim_mode = ball.UP_B
					ball.state_mode = ball.UP_B

			if pygame.key.get_pressed()[pygame.K_o] and (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]) and not(ball.anim_mode == ball.NEUTRAL_B or ball.anim_mode == ball.UP_B):
				if(ball.anim_mode!=ball.SIDE_B):
					ball.anim_ctr = 0
					hitbox.change_rect(15,0,25,25)
					hitbox.change_kb(5,8)
					hitbox.active = True
					ball.speed = -1
					if(ball.touching_platform):
						ball.accx = 0
					if(pygame.key.get_pressed()[pygame.K_RIGHT]):
						ball.direction = "right"

					else:
						ball.direction = "left"

					if(ball.direction == "right" and not ball.touching_platform):
						#ball.velx = 5
						pass
					elif(ball.direction == "left" and not ball.touching_platform):
						#ball.velx = -5
						pass
				ball.anim_mode = ball.SIDE_B
				ball.state_mode = ball.SIDE_B

		
		if(ball1.stunned<1):
			for event in events:

				if event.type == QUIT:
					sys.exit(0)

				if event.type == USEREVENT + 1:
					ball1.fast_falling = False

				if not hasattr(event, 'key'): continue

				if event.type == KEYDOWN:

					if event.key == K_w and ball1.jump_ctr == 1:
						ball1.jump()

					if event.key == K_w and ball1.jump_ctr == 2:
						ball1.jump()

				if event.type == KEYUP:
					if (event.key == K_a or event.key == K_d) and ball1.touching_platform:
						ball1.anim_mode = ball1.IDLE

				if event.key == K_ESCAPE:
					sys.exit(0)



			if(pygame.key.get_pressed()[pygame.K_b] and not ball1.touching_platform):
					if(ball1.anim_mode!=ball1.AERIAL):
						ball1.anim_ctr = 0
						hitbox1.change_rect(0,-10,50,25)
						hitbox1.change_kb(10,5)
						hitbox1.active = True
					ball1.accx = 0
					ball1.velx = 0
					ball1.anim_mode = ball1.AERIAL
					ball1.state_mode = ball1.AERIAL


			if(ball1.touching_platform and ball1.state_mode == ball1.IDLE):
				if(ball1.touching_platform and ball1.falling == True):
					ball1.state_mode = ball1.IDLE
					ball1.falling = False

				if(ball1.state_mode == ball1.IDLE):
					ball1.anim_mode = ball1.IDLE

				if pygame.key.get_pressed()[pygame.K_s] and ball1.falling == False:
					ball1.anim_mode = ball1.CROUCHING

				if pygame.key.get_pressed()[pygame.K_a] and ball1.falling == False:
					ball1.accx = -3
					if(pygame.key.get_pressed()[pygame.K_w] and ball1.jump_ctr == 2):
						ball1.jump()
						ball1.anim_mode = ball1.JUMPING
						ball1.touching_platform = False
					elif(ball1.touching_platform and ball1.anim_mode!=ball1.JUMPING):
						ball1.anim_mode = ball1.RUNNING
						ball1.direction = "left"
				if pygame.key.get_pressed()[pygame.K_d] and ball1.falling == False:
					ball1.accx = 3
					if(pygame.key.get_pressed()[pygame.K_w] and ball1.jump_ctr == 2):
						ball1.jump()
						ball1.anim_mode = ball1.JUMPING
						ball1.touching_platform = False
					elif(ball1.touching_platform and ball1.anim_mode!=ball1.JUMPING):
						ball1.anim_mode = ball1.RUNNING
						ball1.direction = "right"
				if not(pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]):
					ball1.accx = 0
				if(pygame.key.get_pressed()[pygame.K_b]):
					if(ball1.anim_mode!=ball1.JAB):
						ball1.anim_ctr = 0
						hitbox1.change_rect(0,-10,50,25)
						hitbox1.change_kb(10,5)
						hitbox1.active = True
					ball1.accx = 0
					ball1.velx = 0
					ball1.anim_mode = ball1.JAB
					ball1.state_mode = ball1.JAB
				if(pygame.key.get_pressed()[pygame.K_b] and (pygame.key.get_pressed()[pygame.K_d]or pygame.key.get_pressed()[pygame.K_a])):
					if(ball1.anim_mode!=ball1.FORWARD_TILT):
						ball1.anim_ctr = 0
						hitbox1.change_rect(15,5,35,20)
						hitbox1.change_kb(35,7)
						hitbox1.active = True
					ball1.accx = 0
					ball1.velx = 0
					ball1.anim_mode = ball1.FORWARD_TILT
					ball1.state_mode = ball1.FORWARD_TILT
				if(pygame.key.get_pressed()[pygame.K_b] and (pygame.key.get_pressed()[pygame.K_s])):
					if(ball1.anim_mode!=ball1.DOWN_TILT):
						ball1.anim_ctr = 0
						hitbox1.change_rect(15,12,35,15)
						hitbox1.change_kb(7,14)
						hitbox1.active = True
					ball1.accx = 0
					ball1.velx = 0
					ball1.anim_mode = ball1.DOWN_TILT
					ball1.state_mode = ball1.DOWN_TILT
			elif(ball1.falling or ball1.jump_ctr<2):
				if(ball1.accx>1.4 and ball1.stunned<1):
					ball1.accx = 1.4
				if(ball1.accx<-1.4 and ball1.stunned<1):
					ball1.accx = -1.4
				if pygame.key.get_pressed()[pygame.K_a]:
					ball1.accx = -1.4

				if pygame.key.get_pressed()[pygame.K_d]:
					ball1.accx = 1.4

			if pygame.key.get_pressed()[pygame.K_s] and ball1.touching_platform:
				ball1.fast_falling = True
				pygame.time.set_timer(USEREVENT + 1, 500)
			if pygame.key.get_pressed()[pygame.K_s] and not ball1.touching_platform:
				ball1.fast_falling = True
				ball1.max_forward_speed *= 2
				pygame.time.set_timer(USEREVENT + 1, 500)
			if pygame.key.get_pressed()[pygame.K_v] and not(pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]) and not(ball1.anim_mode == ball1.NEUTRAL_B or ball1.anim_mode == ball1.SIDE_B):
				if(ball1.anim_mode!=ball1.NEUTRAL_B):
					ball1.anim_ctr = 0
					ball1.anim_mode = ball1.NEUTRAL_B
					fball1.play()
					proj = Projectile(ball1.position, '../resources/Mario/Mario_Neutral_B/Mario_Fireball.png', ball1.direction, ball, False)
					ball1.state_mode = ball1.NEUTRAL_B
					shot_list.add(proj)
					shoot = True
			if pygame.key.get_pressed()[pygame.K_v] and pygame.key.get_pressed()[pygame.K_w] and not(ball1.anim_mode == ball1.NEUTRAL_B or ball1.anim_mode == ball1.SIDE_B):
				if(ball1.anim_mode!=ball1.UP_B):
					ball1.anim_ctr = 0
					hitbox1.change_rect(5,0,25,25)
					hitbox1.change_kb(5,13)
					hitbox1.active = True
					ball1.speed = -13
					if(ball1.direction == "right"):
						ball1.velx = 10
					else:
						ball1.velx = -10
					ball1.anim_mode = ball1.UP_B
					ball1.state_mode = ball1.UP_B

			if pygame.key.get_pressed()[pygame.K_v] and (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]) and not(ball1.anim_mode == ball1.NEUTRAL_B or ball1.anim_mode == ball1.UP_B):
				if(ball1.anim_mode!=ball1.SIDE_B):
					ball1.anim_ctr = 0
					hitbox1.change_rect(15,0,25,25)
					hitbox1.change_kb(5,8)
					hitbox1.active = True
					ball1.speed = -1
					if(ball1.touching_platform):
						ball1.accx = 0
					if(pygame.key.get_pressed()[pygame.K_d]):
						ball1.direction = "right"

					else:
						ball1.direction = "left"

					if(ball1.direction == "right" and not ball1.touching_platform):
						#ball1.velx = 5
						pass
					elif(ball1.direction == "left" and not ball1.touching_platform):
						#ball1.velx = -5
						pass
				ball1.anim_mode = ball1.SIDE_B
				ball1.state_mode = ball1.SIDE_B

		for shot in shot_list:
			shot.update()
		pygame.display.update()
		map1.draw()
		map1.update(deltat)
		ball.update(deltat)
		ball.draw()	
		ball1.update(deltat)
		ball1.draw()	
		if(hitbox!=None):
			hitbox.draw()
			hitbox.update()

	if(ball.health_bar.lives == 0):
		winner = "Player 1"
	else:
		winner = "Player 2"

	pygame.time.delay(750)
	game_end(winner)
		#pygame.draw.rect(screen, (0,255,0), ((screen.get_width() / 2, screen.get_height() / 2, 4, 4)), 0) #uncomment to see center 