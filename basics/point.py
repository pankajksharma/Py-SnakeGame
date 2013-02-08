class Point(object):
	"""Class for Coordinates."""
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def get_x(self):
		"""Returns x Coordinate."""
		return self.x

	def get_y(self):
		"""Returns y Coordinate."""
		return self.y

	def set_x(self, new_x):
		"""Sets x Coordinate."""
		self.x = new_x

	def set_y(self, new_y):
		"""Sets y Coordinate."""
		self.y = new_y

	def __eq__(self, other):
		return self.get_x() == other.get_x() and self.get_y() == other.get_y()

	def __str__(self):
		"""String Function."""
		return '('+str(self.x)+', '+str(self.y)+')'

	def __repr__(self):
		"""Repr Function."""
		return '('+str(self.x)+', '+str(self.y)+')'