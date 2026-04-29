import time
from tkinter import *
from tkinter import messagebox
import random

class Movement:
    def __init__(self, item, board):
        self.item = item
        self.board = board

    def move_up(self, board):
        self.item.y -= 1
        try:
            if self.item.y < 0 or not self.check_validity(board):
                raise IndexError
            self.item.update_character(board, "up")
        except IndexError:
            self.item.y += 1

    def move_down(self, board):
        self.item.y += 1
        try:
            if self.item.y > board.WINDOW_HEIGHT or not self.check_validity(board):
                raise IndexError
            self.item.update_character(board, "down")
        except IndexError:
            self.item.y -= 1

    def move_right(self, board):
        self.item.x += 1
        try:
            if self.item.x > board.WINDOW_WIDTH or not self.check_validity(board):
                raise IndexError
            self.item.update_character(board, "right")
        except IndexError:
            self.item.x -= 1

    def move_left(self, board):
        self.item.x -= 1
        try:
            if self.item.x < 0 or not self.check_validity(board):
                raise IndexError
            self.item.update_character(board, "left")
        except IndexError:
            self.item.x += 1

    def check_validity(self, board):
        if board.colormap[self.item.y][self.item.x] == "red":
            return False
        else:
            return True
    
class Board:
    def __init__(self, parent, seed, tilemap, colormap):
        self.parent = parent
        self.seed = seed
        self.tilemap = tilemap
        self.colormap = colormap

        for i in range(self.parent.WINDOW_HEIGHT):
            self.tilemap.append([])
            self.colormap.append([])
            for j in range(self.parent.WINDOW_WIDTH):
                color = str(self.seed[i+1])[j+2]
                if color == "r":
                    color = "red"
                elif color == "w":
                    color = "white"
                
                f = Frame(self.parent, bg=color, width=self.TILE_SIZE, height=self.TILE_SIZE)
                f.grid(row=i, column=j)
                self.tilemap[i].append(f)
                self.colormap[i].append(color)

class Character:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board
        self.movement = Movement(self, board)
    
    def move_up(self, board):
        self.movement.move_up(board)

    def move_down(self, board):
        self.movement.move_down(board)

    def move_right(self, board):
        self.movement.move_right(board)

    def move_left(self, board):
        self.movement.move_left(board)   

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
        self.box.initiate_movement(board)

    def print_pos(self):
        print(f"{self.x},{self.y}")


class Box:
    def __init__(self, x, y, board, player):
        self.x = x
        self.y = y
        self.movement = Movement(self, board)
        self.player = player
        board = board
        board.tilemap[self.y][self.x].configure(bg="yellow")

        self.detect_walls(self.x, self.y, board)

    def detect_walls(self, x, y, board):
        self.surrounding_walls = 0
        if board.colormap[y-1][x] == "red" or (x == self.player.x and y-1 == self.player.y):
            self.surrounding_walls += 1
        if board.colormap[y+1][x] == "red" or (x == self.player.x and y+1 == self.player.y):
            self.surrounding_walls += 1
        if board.colormap[y][x-1] == "red" or (x-1 == self.player.x and y == self.player.y):
            self.surrounding_walls += 1
        if board.colormap[y][x+1] == "red" or (x+1 == self.player.x and y == self.player.y):
            self.surrounding_walls += 1
        return self.surrounding_walls

    def initiate_movement(self, board):
        if self.detect_player(board):
            self.iters = 0
            self.move_box(board)        

    def player_visible(self, board):
        directions = [(-1,0),(1,0),(0,1),(0,-1)]
        for i in range(4):
            for j in range(10):
                if board.colormap[self.y+directions[i][0]*j][self.x+directions[i][1]*j] == "red":
                    break
                if self.y+((j+1)*(directions[i][0])) == self.player.y and self.x+((j+1)*directions[i][1]) == self.player.x:
                    self.player_dir = i
                    return self.player_dir
        return 4
    
    def dead_end(self, dir, board):
        directions = [(-1,0),(1,0),(0,1),(0,-1)]
        dead_end = False
        for i in range(10):
            if self.detect_walls(self.x+((i+1)*directions[dir][1]), self.y+((i+1)*directions[dir][0]), board) < 3 and board.colormap[self.y+((i+2)*directions[dir][0])][self.x+((i+2)*directions[dir][1])] == "red":
                dead_end = False
                break
            elif self.detect_walls(self.x+((i+1)*directions[dir][1]), self.y+((i+1)*directions[dir][0]), board) <= 1:
                dead_end = False
                break
            elif (self.detect_walls(self.x+((i+1)*directions[dir][1]), self.y+((i+1)*directions[dir][0]), board)) == 3:
                dead_end = True
                break
            elif board.colormap[self.y+((i+2)*directions[dir][0])][self.x+((i+2)*directions[dir][1])] == "red":
                dead_end = True
                break
            else:
                pass
        return dead_end
         
    def detect_player(self, board):
        if (self.player.x in range(self.x-2, self.x+3) and self.player.y in range(self.y-2, self.y+3)) and self.player_visible(board) in range(4):
            return True
        
    def move_box(self, board):
        if self.player_dir == 0:
            if self.surrounding_walls == 0:
                self.move_down(board)
            elif self.surrounding_walls == 2:
                if (board.colormap[self.y+1][self.x] == "red" or self.dead_end(1, board)) and (board.colormap[self.y][self.x+1] == "red" or self.dead_end(2, board)):
                    self.move_left(board)
                elif (board.colormap[self.y+1][self.x] == "red" or self.dead_end(1, board)) and (board.colormap[self.y][self.x-1] == "red" or self.dead_end(3, board)):
                    self.move_right(board)
                else:
                    self.move_down(board)
            elif self.surrounding_walls == 1:
                if (board.colormap[self.y+1][self.x] == "red" or self.dead_end(1, board)):
                    self.move_right(board)
                else:
                    self.move_left(board)

        elif self.player_dir == 1:
            if self.surrounding_walls == 0:
                self.move_up(board)
            elif self.surrounding_walls == 2:
                if (board.colormap[self.y-1][self.x] == "red" or self.dead_end(0, board)) and (board.colormap[self.y][self.x+1] == "red" or self.dead_end(2, board)):
                    self.move_left(board)
                elif (board.colormap[self.y-1][self.x] == "red" or self.dead_end(0, board)) and (board.colormap[self.y][self.x-1] == "red" or self.dead_end(3, board)):
                    self.move_right(board)
                else:
                    self.move_up(board)
            elif self.surrounding_walls == 1:
                if (board.colormap[self.y-1][self.x] == "red" or self.dead_end(0, board)):
                    self.move_left(board)
                else:
                    self.move_right(board)

        elif self.player_dir == 2:
            if self.surrounding_walls == 0:
                self.move_left(board)
            elif self.surrounding_walls == 2:
                if (board.colormap[self.y][self.x-1] == "red" or self.dead_end(3, board)) and (board.colormap[self.y+1][self.x] == "red" or self.dead_end(1, board)):
                    print("works")
                    self.move_up(board)
                elif (board.colormap[self.y][self.x-1] == "red" or self.dead_end(3, board)) and (board.colormap[self.y-1][self.x] == "red" or self.dead_end(0, board)):
                    self.move_down(board)
                else:
                    self.move_left(board)
            elif self.surrounding_walls == 1:
                if (board.colormap[self.y][self.x-1] == "red" or self.dead_end(3, board)):
                    self.move_down(board)
                else:
                    self.move_up(board)

        elif self.player_dir == 3:
            if self.surrounding_walls == 0:
                self.move_right(board)
            elif self.surrounding_walls == 2:
                if (board.colormap[self.y][self.x+1] == "red" or self.dead_end(2, board)) and (board.colormap[self.y+1][self.x] == "red" or self.dead_end(1, board)):
                    self.move_left(board)
                elif (board.colormap[self.y][self.x+1] == "red" or self.dead_end(2, board)) and (board.colormap[self.y-1][self.x] == "red" or self.dead_end(0, board)):
                    self.move_down(board)
                else:
                    self.move_right(board)
            elif self.surrounding_walls == 1:
                if (board.colormap[self.y][self.x+1] == "red" or self.dead_end(2, board)):
                    self.move_up(board)
                else:
                    self.move_down(board)

        self.detect_walls(self.x, self.y, board)

    def move_up(self, board):
        self.iters += 1
        if self.dead_end(0, board) and self.dead_end(1, board) and self.dead_end(2, board) and self.dead_end(3, board):
            self.movement.move_up(board)
        if (self.dead_end(0, board) or self.player_dir == 0) and self.iters <= 4:
            self.move_left(board)
        else:
            self.movement.move_up(board)
            if self.detect_player(board):
                print("detect")
                self.move_box(board)

    def move_down(self, board):
        self.iters += 1
        if self.dead_end(0, board) and self.dead_end(1, board) and self.dead_end(2, board) and self.dead_end(3, board):
            self.movement.move_down(board)
        elif (self.dead_end(1, board) or self.player_dir == 1) and self.iters <= 4:
            self.move_right(board)
        else:
            self.movement.move_down(board)
            if self.detect_player(board):
                print("detect")
                self.move_box(board)

    def move_right(self, board):
        self.iters += 1
        if self.dead_end(0, board) and self.dead_end(1, board) and self.dead_end(2, board) and self.dead_end(3, board):
            self.movement.move_right(board)
        elif (self.dead_end(2, board) or self.player_dir == 2) and self.iters <= 4:
            self.move_up(board)
        else:
            self.movement.move_right(board)
            if self.detect_player(board):
                print("detect")
                self.move_box(board)

    def move_left(self, board):
        self.iters += 1
        if self.dead_end(0, board) and self.dead_end(1, board) and self.dead_end(2, board) and self.dead_end(3, board):
            self.movement.move_left(board)
        elif (self.dead_end(3, board) or self.player_dir == 3) and self.iters <= 4:
            self.move_down(board)
        else:
            self.movement.move_left(board)
            if self.detect_player(board):
                print("detect")
                self.move_box(board)

    def update_character(self, board, dir):
        board.tilemap[self.y][self.x].configure(bg="yellow")

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


    
class GUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Sokoban")

        self.seed = [["10x10:3,9:5,8"],
                     ["rwrrrrrrrr"],
                     ["rwwwwwwrrr"],
                     ["rwrrwwwwrr"],
                     ["rwwrwrrwrr"],
                     ["rrrrrrrwrr"],
                     ["rrwwwwwwrr"],
                     ["rrwwwwwwrr"],
                     ["rrwrrrrwrr"],
                     ["rwwwwwwwwr"],
                     ["rrrwrrwrrr"]
                     ]

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

        self.board = Board(self, self.seed, self.tilemap, self.colormap)

        self.character = Character(int(str(self.seed[0])[8]),int(str(self.seed[0])[10]), self.board)

        self.parent.bind("<KeyRelease-w>", lambda i: self.character.move_up(self))
        self.parent.bind("<KeyRelease-s>", lambda i: self.character.move_down(self))
        self.parent.bind("<KeyRelease-d>", lambda i: self.character.move_right(self))
        self.parent.bind("<KeyRelease-a>", lambda i: self.character.move_left(self))

        self.tilemap[self.character.y][self.character.x].configure(bg="black")

        self.box = Box(int(str(self.seed[0])[12]),int(str(self.seed[0])[14]), self.board, self.character)
        self.character.box = self.box



                



if __name__ == "__main__":
    root = Tk()
    GUI(root)
    root.mainloop()