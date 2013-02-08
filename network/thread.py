import threading
import os,sys,re
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from basics import point,snake
from basics.direction import Direction

class ServerThread(threading.Thread):
	"""Class to implement threading for listening for clients."""
	def __init__(self, server):
		self.server = server
		self.socket = server.get_socket()
		threading.Thread.__init__(self)

	def run(self):
		while 1:
			con,client = self.socket.accept()
			self.server.add_client(con)

class DataSendThread(threading.Thread):
	"""Thread for sending data parallely to all clients."""
	def __init__(self, server, client_snake, food):
		self.server = server
		self.client_snake = client_snake
		self.food = food
		threading.Thread.__init__(self)

	def encrypt_snake(self, snake):
		"""Returns encrpted snake object to send over netowrk."""
		enc_data = "%%snake-"+str(snake.get_id())+"%%"
		enc_data += "%%body%%"
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
		enc_data += "%%eosnake %%"
		return enc_data

	def encrypt_food(self):
		"""Returns encrpted food object to send over netowrk."""
		enc_data = "%%food%%"
		enc_data += "%%pos%%"
		enc_data += str(self.food.get_x())
		enc_data += "%%sep_xy%%"
		enc_data += str(self.food.get_y())
		enc_data += "%%pos%%"
		enc_data += "%%eofood %%"
		return enc_data

	def run(self):
		while True:
			for client in self.client_snake:
				self.server.send_data_to_all_clients(self.encrypt_snake(self.client_snake[client]))
			self.server.send_data_to_all_clients(self.encrypt_food())

class ClientListeningThread(threading.Thread):
	def __init__(self, client, snake):
		self.client = client
		self.snake = snake
		threading.Thread.__init__(self)
		self.direction = {
			'right' : Direction.RIGHT,
			'left' : Direction.LEFT,
			'down' : Direction.UP,
			'up' : Direction.DOWN
		}

	def decrypt_for_direction(self, enc_data):
		direction = enc_data.split("dir")[1]
		return self.direction[direction.replace('%', '')]

	def run(self):
		enc_data = ''

		while True:
			enc_data += self.client.recv(128)
			for directions in re.findall("%%dir[^ ]*dir %%", enc_data):
				direction = self.decrypt_for_direction(directions)
			#	print direction
				enc_data = enc_data[:enc_data.index(directions)]
			self.snake.update_direction(direction)

class ClientThread(threading.Thread):
	def __init__(self, client, board, food):
		self.client = client
		self.board = board
		self.food = food
		self.direction = {
			'right' : Direction.RIGHT,
			'left' : Direction.LEFT,
			'down' : Direction.UP,
			'up' : Direction.DOWN
		}
		threading.Thread.__init__(self)

	def decrypt_for_snake(self, enc_data):
		"""Returns Snake object for given encypted string."""
		snake_id = int(enc_data[8])
		body_list = []
		for points in enc_data.split("%%body%%")[1].split("%%eop%%")[:-1]:
			x_y = points.split("%%sep_xy%%")
			body_list.append(point.Point(int(x_y[0]), int(x_y[1])))
		direction = self.direction[enc_data.split("%%dir%%")[1]]
		color = enc_data.split("%%color%%")[1]

		psnake = self.board.get_snake(snake_id)
		if psnake:
			self.board.update_snake(psnake, body_list, direction)
		else:
			self.board.add_snake(snake.Snake(snake_id, body_list, direction, color))
		

	def decrypt_for_food(self, enc_data):
		"""Updates food object."""
		food_point = enc_data.split("%%pos%%")[1].split("%%sep_xy%%")
		self.food.set_x(int(food_point[0]))
		self.food.set_y(int(food_point[1]))

	def run(self):
		enc_data = ""
		while True:
			old_data = ""
			enc_data += self.client.recv(1024)
			for snake in re.findall("%%snake-[^ ]*eosnake %%", enc_data):
				self.decrypt_for_snake(snake)
				enc_data =  enc_data[enc_data.index(snake):]
				
			for food in re.findall("%%food[^ ]*eofood %%", enc_data):
				self.decrypt_for_food(food)
				enc_data = enc_data[enc_data.index(food):]