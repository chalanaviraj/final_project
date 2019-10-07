from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .Block import Block

import random, math


NUM_COLORS = {
    0: Qt.red,#red
    1: Qt.yellow,#yellow
    2: Qt.blue,#blue
    3: Qt.green#green
}

class RectColored(Block):



    def __init__(self, x, y):
        super(RectColored, self).__init__(x, y)
        self.color_value = random.randint(0, 3)

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



        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed == True:
        	#8 orange, 2 purple, 3 blue, 4 light blue, 6 green
            outer, inner = NUM_COLORS[self.color_value], NUM_COLORS[self.color_value]

            pen = QPen(outer)
            pen.setWidth(1)
            p.setPen(pen)
            p.setBrush(inner)

            p.drawPolygon(self.createPoly(15, 10, 10))

    def check_block(cls, grid, x, y, n):
        w = grid.itemAtPosition(y,x).widget()
        for xi in range(max(0, x - 1), min(x + 2, n)):
            for yi in range(max(0, y - 1), min(y + 2, n)):
                w1 = grid.itemAtPosition(yi, xi).widget()
                if (xi != x or yi != y) and w.color_value == w1.color_value and (w.is_revealed and w1.is_revealed):
                    return True
        return False