import point

from direction import Direction

class Snake(object):
	"""Deifnes Snake Body."""
	def __init__(self, snake_id, body_points, direction, color="yellow"):
		try:
			assert(len(body_points)>=3)
		except:
			print body_points
		self.id = snake_id
		self.length = len(body_points)
		self.body_points = body_points
		self.direction = direction
		self.color = color

	def get_id(self):
		"""Returns id of snake."""
		return self.id

	def add_point(self, point):
		"""Adds point to snake Body."""
		self.body_points.append(point)

	def get_mouth_point(self):
		"""Returns Snake's mouth Coordinates."""
		return self.body_points[-1]

		
	def get_body_points(self):
		"""Returns Body points of snake."""
		return self.body_points

	def get_length(self):
		"""Returns snake's length."""
		return self.length

	def get_color(self):
		"""Returns Snake's Body color."""
		return self.color

	def update_direction(self, direction):
		"""Updates Snake Direction."""
		if abs(self.direction - direction) > 1:
			self.direction = direction

	def has_eaten_food(self, food_point):
		"""Returns True if mounth and food are at same location."""
		return self.body_points[-1] == food_point

	def is_bitten_by_itself(self):
		"""Returns True if the snake is bitten by itself."""
		body_points = self.get_body_points()
		for body_point in body_points[:-1]:
			if body_point == body_points[-1]:
				return True
		return False

	def is_bitten_by_another_snake(self, other_snake_mouth_point, other_snake_length):
		"""Returns true if Sanke's body is bitten by Another Snake."""
		if self.get_mouth_point() == other_snake_mouth_point:
			return self.get_length() < other_snake_length
		for body_point in self.get_body_points()[:-1]:
			if body_point == other_snake_mouth_point:
				return True
		return False

	def has_hit_board_wall(self, board):
		"""Returns True if snake hits the wall."""
		return self.get_mouth_point().get_x() <= board.get_init_point().get_x() or \
			   self.get_mouth_point().get_y() <= board.get_init_point().get_y() or \
			   self.get_mouth_point().get_x() >= board.get_width() - 1 or 				\
			   self.get_mouth_point().get_y() >= board.get_height() - 1

	def get_direction(self):
		"""Returns snake direction as string."""
		if self.direction == Direction.RIGHT:
			return 'right'
		elif self.direction == Direction.LEFT:
			return 'left'
		elif self.direction == Direction.UP:
			return 'down'
		else:
			return 'up'

	def grow_snake(self):
		"""Increases snake body."""
		self.length += 1
		self.body_points.insert(0, self.get_body_points()[0])

	def move_snake(self):
		"""Update the body points of snake."""
		#Remove Tail
		self.body_points.remove(self.body_points[0])
		#Update Head
		self.body_points.append(self.get_new_head())

	def get_new_head(self):
		"""Returns new head location based upon the Direction."""
		snake_head = self.body_points[-1]
		snake_new_head = point.Point(snake_head.get_x(), snake_head.get_y())
		if self.direction == Direction.RIGHT:
			snake_new_head.set_x(snake_new_head.get_x()+1)
		elif self.direction == Direction.LEFT:
			snake_new_head.set_x(snake_new_head.get_x()-1)
		elif self.direction == Direction.UP:
			snake_new_head.set_y(snake_new_head.get_y()+1)
		else:
			snake_new_head.set_y(snake_new_head.get_y()-1)
		return snake_new_head

	def update_snake(self, body_points, direction):
		"""Updates snake explicitly."""
		self.length = len(body_points)
		self.body_points = body_points
		self.direction = direction

	def __str__(self):
		print self.body_points
