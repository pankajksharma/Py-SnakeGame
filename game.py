import pygame, sys
from pygame.locals import *

from basics import board, point, food, snake
from basics.direction import Direction
from basics.mode import Mode
from basics.colors import Colors as color

class Game(object):
	"""Wrapper class to initialize game."""
	def __init__(self, name):
		self.name = name

	def init(self, res, flags=0, depth=0):
		"""Begins Execution."""
		self.res = res
		pygame.display.set_caption(self.name)
		self.surface = pygame.display.set_mode(res, flags, depth)
		self.font = pygame.font.SysFont("Ubuntu", 30)
		self.font2 = pygame.font.SysFont("Ubuntu", 15)
		self.game_over_text = self.font.render("Game Over!", 1, color.BLACK)
		self.new_high_score_text = self.font2.render("New High Score.",1,color.BLACK)

class SnakeGame(Game):
	"""Wrapper class for Snake Game."""

	def __init__(self, name, min_players=1):
		Game.__init__(self, name)
		self.surface = None
		self.min_players = min_players
		pygame.init()

	def get_snake(self, snake_id):
		if snake_id == 0:
			return snake.Snake(snake_id, [point.Point(1,1), point.Point(2,1), point.Point(3,1)], Direction.RIGHT, "yellow")
		elif snake_id == 1:
			max_x = self.board.get_width()-1
			return snake.Snake(snake_id, [point.Point(max_x-1,1), point.Point(max_x-2,1), point.Point(max_x-3,1)], Direction.LEFT, "green")
		elif snake_id == 2:
			mid_x = self.board.get_width()/2
			max_y = self.board.get_height()-1
			return snake.Snake(snake_id, [point.Point(mid_x, max_y-1), point.Point(mid_x,max_y-2), point.Point(mid_x, max_y-3)], Direction.DOWN, "red")

	def load_icons(self):
		"""Loads icons for the game."""
		self.board_wall_icon = pygame.image.load('imgs/wall.png')
		self.frog_icon = pygame.image.load('imgs/frog.png')
		self.lives_icon = pygame.image.load('imgs/heart.png')
		self.high_score_icon = pygame.image.load('imgs/highscore.png')
		self.snake_body_icon = {
			'yellow' : pygame.image.load('imgs/snake/yellow/snake_body.png'),
			'green' : pygame.image.load('imgs/snake/green/snake_body.png'),
			'red' : pygame.image.load('imgs/snake/red/snake_body.png')
		}
		self.snake_mouth_icon = {}
		self.snake_mouth_icon['yellow'] =  {
			'right' : pygame.image.load('imgs/snake/yellow/snake_mouth_right.gif'),
			'left' : pygame.image.load('imgs/snake/yellow/snake_mouth_left.gif'),
			'up' : pygame.image.load('imgs/snake/yellow/snake_mouth_up.gif'),
			'down' : pygame.image.load('imgs/snake/yellow/snake_mouth_down.gif'),
		}
		self.snake_mouth_icon['green'] =  {
			'right' : pygame.image.load('imgs/snake/green/snake_mouth_right.gif'),
			'left' : pygame.image.load('imgs/snake/green/snake_mouth_left.gif'),
			'up' : pygame.image.load('imgs/snake/green/snake_mouth_up.gif'),
			'down' : pygame.image.load('imgs/snake/green/snake_mouth_down.gif'),
		}
		self.snake_mouth_icon['red'] =  {
			'right' : pygame.image.load('imgs/snake/red/snake_mouth_right.gif'),
			'left' : pygame.image.load('imgs/snake/red/snake_mouth_left.gif'),
			'up' : pygame.image.load('imgs/snake/red/snake_mouth_up.gif'),
			'down' : pygame.image.load('imgs/snake/red/snake_mouth_down.gif'),
		}
		
	def do_initial_config(self):
		"""Does all the Initializion required."""
		self.food = food.Food(self.res[0]/self.scale, self.res[1]/self.scale)
		self.init_point = point.Point(0, 0)
		self.board = board.Board(self.res[0]/self.scale, self.res[1]/self.scale, self.init_point, self.min_players)
		self.load_icons()

	def draw_board(self):
		"""Initializes and draw board object."""
		for i in range(0, self.res[1]/self.scale):
			self.surface.blit(self.board_wall_icon, (self.board.get_init_point().get_x()*self.scale, i*self.scale))
			self.surface.blit(self.board_wall_icon, ((self.board.get_width()-1)*self.scale, i*self.scale))
		for i in range(0, self.res[0]/self.scale):
			self.surface.blit(self.board_wall_icon, ( i*self.scale, self.board.get_init_point().get_y()))
			self.surface.blit(self.board_wall_icon, ( i*self.scale, (self.board.get_height()-1)*self.scale))
	
	def draw_food(self):
		"""Draws snake food."""
		self.surface.blit(self.frog_icon, (self.food.get_x()*self.scale, self.food.get_y()*self.scale))


class StartGameScreen(Game):
	"""Start Screen for Game."""
	def __init__(self, name):
		Game.__init__(self, name)
		self.surface = None
		pygame.init()

	def get_game_mode(self, options):
		"""Returns game Mode."""
		game_mode_pos = self.draw_start_screen(options)[1]
		if game_mode_pos < 130:
			return Mode.SINGLEPLAYER
		elif game_mode_pos > 200:
			return Mode.MULTIPLAYER_SERVER
		else:
			return Mode.MULTIPLAYER_CLIENT

	def draw_start_screen(self, options):
		"""Draws Start Screen."""
		start_options = []
		for option in options:
			start_options.append(self.font.render(option, 1, color.WHITE))
		bg = pygame.image.load('imgs/bg.png')
		option_triangle = pygame.image.load('imgs/option-triangle.png')
		cur_option = 0
		while True:
			self.surface.fill(color.START_SCREEN_GREEN)
			self.surface.blit(bg, (0, 0))
			i = 0
			for start_option in start_options:
				self.surface.blit(start_option, (50,100+50*i))
				i += 1

			self.surface.blit(option_triangle, (20, 105+50*cur_option))

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == MOUSEBUTTONUP:
					return event.pos
				elif event.type == KEYDOWN:
					if event.key == K_UP:
						cur_option -= 1
					elif event.key == K_DOWN:
						cur_option += 1
					elif event.key == K_RETURN:
						return (100, 105+50*cur_option)
			cur_option %= 3

			pygame.display.update()	