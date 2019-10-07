from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Block(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal(int, int)
    def __init__(self, x, y):
        super(Block, self).__init__()
        self.setFixedSize(QSize(25, 25))
        self.x = x
        self.y = y
        self.reset()

    def reset(self):
        self.is_revealed = False
        self.adjacent_nodes = 0
        self.is_mine = False
        self.update()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal()
            if self.adjacent_nodes == 0:
                self.expandable.emit(self.x, self.y)
            self.clicked.emit(self.x, self.y)

    def mouseReleaseEvent(self, e):
        self.click()