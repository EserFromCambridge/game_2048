import unittest
from unittest import mock
from game_2048 import Game2048
try:
    import tkinter as tk
except ImportError:  # python 2
    import Tkinter as tk
import builtins


class TestGame2048(unittest.TestCase):

    def setUp(self):
        self.new_game = Game2048()
        self.matrix = [[0, 2, 0, 2], [0, 2, 4, 2], [4, 2, 0, 2], [2, 0, 0, 2]]

    def test_init_matrix(self):
        self.new_game.init_matrix()
        cnt2 = 0
        cnt0 = 0
        for lst in self.new_game.matrix:
            cnt2 += lst.count(2)
            cnt0 += lst.count(0)
        self.assertEqual(cnt2, 2)
        self.assertEqual(cnt0, 14)

    def test_add_element(self):
        self.new_game.matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.new_game.add_element()
        self.new_game.add_element()
        cnt = 0
        for lst in self.new_game.matrix:
            cnt += lst.count(2)
        self.assertEqual(cnt, 2)

    def test_transpose(self):
        new_matrix = Game2048.transpose(self.matrix)
        self.assertEqual(new_matrix, [[0, 0, 4, 2], [2, 2, 2, 0], [0, 4, 0, 0], [2, 2, 2, 2]])

    def test_reverse(self):
        new_matrix = Game2048.reverse(self.matrix)
        self.assertEqual(new_matrix, [[2, 0, 2, 0], [2, 4, 2, 0], [2, 0, 2, 4], [2, 0, 0, 2]])

    def test_compress(self):
        new_matrix = Game2048.compress(self, self.matrix)
        self.assertEqual(new_matrix, [[2, 2, 0, 0], [2, 4, 2, 0], [4, 2, 2, 0], [2, 2, 0, 0]])

    def test_merge(self):
        new_matrix = Game2048.merge(self, self.matrix)
        self.assertEqual(new_matrix, self.matrix)
        new_matrix = Game2048.merge(self, Game2048.compress(self, self.matrix))
        self.assertEqual(new_matrix, [[4, 0, 0, 0], [2, 4, 2, 0], [4, 4, 0, 0], [4, 0, 0, 0]])

    def test_up_button(self):
        new_matrix = Game2048.up_button(self.new_game, self.matrix)
        self.assertEqual(new_matrix, [[4, 4, 4, 4], [2, 2, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]])

    def test_down_button(self):
        new_matrix = Game2048.down_button(self.new_game, self.matrix)
        self.assertEqual(new_matrix, [[0, 0, 0, 0], [0, 0, 0, 0], [4, 2, 0, 4], [2, 4, 4, 4]])

    def test_right_button(self):
        new_matrix = Game2048.right_button(self.new_game, self.matrix)
        self.assertEqual(new_matrix, [[0, 0, 0, 4], [0, 2, 4, 2], [0, 0, 4, 4], [0, 0, 0, 4]])

    def test_left_button(self):
        new_matrix = Game2048.left_button(self.new_game, self.matrix)
        self.assertEqual(new_matrix, [[4, 0, 0, 0], [2, 4, 2, 0], [4, 4, 0, 0], [4, 0, 0, 0]])

    def test_process(self):
        new_matrix = Game2048.process(self.new_game, self.matrix)
        self.assertEqual(new_matrix, [[4, 0, 0, 0], [2, 4, 2, 0], [4, 4, 0, 0], [4, 0, 0, 0]])

    @mock.patch('game_2048.tk')
    def test_init_frame(self, mocked_tk):
        self.new_game.init_frame()
        self.assertEqual(mocked_tk.Frame.call_count, 17)
        self.assertEqual(mocked_tk.Label.call_count, 16)

    @mock.patch('game_2048.builtins')
    def test_key_pressed(self, mocked_builtins):
        mocked_builtins.repr.return_value = "a"
        e = tk.Event()
        e.char = chr(119) # character 'w'
        self.new_game.key_pressed(e)
        mocked_builtins.repr.assert_called_once()


if __name__ == "__main__":
    unittest.main()
