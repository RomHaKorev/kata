import os
import random
import sys

from enum import Enum

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *

RESOURCES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")

def pickImage():
	return random.choice([os.path.join(RESOURCES_PATH, f) for f in os.listdir(RESOURCES_PATH) if os.path.isfile(os.path.join(RESOURCES_PATH, f))])


class CellState(Enum):
	Dead = 0
	Alive = 1

class Cell(QGraphicsItem):
	def __init__(self, x, y):
		super().__init__()
		self.image = QPixmap(pickImage()).scaled(Cell.cellSize().toSize(), transformMode =Qt.SmoothTransformation)
		self.setX(x * Cell.cellSize().width())
		self.setY(y * Cell.cellSize().height())
		self.state = random.choice([CellState.Dead, CellState.Alive])
		
	def boundingRect(self):
		return QRectF(QPointF(0, 0), Cell.cellSize())

	def paint(self, painter, option, widget):
		if self.state == CellState.Alive:
			painter.drawPixmap(0, 0, self.image)

	@classmethod
	def cellSize(cls):
		return QSizeF(20, 20)


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

	def update(self):
		print("Update cells")


class GameModel(QGraphicsScene):
	def __init__(self, grid, parent=None):
		w = grid.rowCount * Cell.cellSize().width()
		h = grid.columnCount * Cell.cellSize().height()
		super().__init__(0, 0, w, h, parent)

		self.startTimer(1000)

		self.grid = grid
		for cell in self.grid:
			self.addItem(cell)

	def timerEvent(self, event):
		self.grid.update()

class GameView(QGraphicsView):
	def __init__(self, parent=None):
		super().__init__(parent)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    grid = Grid(10, 10)

    model = GameModel(grid)
    view = QGraphicsView()
    view.setScene(model)
    view.show()
    #ex.start_card_holder()
    sys.exit(app.exec_())