
from cell import *
from position import *

class Grid(object):
	def __init__(self, rowCount, columnCount):
		self.rowCount = rowCount
		self.columnCount = columnCount

		self.cells = list()
		for row in range(rowCount):
			l = list()
			for column in range(columnCount):
				c = Cell(row, column)
				l.append(c)
			self.cells.append(l)

	def __iter__(self):
		for row in self.cells:
			for cell in row:
				yield cell

	def applyOnEachCell(self, callback):
		for x in range(self.rowCount):
			self.applyEachColumnOfRow(x, callback)

	def applyEachColumnOfRow(self, row, callback):
		for column in range(self.columnCount):
			callback(Position(row, column))
	

	def countNeighbourAt(self, position, positionNeighbour):
		if position == positionNeighbour:
			return 0
		if self.cells[positionNeighbour.x][positionNeighbour.y].isAlive():
			return 1
		return 0

	def countEachNeighboursWithX(self, position, xNeighbour):
		topNeighbour = max(0, position.y - 1)
		bottomNeighbour = min(self.columnCount - 1, position.y + 1)
		aliveneighbours = 0
		for yNeighbour in range(topNeighbour, bottomNeighbour + 1):
			aliveneighbours += self.countNeighbourAt(position, Position(xNeighbour, yNeighbour))
		return aliveneighbours

	def countEachNeighbours(self, position):
		leftNeighbour = max(0, position.x - 1)
		rightNeighbour = min(self.rowCount - 1, position.x + 1)
		aliveneighbours = 0
		for xNeighbour in range(leftNeighbour, rightNeighbour + 1):
			aliveneighbours += self.countEachNeighboursWithX(position, xNeighbour)
		return aliveneighbours

	def changeCellStatus(self, position):
		cell = self.cells[position.x][position.y]
		aliveneighbours = self.countEachNeighbours(position)
		cell.evaluateNextState(aliveneighbours)

	def update(self):
		self.applyOnEachCell(self.changeCellStatus)
		self.applyOnEachCell(lambda position: self.cells[position.x][position.y].applyNextState())
