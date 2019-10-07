from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .Block import Block
import math

class Hex(Block):
    def __init__(self, x, y):
        super(Hex, self).__init__(x, y)


    def createPoly(self, n, r, s):
        polygon = QPolygonF() 
        w = 360/n
        for i in range(n):
            t = w*i + s
            x = r*math.cos(math.radians(t))
            y = r*math.sin(math.radians(t))
            polygon.append(QPointF(self.width()/2 +x, self.height()/2 + y))  

        return polygon

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()
        
        if self.is_revealed:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray
        
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.setBrush(inner)

        p.drawPolygon(self.createPoly(6, 10, 10))

        if self.is_revealed == True:

            color = QColor('#03A9F4')
            node_val = ""


            if self.is_mine:
                color = QColor('#f44336')
                node_val = "X"
            elif self.adjacent_nodes > 0:
                node_val = str(self.adjacent_nodes)

            pen = QPen(color)
            p.setPen(pen)
            f = p.font()
            f.setBold(True)
            p.setFont(f)
            p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, node_val)

    def check_block(cls, grid, x, y, n):
        w = grid.itemAtPosition(y, x).widget()
        return w.is_mine and w.is_revealed