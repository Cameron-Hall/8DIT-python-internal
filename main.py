from tkinter import *
from tkinter import messagebox
import random

class Character:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board
    
    def move_up(self, board):
        board.tilemap[self.y][self.x].configure(bg="green")
        self.y -= 1
        try:
            if self.y < 0:
                self.y = 0
            self.update_character(board)
        except IndexError:
            self.y += 1
            self.update_character(board)

    def move_down(self, board):
        board.tilemap[self.y][self.x].configure(bg="green")
        self.y += 1
        try:
            self.update_character(board)
        except IndexError:
            self.y -= 1
            self.update_character(board)

    def move_right(self, board):
        board.tilemap[self.y][self.x].configure(bg="green")
        self.x += 1
        try:
            self.update_character(board)
        except IndexError:
            self.x -= 1
            self.update_character(board)

    def move_left(self, board):
        board.tilemap[self.y][self.x].configure(bg="green")
        self.x -= 1
        try:
            if self.x < 0:
                self.x += 1
            self.update_character(board)
        except IndexError:
            self.x += 1
            self.update_character(board)
        

    def update_character(self, board):
        board.tilemap[self.y][self.x].configure(bg="black")
        self.print_pos()

    def print_pos(self):
        print(f"{self.x},{self.y}")


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def detect_player(self, player):
        pass

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass


class GUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Sokoban")

        self.seed = [["10x10:"],
                     ["rrrrrrrrrr"],
                     ["rwwwwwwwwr"],
                     ["rwwwwwwwwr"],
                     ["rwwwwwwwwr"],
                     ["rrrrwwrrrr"],
                     ["rwwwwwwwwr"],
                     ["rwwrrrrwwr"],
                     ["rwwwwwwwwr"],
                     ["rrrwwwwrrr"],
                     ["rrrrwwrrrr"]]

        self.TILE_SIZE = 25

        self.WINDOW_WIDTH = int(str(self.seed[0])[2:4])
        self.WINDOW_HEIGHT = int(str(self.seed[0])[5:7])
        self.parent.geometry(f"{self.WINDOW_WIDTH*self.TILE_SIZE}x{self.WINDOW_HEIGHT*self.TILE_SIZE}+200+200")

        self.tilemap = []

        for i in range(self.WINDOW_HEIGHT):
            self.tilemap.append([])
            for j in range(self.WINDOW_WIDTH):
                color = str(self.seed[i+1])[j+2]
                if color == "r":
                    color = "red"
                elif color == "w":
                    color = "white"
                
                f = Frame(self.parent, bg=color, width=self.TILE_SIZE, height=self.TILE_SIZE)
                f.grid(row=i, column=j)
                self.tilemap[i].append(f)

        self.character = Character(5,1, self)

        self.parent.bind("<KeyRelease-w>", lambda i: self.character.move_up(self))
        self.parent.bind("<KeyRelease-s>", lambda i: self.character.move_down(self))
        self.parent.bind("<KeyRelease-d>", lambda i: self.character.move_right(self))
        self.parent.bind("<KeyRelease-a>", lambda i: self.character.move_left(self))

        self.tilemap[self.character.y][self.character.x].configure(bg="black")

                


if __name__ == "__main__":
    root = Tk()
    GUI(root)
    root.mainloop()