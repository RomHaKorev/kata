import os
import random
import sys

from enum import Enum

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *

from grid import *

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

    grid = Grid(100, 100)

    model = GameModel(grid)
    view = QGraphicsView()
    view.setScene(model)
    view.show()
    #ex.start_card_holder()
    sys.exit(app.exec_())