class Board(object):
	"""Game Borad"""
	def __init__(self, width, height, init_point = (0,0), min_players = 1):
		self.width = width
		self.height = height
		self.snakes = []
		self.init_point = init_point
		self.min_players = min_players

	def get_min_players_count(self):
		"""Returns Min Player Count."""
		return self.min_players

	def  get_width(self):
		"""Returns width of Borad."""
		return self.width

	def get_height(self):
		"""Returns height of Borad."""
		return self.height

	def add_snake(self, snake):
		"""Adds snake to the Borad."""
		self.snakes.append(snake)

	def get_no_of_snakes(self):
		"""Returns number of snakes on Borad."""
		return len(self.snakes)

	def get_snakes(self):
		"""Returns snakes objects present."""
		return self.snakes

	def get_init_point(self):
		"""Returns starting x,y coordinates."""
		return self.init_point

	def get_snake(self, snake_id):
		"""Returns snake object if it's present on Borad."""
		for snake in self.snakes:
			if int(snake.id) == int(snake_id):
				return snake
		return None

	def update_snake(self, snake, body_points, direction):
		"""Updates Snake."""
		snake.update_snake(body_points, direction)
