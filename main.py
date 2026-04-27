from tkinter import *
from tkinter import messagebox
import random

class Character:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board
    
    def move_up(self, board):
        self.y -= 1
        try:
            if self.y < 0 or not self.check_validity(board):
                raise IndexError
            self.update_character(board, "up")
        except IndexError:
            self.y += 1

    def move_down(self, board):
        self.y += 1
        try:
            if self.y > board.WINDOW_HEIGHT or not self.check_validity(board):
                raise IndexError
            self.update_character(board, "down")
        except IndexError:
            self.y -= 1

    def move_right(self, board):
        self.x += 1
        try:
            if self.x > board.WINDOW_WIDTH or not self.check_validity(board):
                raise IndexError
            self.update_character(board, "right")
        except IndexError:
            self.x -= 1

    def move_left(self, board):
        self.x -= 1
        try:
            if self.x < 0 or not self.check_validity(board):
                raise IndexError
            self.update_character(board, "left")
        except IndexError:
            self.x += 1

    
    def check_validity(self, board):
        if board.colormap[self.y][self.x] == "red":
            return False
        else:
            return True
        

    def update_character(self, board, dir):
        board.tilemap[self.y][self.x].configure(bg="black")

        if dir == "up":
            try:
                board.tilemap[self.y+1][self.x].configure(bg=board.colormap[self.y+1][self.x])
            except IndexError:
                pass

        elif dir == "down":
            try:
                board.tilemap[self.y-1][self.x].configure(bg=board.colormap[self.y-1][self.x])
            except IndexError:
                pass

        elif dir == "right":
            try:
                board.tilemap[self.y][self.x-1].configure(bg=board.colormap[self.y][self.x-1])
            except IndexError:
                pass

        elif dir == "left":
            try:
                board.tilemap[self.y][self.x+1].configure(bg=board.colormap[self.y][self.x+1])
            except IndexError:
                pass

        # self.print_pos()
        self.box.detect_player(self, board)


    def print_pos(self):
        print(f"{self.x},{self.y}")


class Box:
    def __init__(self, x, y, board, player):
        self.x = x
        self.y = y
        player = player
        board = board
        board.tilemap[self.y][self.x].configure(bg="yellow")

        self.surrounding_walls = 0
        if board.colormap[self.y-1][self.x] == "red":
            self.surrounding_walls += 1
        if board.colormap[self.y+1][self.x] == "red":
            self.surrounding_walls += 1
        if board.colormap[self.y][self.x-1] == "red":
            self.surrounding_walls += 1
        if board.colormap[self.y][self.x+1] == "red":
            self.surrounding_walls += 1

    def player_visible(self, player, board):
        directions = [(-1,0),(1,0),(0,1),(0,-1)]
        for i in range(4):
            for j in range(10):
                if board.colormap[self.y+directions[i][0]*j][self.x+directions[i][1]*j] == "red":
                    break
                if self.y+((j+1)*(directions[i][0])) == player.y and self.x+((j+1)*directions[i][1]) == player.x:
                    self.player_dir = i     # up:0 down:1 right:2 left:3
                    print(self.player_dir)
                    return True
        return False
                            
            
                
    def detect_player(self, player, board):
        if (player.x in range(self.x-2, self.x+3) and player.y in range(self.y-2, self.y+3)) and self.player_visible(player, board):
            print("close")
        else:
            print("far")
        # print(self.surrounding_walls)

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

        self.seed = [["10x10:1,6:5,6"],
                     ["rrrrrrrrrr"],
                     ["rrrrrrrrrr"],
                     ["rrrrrrrrrr"],
                     ["rrrrrrrwrr"],
                     ["rrrrrwwwwr"],
                     ["rwwwwwwwrr"],
                     ["rwwwrwwwwr"],
                     ["rrrwwwwwrr"],
                     ["rrrrrrrrrr"],
                     ["rrrrrrrrrr"]]

        self.TILE_SIZE = 25

        self.WINDOW_WIDTH = int(str(self.seed[0])[2:4])
        self.WINDOW_HEIGHT = int(str(self.seed[0])[5:7])
        self.parent.geometry(f"{self.WINDOW_WIDTH*self.TILE_SIZE}x{self.WINDOW_HEIGHT*self.TILE_SIZE}+200+200")
        self.parent.resizable(False, False)

        self.tilemap = []
        self.colormap = []

        for i in range(self.WINDOW_HEIGHT):
            self.tilemap.append([])
            self.colormap.append([])
            for j in range(self.WINDOW_WIDTH):
                color = str(self.seed[i+1])[j+2]
                if color == "r":
                    color = "red"
                elif color == "w":
                    color = "white"
                
                f = Frame(self.parent, bg=color, width=self.TILE_SIZE, height=self.TILE_SIZE)
                f.grid(row=i, column=j)
                self.tilemap[i].append(f)
                self.colormap[i].append(color)

        self.character = Character(int(str(self.seed[0])[8]),int(str(self.seed[0])[10]), self)

        self.parent.bind("<KeyRelease-w>", lambda i: self.character.move_up(self))
        self.parent.bind("<KeyRelease-s>", lambda i: self.character.move_down(self))
        self.parent.bind("<KeyRelease-d>", lambda i: self.character.move_right(self))
        self.parent.bind("<KeyRelease-a>", lambda i: self.character.move_left(self))

        self.tilemap[self.character.y][self.character.x].configure(bg="black")

        self.box = Box(int(str(self.seed[0])[12]),int(str(self.seed[0])[14]), self, self.character)
        self.character.box = self.box
                


if __name__ == "__main__":
    root = Tk()
    GUI(root)
    root.mainloop()