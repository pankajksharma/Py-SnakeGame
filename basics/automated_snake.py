from snake import Snake
from direction import Direction

class AutoMatedSnake(Snake):
	"""Class for Automated Snake."""
	def __init__(self, snake_id, body_points, direction, color="yellow"):
		Snake.__init__(self, snake_id, body_points, direction, color)

	def get_auto_mated_direction(self, food):
		if food.get_x() < self.get_mouth_point().get_x():
			return Direction.LEFT
		elif food.get_x() > self.get_mouth_point().get_x():
			return Direction.RIGHT
		elif food.get_y() < self.get_mouth_point().get_y():
			return Direction.DOWN
		else:
			return Direction.UP