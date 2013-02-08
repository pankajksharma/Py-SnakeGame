import pygame, sys, random
from pygame.locals import *

from basics import snake,point,board, food
from basics.direction import Direction

def encrypt_snake(snake):
	"""Returns encrpted Body list to send over netowrk."""
	enc_data = "%%body%%"
	for point in snake.get_body_points():
		enc_data += str(point.get_x()) + "%%sep_xy%%"
		enc_data += str(point.get_y())
		enc_data += "%%eop%%"
	enc_data += "%%body%%"
	enc_data += "%%dir%%"
	enc_data += snake.get_direction()
	enc_data += "%%dir%%"
	enc_data += "%%color%%"
	enc_data += snake.get_color()
	enc_data += "%%color%%"
	return enc_data

def get_snake_points(enc_data):
	"""Returns Snake object for given encypted string."""
	body_list = []
	for points in enc_data.split("%%body%%")[1].split("%%eop%%")[:-1]:
		x_y = points.split("%%sep_xy%%")
		body_list.append(point.Point(int(x_y[0]), int(x_y[1])))
	return body_list

def get_snake_direction(enc_data):

	return enc_data.split("%%dir%%")[1]

def get_snake_color(enc_data):

	return enc_data.split("%%color%%")[1]

def get_food_location():
	"""Returns random x and y coordinates for food."""
	return (random.randint(0,20), random.randint(0,15))

##First Snake
point1 = point.Point(0,0)
point2 = point.Point(0,1)
point3 = point.Point(0,2)

snake1 = snake.Snake([point1, point2, point3], Direction.RIGHT)

snake_food = food.Food(20,15)

#PyGame Variables
pygame.init()

FPS = 6
GAME_OVER = False
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Snakes')

myfont = pygame.font.SysFont("Comic Sans MS", 30)
game_over_text = myfont.render("Game Over!", 1, (0,0,0))

WHITE = (255, 255, 255)
snake_body = pygame.image.load('imgs/snake/'+snake1.get_color()+'/snake_body.png')
snake_mouth_icon = {}
snake_mouth_icon['yellow'] =  {
			'right' : pygame.image.load('imgs/snake/yellow/snake_mouth_right.gif'),
			'left' : pygame.image.load('imgs/snake/yellow/snake_mouth_left.gif'),
			'up' : pygame.image.load('imgs/snake/yellow/snake_mouth_up.gif'),
			'down' : pygame.image.load('imgs/snake/yellow/snake_mouth_down.gif'),
		}
snake_food_icon = pygame.image.load('imgs/frog.png')

#Networking Part


while True:
	#snake_mouth = pygame.image.load('imgs/snake/'+snake1.get_color()+'/snake_mouth_'+snake1.get_direction()+'.gif')
	DISPLAYSURF.fill(WHITE)
	snake_body_points = snake1.get_body_points()
	snake_mouth_point = snake_body_points[-1]
	enc_data = encrypt_snake(snake1)
	#print enc_data
	#print snake_body_points == get_snake_points(enc_data),
	#print get_snake_direction(enc_data), get_snake_color(enc_data)
	print snake_food
	for body_point in snake_body_points[:-1]:
		DISPLAYSURF.blit(snake_body, (20*body_point.get_x(), 20*body_point.get_y()))
	DISPLAYSURF.blit(snake_mouth_icon[snake1.get_color()][snake1.get_direction()], 
		(20*snake_mouth_point.get_x(), 20*snake_mouth_point.get_y()))
	DISPLAYSURF.blit(snake_food_icon, (20*snake_food.get_x(), 20*snake_food.get_y()))
	#direction = random.choice([0,1,3,4])
	#print direction
	
	key_pressed = False
	if snake1.has_eaten_food(snake_food):
		snake_food.update_position()
		snake1.grow_snake()

	if snake1.is_bitten_by_itself():
		GAME_OVER = True

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == KEYUP:
			if event.key == K_RIGHT:
				snake1.update_direction(Direction.RIGHT)
			elif event.key == K_LEFT:
				snake1.update_direction(Direction.LEFT)
			elif event.key == K_UP:
				snake1.update_direction(Direction.DOWN)
			elif event.key == K_DOWN:
				snake1.update_direction(Direction.UP)
			if not GAME_OVER:
				snake1.move_snake()
				key_pressed = True

	if not GAME_OVER and not key_pressed: 
		snake1.move_snake()

	if GAME_OVER:
		DISPLAYSURF.blit(game_over_text, (100, 100))
		break
	pygame.display.update()
	fpsClock.tick(FPS)
