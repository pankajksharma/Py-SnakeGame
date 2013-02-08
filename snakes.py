#! /usr/bin/env python
from game import *
from basics import point, snake, board
from single_player import SinglePlayerGame
from multi_player import MultiPlayerGame
from multi_player_server import MultiPlayerServer
from basics.direction import Direction
from basics.mode import Mode

from network import server, thread, client

while True:

	GAME_NAME = "P Snakes"

	MAX_LIVES = 3

	start_screen = StartGameScreen(GAME_NAME)

	start_screen.init((400, 300), 0, 32)

	game_mode = start_screen.get_game_mode(['Single Player', 'Multi Player', 'Multi Player (as Server)'])

	if game_mode == Mode.SINGLEPLAYER:
		GAME_NAME += ' {Single Player}'
		point1 = point.Point(1,1)
		point2 = point.Point(2,1)
		point3 = point.Point(3,1)
		snake1 = snake.Snake(0, [point1, point2, point3], Direction.RIGHT, "yellow")
		game = SinglePlayerGame(GAME_NAME, snake1, 8)
		game.init((400, 300), 0, 32)
		if not game.begin_game():
			break

	elif game_mode == Mode.MULTIPLAYER_SERVER:
		GAME_NAME += ' {Server}'
		server = server.Server()
		server.initiate()
		client_listening_threads  = thread.ServerThread(server)
		client_listening_threads.start()

		game_server = MultiPlayerServer(GAME_NAME, server, 2, 8)
		game_server.init((800, 600), 0, 32)

		game_server.begin_game()

	else:
		GAME_NAME += ' {Multi Player}'
		client = client.Client('localhost', 7792)

		game = MultiPlayerGame(GAME_NAME, client, 2, 8)
		game.init((800, 600), 0, 32)

		game.begin_game()
