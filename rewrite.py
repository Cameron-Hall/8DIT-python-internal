from tkinter import *


class Board:
    def __init__(self, seed, parent, GUI):
        self.game = parent
        self.seed = seed
        self.GUI = GUI

        self.tilemap = []
        self.colormap = []

        for i in range(self.GUI.WINDOW_HEIGHT//self.game.TILE_SIZE):
            self.tilemap.append([])
            self.colormap.append([])

            for j in range(self.GUI.WINDOW_WIDTH//self.game.TILE_SIZE):
                color = self.seed[i][j]
                color = self.game.colors[color]

                tile = Frame(self.game.levels[int(self.seed[self.GUI.WINDOW_HEIGHT//self.game.TILE_SIZE][0])-1], width=self.game.TILE_SIZE, height=self.game.TILE_SIZE, bg=color)
                tile.grid(row=i, column=j)
                self.tilemap[i].append(tile)
                self.colormap[i].append(color)

        self.pathmap = []

        for i in range(self.GUI.WINDOW_HEIGHT//self.game.TILE_SIZE):
            self.pathmap.append([])
            for j in range(self.GUI.WINDOW_WIDTH//self.game.TILE_SIZE):
                self.pathmap[i].append({"up":0, "down":0, "left": 0, "right":0})
                if self.colormap[i][j] == "red":
                    pass
                else:
                    for k in range(i-1,-1,-1):
                        if self.colormap[k][j] == "red":
                            break
                        else:
                            self.pathmap[i][j]["up"] += 1

                    for k in range(i+1,10,1):
                        if self.colormap[k][j] == "red":
                            break
                        else:
                            self.pathmap[i][j]["down"] += 1

                    for k in range(j-1,-1,-1):
                        if self.colormap[i][k] == "red":
                            break
                        else:
                            self.pathmap[i][j]["left"] += 1

                    for k in range(j+1,10,1):
                        if self.colormap[i][k] == "red":
                            break
                        else:
                            self.pathmap[i][j]["right"] += 1

        character_x = int(self.seed[self.GUI.WINDOW_HEIGHT//self.game.TILE_SIZE][2])
        character_y = int(self.seed[self.GUI.WINDOW_HEIGHT//self.game.TILE_SIZE][4])

        self.character = Character(character_x, character_y, self)

        self.GUI.parent.bind("<KeyRelease-w>", lambda i: self.character.move_up())
        self.GUI.parent.bind("<KeyRelease-s>", lambda i: self.character.move_down())
        self.GUI.parent.bind("<KeyRelease-d>", lambda i: self.character.move_right())
        self.GUI.parent.bind("<KeyRelease-a>", lambda i: self.character.move_left())

        self.tilemap[self.character.y][self.character.x].configure(bg="black")

        box_x = self.seed[self.GUI.WINDOW_HEIGHT//self.game.TILE_SIZE][6]
        box_y = self.seed[self.GUI.WINDOW_HEIGHT//self.game.TILE_SIZE][8]

        self.box = Box(box_x, box_y, self, self.character)


class Box:
    def __init__(self, x, y, board, character):
        self.x = x
        self.y = y
        self.board = board
        self.character = character

    def initiate_movement(self):
        if self.detect_player(self.board):
            self.move_box(self.board) 

    def detect_player(self):
        if (self.player.x in range(self.x-2, self.x+3) and self.player.y in range(self.y-2, self.y+3)) and self.player_visible(self.board) in range(4):
            return True
        
    def player_visible(self):
        pass

    def move_box(self):
        pass

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_right(self):
        pass

    def move_left(self):
        pass


class Character:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board
        self.color = "black"
        self.movement = Movement(self, self.board)

    def move_up(self):
        self.movement.move_up()

    def move_down(self):
        self.movement.move_down()

    def move_right(self):
        self.movement.move_right()

    def move_left(self):
        self.movement.move_left()

    
class Game:
    def __init__(self, parent):
        self.parent = parent

        self.seeds = [["rwrrrrrrrr",
                       "rwwwwwwrrr",
                       "rwrrwwwwrr",
                       "rwwrwrrwrr",
                       "rrrrrrrwrr",
                       "rrwwwwwwrr",
                       "rrwwwwwwrr",
                       "rrwrrrrwrr",
                       "rwwwwwwwwr",
                       "rrrwrrwrrr", "1:1,8:4,8"]]
        
        self.levels = []

        self.colors = {"w": "white", "b": "black", "r": "red", "g": "green", "y": "yellow"}

        self.TILE_SIZE = 50

        self.levels = []

        for seed in self.seeds:
            self.levels.append(Frame(self.parent.parent))

        self.levels[0].pack()
        
        for seed in self.seeds:
            b = Board(seed, self, self.parent)


class GUI:
    def __init__(self, parent):
        self.parent = parent
        
        self.WINDOW_WIDTH = 500
        self.WINDOW_HEIGHT = 500

        self.game = Game(self)

        self.parent.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+200+200")
        self.parent.resizable(False, False)


class Movement:
    def __init__(self, item, board):
        self.item = item
        self.board = board

    def move_up(self):
        self.item.y -= 1
        try:
            if self.item.y < 0 or not self.check_validity():
                raise IndexError
            self.update_character("up")
        except IndexError:
            self.item.y += 1

    def move_down(self):
        self.item.y += 1
        try:
            if self.item.y > self.board.GUI.WINDOW_HEIGHT or not self.check_validity():
                raise IndexError
            self.update_character("down")
        except IndexError:
            self.item.y -= 1

    def move_right(self):
        self.item.x += 1
        try:
            if self.item.x > self.board.GUI.WINDOW_WIDTH or not self.check_validity():
                raise IndexError
            self.update_character("right")
        except IndexError:
            self.item.x -= 1

    def move_left(self):
        self.item.x -= 1
        try:
            if self.item.x < 0 or not self.check_validity():
                raise IndexError
            self.update_character("left")
        except IndexError:
            self.item.x += 1

    def check_validity(self):
        if self.board.colormap[self.item.y][self.item.x] == "red":
            return False
        else:
            return True
        
    def update_character(self, dir):
        self.board.tilemap[self.item.y][self.item.x].configure(bg=self.item.color)

        if dir == "up":
            try:
                self.board.tilemap[self.item.y+1][self.item.x].configure(bg=self.board.colormap[self.item.y+1][self.item.x])
            except IndexError:
                pass

        elif dir == "down":
            try:
                self.board.tilemap[self.item.y-1][self.item.x].configure(bg=self.board.colormap[self.item.y-1][self.item.x])
            except IndexError:
                pass

        elif dir == "right":
            try:
                self.board.tilemap[self.item.y][self.item.x-1].configure(bg=self.board.colormap[self.item.y][self.item.x-1])
            except IndexError:
                pass

        elif dir == "left":
            try:
                self.board.tilemap[self.item.y][self.item.x+1].configure(bg=self.board.colormap[self.item.y][self.item.x+1])
            except IndexError:
                pass

        print(self.board.pathmap[self.item.y][self.item.x])


if __name__ == "__main__":
    root = Tk()
    GUI(root)
    root.mainloop()
