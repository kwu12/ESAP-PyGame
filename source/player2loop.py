while 1:

	while main_game:
		events = pygame.event.get()
		if(ball1.touching_platform and ball1.ANIM_INC[ball1.anim_mode] - ball1.anim_ctr < 1):
			ball1.state_mode = ball1.IDLE
			ball1.anim_mode = ball1.IDLE
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

		#pygame.draw.rect(screen, (0,255,0), ((screen.get_width() / 2, screen.get_height() / 2, 4, 4)), 0) #uncomment to see center 