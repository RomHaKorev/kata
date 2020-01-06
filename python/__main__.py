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
	def __init__(self, position):
		super().__init__()
		self.image = QPixmap(pickImage()).scaled(Cell.cellSize().toSize(), transformMode =Qt.SmoothTransformation)
		self.setX(position.x() * Cell.cellSize().width())
		self.setY(position.y() * Cell.cellSize().height())
		self.state = random.choice([CellState.Dead, CellState.Alive])
		
	def boundingRect(self):
		return QRectF(QPointF(0, 0), Cell.cellSize())

	def paint(self, painter, option, widget):
		if self.state == CellState.Alive:
			painter.drawPixmap(0, 0, self.image);

	@classmethod
	def cellSize(cls):
		return QSizeF(20, 20)

class GameModel(QGraphicsScene):
	def __init__(self, rowCount, columnCount, parent=None):
		w = rowCount * Cell.cellSize().width()
		h = columnCount * Cell.cellSize().height()
		super().__init__(0, 0, w, h, parent)

		self.cells = list()
		for row in range(rowCount):
			for column in range(columnCount):
				c = Cell(QPointF(row, column))
				self.addItem(c)
				self.cells.append(c)




class GameView(QGraphicsView):
	def __init__(self, parent=None):
		super().__init__(parent)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = GameModel(10, 10)
    view = QGraphicsView()
    view.setScene(model)
    view.show()
    #ex.start_card_holder()
    sys.exit(app.exec_())