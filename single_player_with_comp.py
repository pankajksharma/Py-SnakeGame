import pygame, sys, random
from pygame.locals import *

from basics import board, point, food, automated_snake

from basics.mode import Mode
from basics.colors import Colors as color
from basics.direction import Direction
from single_player import SinglePlayerGame

class SinglePlayerGameWithComp(SinglePlayerGame):
	"""Single Player Mode."""
	def __init__(self, name, snake, FPS=5, scale=20, LIVES=3):
		SinglePlayerGame.__init__(self, name, snake, FPS, scale, LIVES)

	def is_new_high_score(self):
		"""Returns True if a new high score is created."""
		high_score = int(open('data/hs_vs_comp.txt', 'r').read())
		if self.score > high_score:
			open('data/hs_vs_comp.txt', 'w').write(str(self.score))
			return True
		return False
	
	def begin_game(self):
		self.do_initial_config()
		temp_snake = self.get_snake(1)
		self.automated_snake = automated_snake.AutoMatedSnake(1, temp_snake.get_body_points(), temp_snake.direction, "green")
		self.board.add_snake(self.automated_snake)
		self.board.add_snake(self.snake)
		fpsClock = pygame.time.Clock()
		GAME_OVER = False
		is_new_high_score = False

		while True:
			key_pressed = False
			self.surface.fill(color.WHITE)
			self.draw_board()
			self.draw_snakes()
			self.draw_food()
			self.draw_lives_and_score()

			if self.snake.is_bitten_by_itself() or self.snake.has_hit_board_wall(self.board):
				if self.lives_remaining > 0:
					self.lives_remaining -= 1
					if self.lives_remaining != 0:
						temp_snake = self.get_snake(random.choice(range(3)))
						self.snake.update_snake(temp_snake.get_body_points(), temp_snake.direction)
					else:
						is_new_high_score = self.is_new_high_score()

			if self.automated_snake.is_bitten_by_itself() or self.automated_snake.has_hit_board_wall(self.board):
				temp_snake = self.get_snake(random.choice(range(3)))
				self.automated_snake.update_snake(temp_snake.get_body_points(), temp_snake.direction)

			if self.lives_remaining == 0:
				GAME_OVER = True

			if self.snake.has_eaten_food(self.food):
				self.food.update_position()
				self.snake.grow_snake()
				self.score += 20

			elif self.automated_snake.has_eaten_food(self.food):
				self.food.update_position()
				self.automated_snake.grow_snake()

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
				direction = self.automated_snake.get_auto_mated_direction(self.food)
				self.automated_snake.update_direction(direction)
				self.automated_snake.move_snake()

			if GAME_OVER:
				self.surface.blit(self.game_over_text, (self.res[0]/2-50, self.res[1]/2-50))
				if is_new_high_score:
					self.surface.blit(self.new_high_score_text, (self.res[0]/2-30, self.res[1]/2))
				if event.type == KEYDOWN:
					if event.key == K_RETURN or event.key == K_ESCAPE:
						return True	
	
			pygame.display.update()
			fpsClock.tick(self.FPS)