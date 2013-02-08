import socket

class Client(object):
	"""Class for Client."""
	def __init__(self, host, port_no):
		self.host = host
		self.port_no = port_no
		self.connection = None
		self.initialize()

	def initialize(self):
		"""initializes client socket."""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.host, self.port_no))


	def recv(self, buffer=512):

		return self.socket.recv(buffer)