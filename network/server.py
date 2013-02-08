import socket
from thread import DataSendThread
class Server(object):
	"""Server class for networking."""
	def __init__(self, name='Snake Server', port_no=7792, min_clients=3):
		self.name = name
		self.port_no = port_no
		self.min_clients = min_clients
		self.connected_clients = []
		self.socket = None

	def initiate(self):
		"""Initiates Server Socket."""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('', self.port_no))
		self.socket.listen(self.min_clients)

	def get_socket(self):
		"""Returns Server Socket."""
		return self.socket

	def get_name(self):
		"""Returns Server name."""
		return self.name

	def get_port_no(self):
		"""Returns Server Port Number."""
		return self.port_no

	def get_connected_clients_count(self):
		"""Returns count of connected clients."""
		return len(self.connected_clients)

	def get_connected_clients(self):
		"""Returns a list of connected clients."""
		return self.connected_clients

	def add_client(self, client):
		"""Adds client."""
		self.connected_clients.append(client)

	def send_data_to_client(self, client, data):
		"""Sends data to particular client."""
		if client in self.connected_clients:
			client.sendall(data)
			return True
		return False

	def send_data_to_all_clients(self, data):
		"""Sends data to all connected Clients."""
		for client in self.connected_clients:
			client.sendall(data)

	def __repr__(self):
		return self.name