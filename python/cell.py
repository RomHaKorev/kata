import os
import random
from enum import Enum

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *

import rules

RESOURCES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")

def pickImage():
	return random.choice([os.path.join(RESOURCES_PATH, f) for f in os.listdir(RESOURCES_PATH) if os.path.isfile(os.path.join(RESOURCES_PATH, f))])


class CellState(Enum):
	Dead = False
	Alive = True

class Cell(QGraphicsItem):
	def __init__(self, x, y):
		super(QGraphicsItem, self).__init__()
		self.image = QPixmap(pickImage()).scaled(Cell.cellSize().toSize(), transformMode =Qt.SmoothTransformation)
		self.setX(x * Cell.cellSize().width())
		self.setY(y * Cell.cellSize().height())
		self._state = random.choice([False, True])
		self._nextState = None
		
		self.animation_live = QVariantAnimation()
		self.animation_live.setStartValue(0.0)
		self.animation_live.setEndValue(1.0)
		self.animation_live.setDuration(1000)
		self.animation_live.setEasingCurve(QEasingCurve.InOutCirc)

		self.animation_die = QVariantAnimation()
		self.animation_die.setStartValue(1.0)
		self.animation_die.setEndValue(0.0)
		self.animation_die.setDuration(1000)
		self.animation_die.setEasingCurve(QEasingCurve.InOutCirc)

		self.animation_live.valueChanged.connect(lambda value: self.setOpacity(value))
		self.animation_die.valueChanged.connect(lambda value: self.setOpacity(value))

	def boundingRect(self):
		return QRectF(QPointF(0, 0), Cell.cellSize())

	def paint(self, painter, option, widget):
		#if self._state == True:
		painter.drawPixmap(0, 0, self.image)

	@classmethod
	def cellSize(cls):
		return QSizeF(20, 20)


	def isAlive(self):
		return self._state

	def evaluateNextState(self, aliveneighbours):

		self._nextState = rules.evaluate(self._state, aliveneighbours)

		if self._state:
			self._nextState = (2 <= aliveneighbours <= 3)
			return

		self._nextState = aliveneighbours == 3

	def applyNextState(self):
		if self._state != self._nextState:
			if self._nextState:
				self.animation_live.start()
			else:
				self.animation_die.start()
		self._state = self._nextState
		self.update()