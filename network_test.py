from network import server, thread

game_server = server.Server("Snake Server", 7792, 3)
game_server.initiate()

client_listening_thread = thread.ServerThread(game_server)

client_listening_thread.start()

while 1:
	if len(game_server.get_connected_clients()) > 0:
		print game_server.get_connected_clients()