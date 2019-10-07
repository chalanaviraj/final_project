import sys
import unittest
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import MineSweeper

class MineSweeperTest(unittest.TestCase):
    '''Test the margarita mixer GUI'''
    def setUp(self):
        '''Create the GUI'''
        self.game = MineSweeper.MineSweeper(8, 15)


    def test_square_block_is_revealed(self):
        self.game.generate_square_map()
        block = self.game.grid.itemAtPosition(0, 0).widget()
        block.click()
        self.assertEqual(block.is_revealed, True)


    def test_game_ends_when_mine_is_revealed(self):
    	self.game.generate_square_map()
    	self.game.set_mine_at(0,0)
    	block = self.game.grid.itemAtPosition(0, 0).widget()
    	block.click()
    	self.assertEqual(self.game.gameStatus, 0)

    def test_expandable_block(self):
    	self.game.generate_square_map()
    	self.game.remove_mine_from(0, 0)
    	self.game.remove_mine_from(0, 1)
    	self.game.remove_mine_from(1, 0)
    	self.game.remove_mine_from(1, 1)
    	block1 = self.game.grid.itemAtPosition(0, 0).widget()
    	block2 = self.game.grid.itemAtPosition(0, 1).widget()
    	block3 = self.game.grid.itemAtPosition(1, 0).widget()
    	block4 = self.game.grid.itemAtPosition(1, 1).widget()
    	block1.click()
    	self.assertTrue(block1.is_revealed)
    	self.assertTrue(block2.is_revealed)
    	self.assertTrue(block3.is_revealed)
    	self.assertTrue(block4.is_revealed)

    	


if __name__ == "__main__":
	app = QApplication([])
	unittest.main()
