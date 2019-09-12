import pygame
import time
import sys
import random
import os
pygame.mixer.init()
pygame.init()
#initiate the function
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
display_width = 800
display_length = 800
gameDisplay = pygame.display.set_mode((display_width,display_length))
pygame.display.set_caption('slither')
font = pygame.font.SysFont(None,35)
clock = pygame.time.Clock()
FPS = 30

#Background Image
bgimg = pygame.image.load("snake.png").convert_alpha()
bgimg = pygame.transform.scale(bgimg, (display_width,display_length)).convert_alpha()
#endimg = pygame.image.load("images.jpeg").convert_alpha()
#endimg = pygame.transform.scale(bgimg, (display_width,display_length)).convert_alpha()
pygame.mixer.music.load("Home_Base_Groove.mp3")
pygame.mixer.music.play()
#import pygame
#def plotsnake(gameWindow, color,snake_list, block_size):
#	for x,y in snake_list:
#		pygame.draw.rect(gameWindow, black, [snake_list, block_size, block_size])
#snake_list = []
#snake_head = []
#snake_head.append(lead_x)
#snake_head.append(lead_y)
#snake_list.append(snake_head)
#snake_length = 1
#snake_length =+ 5
#if snake_list > snake_length:
#	del snake_list[0	
def snake(gameDisplay, color,snakelist, block_size):
		for x,y in snakelist:
			pygame.draw.rect(gameDisplay,color,[x,y,block_size,block_size])
def message_to_screen(msg,color):
	screen_text = font.render(msg,True,red)
	gameDisplay.blit(screen_text, [150,50])
def text_screen(text,color,x,y):
	font = pygame.font.SysFont(None,50)
	screen_text = font.render(text,True,color)
	gameDisplay.blit(screen_text,[x,y])
def welcome():
	gameExit = False
	while not gameExit:
		gameDisplay.fill((210,120,230))
		text_screen("Welcome!!",black,300,280)
		text_screen("Press Space To Play",black,220,320)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pygame.mixer.music.load("Bomber_Sting.mp3")
					pygame.mixer.music.play()
					gameLoop()	
		pygame.display.update()
		clock.tick(60)		
#def afterGame():
#	
#	while gameOver == True:
#		gameDisplay.fill(black)
#		message_to_screen("Game over,press C to play again or Q to quit", red)
#		pygame.display.update()
#
#		for event in pygame.event.get():
#			if event.type == pygame.KEYDOWN:
#				if event.type == pygame.K_q:
#					gameExit = True
#					gameOver = False
#				if event.type == pygame.K_c:
#					pass
def gameLoop():
	#check if highscore file exists
	if(not os.path.exists("highscore.txt")):
		with open("highscore.txt", "w") as f:
			f.write("0")
	#reading of highscore 
	with open("highscore.txt", "r") as f:
		hiscore = f.read()
	#gameExit is a variable created in game 
	#we have a game loss and this is a game exit
	#gameExit = False
	#gameOver = False
	#we have a game loss and this is a game exit
	gameExit = False
	gameOver = False
	Score = 0
	#variable for block leading the snake
	block_size = 10
	lead_x = display_length/2
	lead_y = display_width/2
	lead_x_change = 0
	lead_y_change = 0
	dx = 10
	#round off figure to match snake with apple completely - block_size)/10.0)*10.0
	randappleX = round(random.randrange(0,display_width - block_size)/10.0)*10.0
	randappleY = round(random.randrange(0,display_length - block_size)/10.0)*10.0
	snakelist = []
	snakelength = 1
	while not gameExit:
		while gameOver == True:
			#gameDisplay.blit(endimg, (0, 0)) ----------------------------------problem
			#pygame.mixer.music.load("Choose_Your_Path_Sting.mp3") -------------problem
			#pygame.mixer.music.play() -----------------------------------------problem
			#writing of hisocre
			with open("highscore.txt", "w") as f:
				f.write(str(hiscore))
			gameDisplay.fill(white)
			message_to_screen("Game Over, press C to play again or Q to quit.", white)
			text_screen("Score: " +str(Score),green,350,350)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						#pygame.quit()
						gameExit = True
						gameOver = False
					if event.key == pygame.K_c:
						#gameLoop()
						welcome()					
		for event in pygame.event.get():
			pygame.init()
			#print(event)
			if event.type == pygame.QUIT:
				gameExit = True 
			if event.type == pygame.KEYDOWN:
				if event.key  == pygame.K_LEFT:
					lead_x_change -= dx
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT:
					lead_x_change += dx
					lead_y_change = 0
				elif event.key  == pygame.K_DOWN:
					lead_y_change += dx
					lead_x_change = 0
				elif event.key == pygame.K_UP:
					lead_y_change -= dx
					lead_x_change = 0
				elif event.key == pygame.K_RETURN:
					Score += 10
			#for stopping snake being unpressed and run for pressed buttons(lead_x_change = 0)
			#if event.type == pygame.KEYUP:
			#	if event.key  == pygame.K_LEFT or event.key == pygame.K_RIGHT:
			#		lead_x_change = 0
			#	if event.key  == pygame.K_UP or event.key == pygame.K_DOWN:
			#		lead_y_change = 0		
			#creating boundaries for snake.
			#condition to fail gameOver = True
			if lead_x < 0 or lead_x>= display_width or lead_y < 0 or lead_y>= display_length:
				#gameExit = True 
				#guess why? because it will end ...
				#gameDisplay.blit(endimg, (0, 0))
				#pygame.mixer.music.load("Choose_Your_Path_Sting.mp3")
				#pygame.mixer.music.play()
				gameOver = True
		lead_x += lead_x_change
		lead_y += lead_y_change	
		#gameDisplay.fill(white)
		gameDisplay.blit(bgimg, (0, 0))
		text_screen("Score:"+str(Score) + "  Highscore:"+str(hiscore),red,5,5)
		#pygame.draw.rect()
		#draw a rectangle shape
		#rect(Surface, color, Rect, width=0) -> Rec
		#pygame.draw.rect(gameDisplay, green, [lead_x,lead_y,block_size,block_size])
		pygame.draw.rect(gameDisplay, red, [randappleX, randappleY, block_size, block_size])
		#draw a rect at x=200, y=200, and 50*50 pixels
		#gameDisplay.fill(red, rect = [200, 200, 50, 50])
		snake(gameDisplay, green, snakelist, block_size)
		snakehead = []
		snakehead.append(lead_x)
		snakehead.append(lead_y)
		snakelist.append(snakehead)
		print(snakelist)
		print(snakelength)
		if len(snakelist) > snakelength:
			del snakelist[0]
		for eachSegment in snakelist[:-1]:
			if eachSegment == snakehead:
				gameOver = True	
		pygame.display.update()
		if lead_x == randappleX and lead_y == randappleY:
			#print("slither")
			randappleX = round(random.randrange(0,display_width - block_size)/10.0)*10.0
			randappleY = round(random.randrange(0,display_length - block_size)/10.0)*10.0
			Score += 10
			snakelength += 1
			if Score > int(hiscore): #int because highscore file is read in strings
				#print(hiscore)
				hiscore = Score
		clock.tick(FPS)
	#message_to_screen("You Lose, get outside you fool", red)
	#pygame.display.update()
	#time.sleep(2)
	pygame.quit()
#gameLoop()
welcome()