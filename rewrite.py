from tkinter import *


class Board:
    def __init__(self, seed, parent, GUI):
        self.game = parent
        self.seed = seed
        self.GUI = GUI

        # Establishes a tilemap (2D list) of individual colored Frames
        # Establishes a colormap (2D list) of the colors of their respective Frame

        self.tilemap = []
        self.colormap = []

        for i in range((self.GUI.WINDOW_HEIGHT-20)//self.game.TILE_SIZE):
            self.tilemap.append([])
            self.colormap.append([])

            for j in range(self.GUI.WINDOW_WIDTH//self.game.TILE_SIZE):
                color = self.seed[i][j]
                color = self.game.colors[color]

                tile = Frame(self.game.levels[int(self.seed[(self.GUI.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][0])-1], width=self.game.TILE_SIZE, height=self.game.TILE_SIZE, bg=color)
                tile.grid(row=i, column=j)
                self.tilemap[i].append(tile)
                self.colormap[i].append(color)

        # Establishes a pathmap (2D list) of the possible lengths in each direction and whether they are perceived as an obvious dead end from each grid square

        self.pathmap = []

        for i in range((self.GUI.WINDOW_HEIGHT-20)//self.game.TILE_SIZE):
            self.pathmap.append([])
            for j in range(self.GUI.WINDOW_WIDTH//self.game.TILE_SIZE):
                self.pathmap[i].append({"up":0, "up_dead_end":True, "down":0, "down_dead_end":True, "left": 0, "left_dead_end":True, "right":0, "right_dead_end":True})
                self.pathmap_update(i, j)


        character_x = int(self.seed[(self.GUI.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][2])
        character_y = int(self.seed[(self.GUI.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][4])

        self.character = Character(character_x, character_y, self)

        self.tilemap[self.character.y][self.character.x].configure(bg="black")

        box_x = int(self.seed[(self.GUI.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][6])
        box_y = int(self.seed[(self.GUI.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][8])

        self.box = Box(box_x, box_y, self, self.character)

        self.tilemap[self.box.y][self.box.x].configure(bg="yellow")

    def pathmap_update(self, i, j):
        self.pathmap[i][j] = ({"up":0, "up_dead_end":True, "down":0, "down_dead_end":True, "left": 0, "left_dead_end":True, "right":0, "right_dead_end":True})
        if self.colormap[i][j] == "red":
            pass
        else:
            for k in range(i-1,-1,-1):
                if self.colormap[k][j] == "white":
                    self.pathmap[i][j]["up"] += 1
                    if self.colormap[k][j-1] == "white" or self.colormap[k][j+1] == "white":
                        self.pathmap[i][j]["up_dead_end"] = False
                else:
                    break
                    
            for k in range(i+1,15,1):
                if self.colormap[k][j] == "white":
                    self.pathmap[i][j]["down"] += 1
                    if self.colormap[k][j-1] == "white" or self.colormap[k][j+1] == "white":
                        self.pathmap[i][j]["down_dead_end"] = False
                else:
                    break
                    
            for k in range(j-1,-1,-1):
                if self.colormap[i][k] == "white":
                    self.pathmap[i][j]["left"] += 1
                    if self.colormap[i-1][k] == "white" or self.colormap[i+1][k] == "white":
                        self.pathmap[i][j]["left_dead_end"] = False
                else:
                    break                    

            for k in range(j+1,15,1):
                if self.colormap[i][k] == "white":
                    self.pathmap[i][j]["right"] += 1
                    if self.colormap[i-1][k] == "white" or self.colormap[i+1][k] == "white":
                        self.pathmap[i][j]["right_dead_end"] = False
                else:
                    break


class Box:
    def __init__(self, x, y, board, character):
        self.x = x
        self.y = y
        self.board = board
        self.character = character

        self.color = "yellow"
        self.movement = Movement(self, self.board)

    def initiate_movement(self):
        self.cycles += 1
        if self.detect_player() and self.cycles < 10:
            self.move_box() 

    def detect_player(self):
        if (self.character.x in range(self.x-2, self.x+3) and self.character.y in range(self.y-2, self.y+3)) and self.player_visible() in range(4): 
            if self.character.x == self.x and self.character.y == self.y:
                return False
            return True
        
    def player_visible(self):
        if self.character.y in range(self.y, self.y - self.board.pathmap[self.y][self.x]["up"]-1, -1) and self.character.x == self.x:
            return 0
        elif self.character.y in range(self.y, self.y + self.board.pathmap[self.y][self.x]["down"]+1, 1) and self.character.x == self.x:
            return 1
        elif self.character.x in range(self.x, self.x + self.board.pathmap[self.y][self.x]["right"]+1, 1) and self.character.y == self.y:
            return 2
        elif self.character.x in range(self.x, self.x - self.board.pathmap[self.y][self.x]["left"]-1, -1) and self.character.y == self.y:
            return 3
        else: 
            return 4

    def move_box(self):
        if self.player_visible() == 1:
            if self.check_end("up_dead_end"):
                if self.check_end("left_dead_end"):
                    if self.check_end("right_dead_end"):
                        maximum = max(self.check_end("up"), self.check_end("left"), self.check_end("right"))
                        if maximum == self.check_end("up"):
                            self.move_up()
                        elif maximum == self.check_end("left"):
                            self.move_left()
                        elif maximum == self.check_end("right"):
                            self.move_right()                    
                    else:
                        self.move_right()
                else:
                    self.move_left()
            else:
                self.move_up()
        
        elif self.player_visible() == 0:
            if self.check_end("down_dead_end"):
                if self.check_end("right_dead_end"):
                    if self.check_end("left_dead_end"):
                        maximum = max(self.check_end("down"), self.check_end("right"), self.check_end("left"))
                        if maximum == self.check_end("down"):
                            self.move_down()
                        elif maximum == self.check_end("right"):
                            self.move_right()
                        elif maximum == self.check_end("left"):
                            self.move_left()                    
                    else:
                        self.move_left()
                else:
                    self.move_right()
            else:
                self.move_down()

        elif self.player_visible() == 3:
            if self.check_end("right_dead_end"):
                if self.check_end("up_dead_end"):
                    if self.check_end("down_dead_end"):
                        maximum = max(self.check_end("right"), self.check_end("up"), self.check_end("down"))
                        if maximum == self.check_end("right"):
                            self.move_right()
                        elif maximum == self.check_end("up"):
                            self.move_up()
                        elif maximum == self.check_end("down"):
                            self.move_down()                    
                    else:
                        self.move_down()
                else:
                    self.move_up()
            else:
                self.move_right()
        
        elif self.player_visible() == 2:
            if self.check_end("left_dead_end"):
                if self.check_end("down_dead_end"):
                    if self.check_end("up_dead_end"):
                        maximum = max(self.check_end("left"), self.check_end("down"), self.check_end("up"))
                        if maximum == self.check_end("left"):
                            self.move_left()
                        elif maximum == self.check_end("down"):
                            self.move_down()
                        elif maximum == self.check_end("up"):
                            self.move_up()                    
                    else:
                        self.move_up()
                else:
                    self.move_down()
            else:
                self.move_left()

        self.initiate_movement()
                    

    def check_end(self, dir):
        return self.board.pathmap[self.y][self.x][dir]

    def move_up(self):
        self.movement.move_up()

    def move_down(self):
        self.movement.move_down()

    def move_right(self):
        self.movement.move_right()

    def move_left(self):
        self.movement.move_left()


class Character:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board
        self.color = "black"
        self.movement = Movement(self, self.board)

    def move_up(self):
        self.movement.move_up()
        self.board.box.cycles = 0
        self.board.box.initiate_movement()

    def move_down(self):
        self.movement.move_down()
        self.board.box.cycles = 0
        self.board.box.initiate_movement()

    def move_right(self):
        self.movement.move_right()
        self.board.box.cycles = 0
        self.board.box.initiate_movement()

    def move_left(self):
        self.movement.move_left()
        self.board.box.cycles = 0
        self.board.box.initiate_movement()

    
class Game:
    def __init__(self, parent):
        self.parent = parent

        self.seeds = [["rrrrrrrrrrrrrrr",
                       "rrrrrrrrrwrwrrr",
                       "rrrrrrrwwwwwwrr",
                       "rrrrrrrrrrrwrrr",
                       "rrwwwwwwwwwwwrr",
                       "rrrrwrrrrrrrrrr",
                       "rrrrwrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr","1:2,4:7,4"],
                       
                      ["rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrwrrrwwwwwrr",
                       "rwwrwrrrwrwrwrr",
                       "rwwwwwwwwwwwwrr",
                       "rwwrwrrrrrwrrrr",
                       "rrrrwrrrrwwwrrr",
                       "rrrrrrrrrrwrrrr",
                       "rrrrrrrrrrrrrrr","2:4,6:2,4"],
                       
                      ["rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrwr",
                       "rrrrwrrrwwwwwwr",
                       "rrrrwrrrwrrwrrr",
                       "rrrrwwwwwwrwrrr",
                       "rrrrrrrrwrrwwwr",
                       "rrrrrrrrwwwwrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr","3:4,2:7,4"]]
        
        self.levels = []

        self.colors = {"w": "white", "b": "blue", "r": "red", "g": "green", "y": "yellow"}

        self.TILE_SIZE = 50

        self.levels = []

        self.curr_level = 0

        for seed in self.seeds:
            self.levels.append(Frame(self.parent.mainframe))

        self.toolbar = Toolbar(self.parent.toolbar_frame, self, self.parent)




        self.establish_board()

        
    def establish_board(self): 
        print(self.curr_level)
        print(self.seeds[self.curr_level])
        print(self.levels[self.curr_level])
        self.levels[self.curr_level].grid(row=1, column=0, columnspan=3)
        self.b = Board(self.seeds[self.curr_level], self, self.parent)

        self.toolbar.level_number.configure(text=self.curr_level)

        self.parent.parent.bind("<KeyRelease-w>", lambda i: self.b.character.move_up())
        self.parent.parent.bind("<KeyRelease-s>", lambda i: self.b.character.move_down())
        self.parent.parent.bind("<KeyRelease-d>", lambda i: self.b.character.move_right())
        self.parent.parent.bind("<KeyRelease-a>", lambda i: self.b.character.move_left())




class GUI:
    def __init__(self, parent):
        self.parent = parent
        
        self.WINDOW_WIDTH = 750
        self.WINDOW_HEIGHT = 470

        self.mainframe = Frame(parent)

        self.toolbar_frame = Frame(self.mainframe, height = 30)
        self.toolbar_frame.grid(row=0, column=0)

        self.mainframe.pack()

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


class Toolbar:
    def __init__(self, frame, parent, GUI):
        self.frame = frame
        self.parent = parent
        self.GUI = GUI

        self.prev_level_button = Button(self.frame, width=10, text="< Previous", command=self.prev_level)
        self.prev_level_button.grid(row=0, column=0, padx=20)

        self.level_number = Label(self.frame, text=f"{self.parent.curr_level+1}")
        self.level_number.grid(row=0, column=1)

        self.next_level_button = Button(self.frame, width=10, text="Next >", command=self.next_level)
        self.next_level_button.grid(row=0, column=2, padx=20)

    def prev_level(self):
        self.parent.levels[self.parent.curr_level].grid_forget()
        self.parent.curr_level -= 1
        self.parent.establish_board()

    def next_level(self):
        self.parent.levels[self.parent.curr_level].grid_forget()
        self.parent.curr_level += 1
        self.parent.establish_board()








if __name__ == "__main__":
    root = Tk()
    GUI(root)
    root.mainloop()
