try:
    import tkinter as tk
except ImportError:  # python 2
    import Tkinter as tk
from random import *
import builtins

GRID_LEN = 4
SIZE = 500
GRID_PADDING = 12

FRAME_BACKGROUND_COLOR = "#a3998f"
CELL_BACKGROUND_EMPTY_COLOR = "#dbd1c7"
CELL_BACKGROUND_COLOR = {2: "#eee4da", 4: "#ede0c8", 8: "#edbb90", 16: "#f2a176",
                         32: "#db765e", 64: "#ce5e44", 128: "#edcf72", 256: "#c6ab57",
                         512: "#d3b143", 1024: "#cc4f0c", 2048: "#d81f0a"}
CELL_NUMBER_COLOR = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                     32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
                     512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 25, "bold")

KEY_UP = "\'\\uf700\'"
KEY_DOWN = "\'\\uf701\'"
KEY_LEFT = "\'\\uf702\'"
KEY_RIGHT = "\'\\uf703\'"


class Game2048(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.done = False
        self.master.bind("<Key>", self.key_pressed)

        self.commands = {KEY_UP: self.up_button, KEY_DOWN: self.down_button, KEY_LEFT: self.left_button,
                         KEY_RIGHT: self.right_button}
        self.grid_cells = []

    def start(self):
        self.init_frame()
        self.init_matrix()
        self.update_cells()
        self.mainloop()

    def init_frame(self):
        base = tk.Frame(self, bg=FRAME_BACKGROUND_COLOR, width=500, height=500)
        base.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = tk.Frame(base, bg=CELL_BACKGROUND_EMPTY_COLOR, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = tk.Label(master=cell, text="", bg=CELL_BACKGROUND_EMPTY_COLOR, justify='center', font=FONT, width=4,
                             height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def key_pressed(self, event):
        key = builtins.repr(event.char)
        if key in self.commands:
            self.matrix = self.commands[key](self.matrix)
            if self.done:
                self.matrix = self.add_element()
                self.update_cells()
                self.done = False
        else:
            print('Please use arrow keys')

    def init_matrix(self):
        # create a blank 4x4 matrix and then add 2 elements inside
        self.matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        # add 2 one of its empty('0') box (random selection)
        self.matrix = self.add_element()
        # add 2 one of its empty('0') box (random selection)
        self.matrix = self.add_element()

    def update_cells(self):
        # check all of the cells if they have numbers different than zero
        # configure that cell regarding to that number value.
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=CELL_BACKGROUND_EMPTY_COLOR)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=CELL_BACKGROUND_COLOR[new_number],
                                                    fg=CELL_NUMBER_COLOR[new_number])
        self.update_idletasks()

    def add_element(self):
        x = randint(0, GRID_LEN-1)
        y = randint(0, GRID_LEN-1)
        while self.matrix[x][y] != 0:
            x = randint(0, GRID_LEN-1)
            y = randint(0, GRID_LEN-1)
        self.matrix[x][y] = 2
        return self.matrix

    @staticmethod
    def transpose(matrix):
        new_matrix = [[matrix[j][i] for j in range(GRID_LEN)] for i in range(GRID_LEN)]
        return new_matrix

    @staticmethod
    def reverse(matrix):
        for lst in matrix:
            lst.reverse()
        return matrix

    def compress(self, matrix):
        new_matrix = []
        for lst in matrix:
            new_list = [0, 0, 0, 0]
            col = 0
            for i in range(len(lst)):
                if lst[i] != 0:
                    new_list[col] = lst[i]
                    if col != i:
                        self.done = True
                    col += 1
            new_matrix.append(new_list)
        return new_matrix

    def merge(self, matrix):
        for lst in matrix:
            for i in range(len(lst)-1):
                if lst[i] == lst[i+1] and lst[i] != 0:
                    lst[i] *= 2
                    lst[i+1] = 0
                    self.done = True
        return matrix

    def up_button(self, matrix):
        mat = self.transpose(matrix)
        # apply compress + merge + compress
        mat = self.process(mat)
        # apply transpose again to make it like before
        matrix = self.transpose(mat)
        return matrix

    def down_button(self, matrix):
        mat = self.reverse(self.transpose(matrix))
        # apply compress + merge + compress
        mat = self.process(mat)
        # apply reverse and transpose again to make it like before
        matrix = self.transpose(self.reverse(mat))
        return matrix

    def right_button(self, matrix):
        # take the reverse of the lists of the matrix
        mat = self.reverse(matrix)
        # apply compress + merge + compress
        mat = self.process(mat)
        # apply reverse of the lists of the matrix in order to make it like before
        matrix = self.reverse(mat)
        return matrix

    def left_button(self, matrix):
        # apply compress + merge + compress
        matrix = self.process(matrix)
        return matrix

    def process(self, matrix):
        return self.compress(self.merge(self.compress(matrix)))


if __name__ == '__main__':
    new_game = Game2048()
    new_game.start()
