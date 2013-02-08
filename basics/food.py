import random
from point import Point

class Food(Point):
	"""Snake's Food Class."""
	def __init__(self, max_x, max_y):
		self.max_x = max_x
		self.max_y = max_y
		Point.__init__(self, *self.random_position())

	def update_position(self):
		"""Sets Food Position."""
		new_pos = self.random_position()
		self.set_x(new_pos[0])
		self.set_y(new_pos[1])

	def random_position(self):
		"""Returns Random Position for Food."""
		return (random.randint(1, self.max_x-2), random.randint(1,self.max_y-2))