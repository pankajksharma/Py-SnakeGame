import pygame, sys, random
from pygame.locals import *

from basics.mode import Mode
from basics.colors import Colors as color
from basics.direction import Direction
from game import SnakeGame
from network.thread import ClientListeningThread, DataSendThread

class MultiPlayerServer(SnakeGame):
	"""Server Class for Multi Player Mode."""
	def __init__(self, name, server, min_players, FPS=5, scale=20):
		SnakeGame.__init__(self, name, min_players)
		self.FPS = FPS
		self.scale = scale
		self.server = server
		self.client_snake = {}

	def send_coordinates(self):
		"""Send snakes' coordinates to Clients."""
		data_sending_thread = DataSendThread(self.server, self.client_snake, self.food)
		data_sending_thread.start()

	def listen_for_inputs(self):
		"""Listens for input from clients."""
		print 'listening_for_inputs'
		for client in self.client_snake:
			ClientListeningThread(client, self.client_snake[client]).start()

	def begin_game(self):
		"""Draws vaious objects and makes game move."""
		self.do_initial_config()
		waiting_for_clients_text = self.font.render("Waiting for Min Clients.",1, color.BLACK)
		fpsClock = pygame.time.Clock()
		GAME_OVER = False
		input_listening = False

		while True:
			self.surface.fill(color.WHITE)
			self.draw_board()
			self.draw_food()
			self.draw_snakes()

			if self.server.get_connected_clients_count() < self.board.get_min_players_count():
				self.surface.blit(waiting_for_clients_text, (self.res[0]/2-50, self.res[1]/2-50))
				self.server.send_data_to_all_clients("waiting_for_min_clients")		
			else:
				for snake in self.board.get_snakes():
					if snake.is_bitten_by_itself() or snake.has_hit_board_wall(self.board):
						temp_snake = self.get_snake(random.choice(range(3)))
						snake.update_snake(temp_snake.get_body_points(), temp_snake.direction)

					if snake.has_eaten_food(self.food):
						self.food.update_position()
						snake.grow_snake()
					snake.move_snake()

			#Only add snakes if less than total number
			if self.server.get_connected_clients_count() <= self.board.get_min_players_count():
				for client in self.server.get_connected_clients():
					if client not in self.client_snake:
						self.client_snake[client] = self.get_snake(self.board.get_no_of_snakes())
						self.board.add_snake(self.client_snake[client])

				if not input_listening and self.server.get_connected_clients_count() == self.board.get_min_players_count():
					self.send_coordinates()
					self.listen_for_inputs()
					input_listening = True

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.update()
			fpsClock.tick(self.FPS)