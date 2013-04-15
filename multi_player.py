import pygame, sys
from pygame.locals import *
from basics import point, snake, food
from basics.mode import Mode
from basics.colors import Colors as color
from basics.direction import Direction
from game import SnakeGame
from network.thread import ClientThread

class MultiPlayerGame(SnakeGame):
	"""Class for Multi Player Mode."""
	def __init__(self, name, client, min_players, FPS=5, scale=20):
		SnakeGame.__init__(self, name, min_players)
		self.FPS = FPS
		self.scale = scale
		self.client = client

	def listen_for_snakes_and_food(self):
		"""Listens for snake data over network."""
		listening_thread = ClientThread(self.client, self.board, self.food)
		listening_thread.start()

	def send_to_server(self, direction):
		enc_mssg = "%%dir%%"+direction+"%%dir %%"
		self.client.socket.sendall(enc_mssg)
		
	def begin_game(self):
		"""Draws vaious objects and makes game move."""
		self.do_initial_config()
		waiting_for_clients_text = self.font.render("Waiting for Min Clients.",1, color.BLACK)
		fpsClock = pygame.time.Clock()
		GAME_OVER = False
		self.listen_for_snakes_and_food()

		while True:
			key_pressed = False
			self.surface.fill(color.WHITE)
			self.draw_board()
			self.draw_food()
			self.draw_snakes()

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

				if event.type == KEYDOWN:
					if event.key == K_UP:
						self.send_to_server('up')
					elif event.key == K_DOWN:
						self.send_to_server('down')
					elif event.key == K_LEFT:
						self.send_to_server('left')
					elif event.key == K_RIGHT:
						self.send_to_server('right')

			pygame.display.update()
			fpsClock.tick(self.FPS)