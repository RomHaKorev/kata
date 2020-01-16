class Position(object):
	def __init__(self, x, y):
		self.x, self.y = x, y

	def __eq__(self, other):
		if type(other) is not Position:
			return False
		return self.x == other.x and self.y == other.y

