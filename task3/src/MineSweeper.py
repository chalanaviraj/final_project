from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view.Rect import Rect
from view.Hex import Hex
from view.RectColored import RectColored
from model.Player import Player
import random, time, math, sys


GRID_DIMENSION = 8
TOTAL_MINES = 15


class MineSweeper(QMainWindow):

    def __init__(self, num_tiles, num_mines):
        super(MineSweeper, self).__init__()
        self.n = num_tiles
        self.num_mines = num_mines
        self.player = Player()
        self.setWindowTitle("Minesweeper")

        squareGame = QAction("&Square", self)
        squareGame.triggered.connect(self.generate_square_map)

        hexGame = QAction("&Hexagonal", self)
        hexGame.triggered.connect(self.generate_hex_map)

        coloredGame = QAction("&Colored", self)
        coloredGame.triggered.connect(self.generate_colored_map)

        quitGame = QAction("&Quit", self)
        quitGame.triggered.connect(self.quit_game)

        self.statusBar()

        mainMenu = self.menuBar()
        gameMenu = mainMenu.addMenu('&Game')
        gameMenu.addAction(squareGame)
        gameMenu.addAction(hexGame)
        gameMenu.addAction(coloredGame)
        gameMenu.addAction(quitGame)

        w = QWidget()

        

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.clock.setText("000")
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        self.gameStatus = 1

        vb = QVBoxLayout()
        vb.addWidget(self.clock)
        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)

        self.show()

    def clear_grid(self):
        while self.grid.count() > 0:
            item = self.grid.takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.deleteLater()

    def init_hex_map(self):
        self.clear_grid()
        for x in range(0, self.n):
            for y in range(0, self.n):
                r = Hex(x, y)
                self.grid.addWidget(r, y, x)
                r.expandable.connect(self.expand_reveal)
                r.clicked.connect(self.check_state)

    def init_colored_map(self):
        self.clear_grid()
        for x in range(0, self.n):
            for y in range(0, self.n):
                r = RectColored(x, y)
                self.grid.addWidget(r, y, x)
                r.expandable.connect(self.expand_reveal)
                r.clicked.connect(self.check_state)

    def init_square_map(self):
        self.clear_grid()
        for x in range(0, self.n):
            for y in range(0, self.n):
                r = Rect(x, y)
                self.grid.addWidget(r, y, x)
                r.expandable.connect(self.expand_reveal)
                r.clicked.connect(self.check_state)


    def reset_map(self):
        self.gameStatus = 1
        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(1000) 
        self._timer_start_nsecs = int(time.time())

        for x in range(0, self.n):
            for y in range(0, self.n):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset()

        mines = []
        for i in range(self.num_mines):
            x = random.randint(0, self.n-1)
            y = random.randint(0, self.n-1)

            if (x, y) not in mines:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_mine = True
                mines.append((x, y))

        for x in range(0, self.n):
            for y in range(0, self.n):
                w = self.grid.itemAtPosition(y, x).widget()
                w.adjacent_nodes = self.get_adjacent_nodes(x, y)

    def get_adjacent_nodes(self, x, y):
        nodes = self.get_neighbors(x, y)
        summ = 0
        for nod in nodes:
            if nod.is_mine == True:
                summ += 1
        return summ

    def update_timer(self):
        n_secs = int(time.time()) - self._timer_start_nsecs
        self.clock.setText("%03d" % n_secs)

    def set_mine_at(self, x, y):
        w = self.grid.itemAtPosition(y, x).widget()
        w.is_mine = True

    def remove_mine_from(self, x, y):
        w = self.grid.itemAtPosition(y, x).widget()
        w.is_mine = False

    def set_color(self, x, y, colorid):
        w = self.grid.itemAtPosition(y, x).widget()
        w.color_value = colorid



    def get_neighbors(self, x, y):
        lst = []

        for xi in range(max(0, x - 1), min(x + 2, self.n)):
            for yi in range(max(0, y - 1), min(y + 2, self.n)):
                lst.append(self.grid.itemAtPosition(yi, xi).widget())

        return lst

    def expand_reveal(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.n)):
            for yi in range(max(0, y - 1), min(y + 2, self.n)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.is_mine:
                    w.click()

    def reveal_all_tiles(self):
        for x in range(0, self.n):
            for y in range(0, self.n):
                self.grid.itemAtPosition(y, x).widget().reveal()

    def count_revealed_tiles(self):
    	count = 0
    	for i in range(self.n):
    		for j in range(self.n):
    			w = self.grid.itemAtPosition(i, j).widget()
    			if w.is_revealed and not w.is_mine:
    				count += 1
    	return count

    def game_over(self):
        self.player.setScore(self.count_revealed_tiles())
        self.player.setTime(self.clock.text())
        self.gameStatus = 0
        self.reveal_all_tiles()

    def update_timer(self):

        if self.gameStatus == 1:
            n_secs = int(time.time()) - self._timer_start_nsecs
            self.clock.setText("%03d" % n_secs)

    def check_state(self, x, y):
        w = self.grid.itemAtPosition(y, x).widget()
        if w.check_block(self.grid, x, y, self.n):
            self.game_over()


    def generate_hex_map(self):
        self.init_hex_map()
        self.reset_map()

    def generate_square_map(self):
        self.init_square_map()
        self.reset_map()

    def generate_colored_map(self):
        self.init_colored_map()
        self.reset_map()

    def quit_game(self):
        sys.exit()




if __name__ == '__main__':
    app = QApplication([])
    window = MineSweeper(GRID_DIMENSION, TOTAL_MINES)

    app.exec_()