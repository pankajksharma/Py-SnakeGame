import pygame, sys, random
from pygame.locals import *

from basics import board, point, food

from basics.mode import Mode
from basics.colors import Colors as color
from basics.direction import Direction
from game import SnakeGame

class SinglePlayerGame(SnakeGame):
	"""Single Player Mode."""
	def __init__(self, name, snake, FPS=5, scale=20, LIVES=3):
		SnakeGame.__init__(self, name)
		self.snake = snake
		self.FPS = FPS
		self.scale = scale
		self.lives_remaining = LIVES
		self.score = 0

	def draw_snake(self):
		"""Draws Snake on Board."""
		snake_body_points = self.snake.get_body_points()
		color = self.snake.get_color()
		for point in snake_body_points[:-1]:
			self.surface.blit(self.snake_body_icon[color], (point.get_x()*self.scale, point.get_y()*self.scale))
		snake_mouth = snake_body_points[-1]
		self.surface.blit(self.snake_mouth_icon[color][self.snake.get_direction()], (snake_mouth.get_x()*self.scale, snake_mouth.get_y()*self.scale))

	def draw_lives_and_score(self):
		"""Draws Lives remaining and Score."""
		score = self.font2.render("Score: "+ str(self.score), 1, color.BLACK)
		lives_remaining = self.font2.render(' x '+str(self.lives_remaining), 1, color.BLACK)
		self.surface.blit(score, (20,20))
		self.surface.blit(self.lives_icon, (20,40))
		self.surface.blit(lives_remaining, (40,40))

	def is_new_high_score(self):
		"""Returns True if a new high score is created."""
		high_score = int(open('data/high_score.txt', 'r').read())
		if self.score > high_score:
			open('data/high_score.txt', 'w').write(str(self.score))
			return True
		return False

	def begin_game(self):
		self.do_initial_config()
		self.board.add_snake(self.snake)
		fpsClock = pygame.time.Clock()
		GAME_OVER = False
		is_new_high_score = False

		while True:
			key_pressed = False
			self.surface.fill(color.WHITE)
			self.draw_board()
			self.draw_snake()
			self.draw_food()
			self.draw_lives_and_score()

			if self.snake.is_bitten_by_itself() or self.snake.has_hit_board_wall(self.board):
				if self.lives_remaining > 0:
					self.lives_remaining -= 1
					if self.lives_remaining != 0:
						temp_snake = self.get_snake(random.choice(range(3)))
						self.snake.update_snake(temp_snake.get_body_points(), temp_snake.direction)
						self.score -= 50
					else:
						is_new_high_score = self.is_new_high_score()

			if self.lives_remaining == 0:
				GAME_OVER = True

			if self.snake.has_eaten_food(self.food):
				self.food.update_position()
				self.snake.grow_snake()
				self.score += 20

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

				elif not GAME_OVER and event.type == KEYDOWN:
					if event.key == K_RIGHT:
						self.snake.update_direction(Direction.RIGHT)
					elif event.key == K_LEFT:
						self.snake.update_direction(Direction.LEFT)
					elif event.key == K_UP:
						self.snake.update_direction(Direction.DOWN)
					elif event.key == K_DOWN:
						self.snake.update_direction(Direction.UP)
					if not GAME_OVER:
						self.snake.move_snake()
						key_pressed = True

			if not GAME_OVER and not key_pressed: 
				self.snake.move_snake()

			if GAME_OVER:
				self.surface.blit(self.game_over_text, (self.res[0]/2-50, self.res[1]/2-50))
				if is_new_high_score:
					self.surface.blit(self.new_high_score_text, (self.res[0]/2-30, self.res[1]/2))
				if event.type == KEYDOWN:
					if event.key == K_RETURN or event.key == K_ESCAPE:
						return True	
	
			pygame.display.update()
			fpsClock.tick(self.FPS)