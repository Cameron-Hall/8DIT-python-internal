from tkinter import *
from tkinter import messagebox


class Board:
    """Class for creating a game board and the character and box upon it."""
    def __init__(self, seed, game, gui, level_source):
        """Create a game board, with each element placed as per the seed."""
        self.game = game
        self.seed = seed
        self.gui = gui
        self.level_source = level_source

        # Establishes a tilemap (2D list) of individual colored Frames
        # Establishes a colormap (2D list) of the colors of their respective Frame

        self.tilemap = []
        self.colormap = []

        for i in range((self.gui.WINDOW_HEIGHT-20)//self.game.TILE_SIZE):
            self.tilemap.append([])
            self.colormap.append([])

            for j in range(self.gui.WINDOW_WIDTH//self.game.TILE_SIZE):
                color = self.seed[i][j]
                color = self.game.colors[color]

                tile = Frame(self.game.levels[int(self.seed[(self.gui.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][0:2])-1], width=self.game.TILE_SIZE, height=self.game.TILE_SIZE, bg=color)
                tile.grid(row=i, column=j)
                self.tilemap[i].append(tile)
                self.colormap[i].append(color)

        # Establishes a pathmap (2D list) of the possible lengths in each direction and whether they are perceived as an obvious dead end from each grid square

        self.pathmap = []

        for i in range((self.gui.WINDOW_HEIGHT-20)//self.game.TILE_SIZE):
            self.pathmap.append([])
            for j in range(self.gui.WINDOW_WIDTH//self.game.TILE_SIZE):
                self.pathmap[i].append({"up" : 0, "up_dead_end" : True, "down" : 0, "down_dead_end" : True, "left" : 0, "left_dead_end" : True, "right" : 0, "right_dead_end" : True})
                self.pathmap_update(i, j)

        # Character starting location may change based on where it comes from - if the character comes from the below level they will have a different starting point

        if self.level_source == "prev":
            character_x = int(self.seed[(self.gui.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][11])
            character_y = int(self.seed[(self.gui.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][13])
        else:
            character_x = int(self.seed[(self.gui.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][3])
            character_y = int(self.seed[(self.gui.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][5])

        self.character = Character(character_x, character_y, self)

        self.tilemap[self.character.y][self.character.x].configure(bg="black")

        box_x = int(self.seed[(self.gui.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][7])
        box_y = int(self.seed[(self.gui.WINDOW_HEIGHT-20)//self.game.TILE_SIZE][9])

        self.box = Box(box_x, box_y, self, self.character)

        self.tilemap[self.box.y][self.box.x].configure(bg="green")

    def pathmap_update(self, i, j):
        """Establishes the pathmap information for each tile"""
        self.pathmap[i][j] = ({"up":0, "up_dead_end":True, "down":0, "down_dead_end":True, "left": 0, "left_dead_end":True, "right":0, "right_dead_end":True, "tunnel":False})
        if self.colormap[i][j] == "red":
            pass
        else:
            for k in range(i-1, -1, -1):
                if self.colormap[k][j] in ["white", "yellow"]:
                    self.pathmap[i][j]["up"] += 1
                    if self.colormap[k][j-1] in ["white", "yellow"] or self.colormap[k][j+1] in ["white", "yellow"]:
                        self.pathmap[i][j]["up_dead_end"] = False
                else:
                    break
                    
            for k in range(i+1, 15, 1):
                if self.colormap[k][j] in ["white", "yellow"]:
                    self.pathmap[i][j]["down"] += 1
                    if self.colormap[k][j-1] in ["white", "yellow"] or self.colormap[k][j+1] in ["white", "yellow"]:
                        self.pathmap[i][j]["down_dead_end"] = False
                else:
                    break
                    
            for k in range(j-1, -1, -1):
                if self.colormap[i][k] in ["white", "yellow"]:
                    self.pathmap[i][j]["left"] += 1
                    if self.colormap[i-1][k] in ["white", "yellow"] or self.colormap[i+1][k] in ["white", "yellow"]:
                        self.pathmap[i][j]["left_dead_end"] = False
                else:
                    break                    

            for k in range(j+1, 15, 1):
                if self.colormap[i][k] in ["white", "yellow"]:
                    self.pathmap[i][j]["right"] += 1
                    if self.colormap[i-1][k] in ["white", "yellow"] or self.colormap[i+1][k] in ["white", "yellow"]:
                        self.pathmap[i][j]["right_dead_end"] = False
                else:
                    break

            if (self.colormap[i+1][j] != "white" and self.colormap[i-1][j] != "white") or (self.colormap[i][j+1] != "white" and self.colormap[i][j-1] != "white"):
                self.pathmap[i][j]["tunnel"] = True



class Box:
    """Create a box which responds to the character movement"""
    def __init__(self, x, y, board, character):
        """Establish the box class, with the color of the box"""
        self.x = x
        self.y = y
        self.board = board
        self.character = character
        self.color = "green"
        self.movement = Movement(self, self.board)

    def initiate_movement(self, dir):
        """Start the box's movement, repeating as many times as necesssary"""
        self.dir = dir
        self.cycles += 1
        if (self.detect_player() or self.board.pathmap[self.y][self.x]["tunnel"]) and self.cycles < 10:
            self.move_box() 
        
    def detect_player(self):
        """Check whether the player is close enough to initiate movement"""

        if (self.character.x in range(self.x-2, self.x+3) and self.character.y in range(self.y-2, self.y+3)) and self.player_visible() in range(4): 
            if self.character.x == self.x and self.character.y == self.y:
                return False
            return True

    def player_visible(self):
        """Check the direction that the player is visible from, or if a wall blocks the detection"""
        if self.character.y in range(self.y-1, self.y - self.board.pathmap[self.y][self.x]["up"]-1, -1) and self.character.x == self.x:
            return 0
        elif self.character.y in range(self.y+1, self.y + self.board.pathmap[self.y][self.x]["down"]+1, 1) and self.character.x == self.x:
            return 1
        elif self.character.x in range(self.x+1, self.x + self.board.pathmap[self.y][self.x]["right"]+1, 1) and self.character.y == self.y:
            return 2
        elif self.character.x in range(self.x-1, self.x - self.board.pathmap[self.y][self.x]["left"]-1, -1) and self.character.y == self.y:
            return 3
        else: 
            return 4

    def move_box(self):
        """Move the box per strict rules. The movement is not random and is always predictable given the same circumstances"""
        if (self.player_visible() == 1 and self.cycles == 1) or self.dir == "up":
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
        
        elif (self.player_visible() == 0 and self.cycles == 1) or self.dir == "down":
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

        elif (self.player_visible() == 3 and self.cycles == 1) or self.dir == "right":
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
        
        elif (self.player_visible() == 2 and self.cycles == 1) or self.dir == "left":
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

        self.initiate_movement(self.dir)             

    def check_end(self, dir):
        """Check against the pathmap whether it is a dead end or not"""
        return self.board.pathmap[self.y][self.x][dir]

    def move_up(self):
        """Move the box upwards one tile"""
        self.movement.move_up()
        self.dir = "up"

    def move_down(self):
        """Move the box downwards one tile"""
        self.movement.move_down()
        self.dir = "down"

    def move_right(self):
        """Move the box right one tile"""
        self.movement.move_right()
        self.dir = "right"

    def move_left(self):
        """Move the box left one tile"""
        self.movement.move_left()
        self.dir = "left"


class Character:
    """Create a character which can move around the board."""
    def __init__(self, x, y, board):
        """Create a character at the x and y positions given."""
        self.x = x
        self.y = y
        self.board = board
        self.color = "black"
        self.movement = Movement(self, self.board)

    def move_up(self):
        """Move the character up and starts the box movement"""
        self.movement.move_up()
        self.repeated_location_detection()
        self.board.box.cycles = 0
        self.board.box.initiate_movement(None)

    def move_down(self):
        """Move the character down and starts the box movement"""
        self.movement.move_down()
        self.repeated_location_detection()
        self.board.box.cycles = 0
        self.board.box.initiate_movement(None)

    def move_right(self):
        """Move the character right and starts the box movement"""
        self.movement.move_right()
        self.repeated_location_detection()
        self.board.box.cycles = 0
        self.board.box.initiate_movement(None)

    def move_left(self):
        """Move the character left and starts the box movement"""
        self.movement.move_left()
        self.repeated_location_detection()
        self.board.box.cycles = 0
        self.board.box.initiate_movement(None)

    def repeated_location_detection(self):
        """Check the players location on each turn"""
        if self.board.colormap[self.y][self.x] == "blue":
            self.board.game.next_level()
        
        if self.x == self.board.box.x and self.y == self.board.box.y:
            self.board.game.boxes += 1
            self.board.game.toolbar.boxes_caught.configure(text=f"Boxes caught: {self.board.game.boxes}/{len(self.board.game.levels)}")

    def actuated_location_detection(self):
        """Check the players location at certain moments"""
        if self.board.colormap[self.y][self.x] == "yellow":
            self.board.game.prev_level()


    
class Game:
    """Class for the game, establishing of seeds and the changing of levels"""
    def __init__(self, parent):
        """Creates a game window for the board to sit in"""
        self.parent = parent
        self.boxes = 0
        self.TILE_SIZE = 50
        self.colors = {"w": "white", "b": "blue", "r": "red", "g": "green", "y": "yellow"}

        self.curr_level = 0
        self.levels = []
        self.seeds = [["rrrrrrrrrrrrrrr",
                       "rrrrrrrrrwrwrrr",
                       "rrrrrrrwwwwwwrr",
                       "rrrrrrrrrrrwrrr",
                       "rrwwwwwwwwwwwrr",
                       "rrrrwrrwrrrrrrr",
                       "rrrrbrrwrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr","01:2,4:7,4:4,5"],
                       
                      ["rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrwr",
                       "rrrryrrrwwwwwwr",
                       "rrrrwrrrrrrwrrr",
                       "rrrrwwwwwwrwrrr",
                       "rrrrrrrrwrrwwwr",
                       "rrrrbwwwwwwwrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr","02:4,2:7,4:5,6"],

                       ["rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrbrrrwwwwwrr",
                       "rwwrwrrrwrwrwrr",
                       "rwwwwwwwwwwwwrr",
                       "rwwrwrrrrrwrrrr",
                       "rrrryrrrrwwwrrr",
                       "rrrrrrrrrrwrrrr",
                       "rrrrrrrrrrrrrrr","03:4,6:2,4:4,3"],
                       
                       ["rrrrrrrrrrrrrrr",
                       "rwwrwwwwrrrrrwr",
                       "rwwwwywwwwwwrwr",
                       "rrrrrwwwrrrwwwr",
                       "rbwwwwrrrwrwwwr",
                       "rrwwwrrwwwrwwwr",
                       "rrrwrrwwwwwwwwr",
                       "rrwwrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr","04:5,2:7,5:4,2"],
                       
                        ["rrrrrrrrrrrrrrr",
                       "rrrrrrwwwwwrrrr",
                       "rwwwwwwrwrwrrrr",
                       "rwrrrrwwwwwrrrr",
                       "ryrrbwwrwrwwwrr",
                       "rrrrrrwwwwwrwrr",
                       "rwrrrrrrwrrrwrr",
                       "rwwwwwwwwwwwwwr",
                       "rrrrrrrrrrrrrrr","05:1,4:5,2:6,4"],
                       
                        ["rrrrrrrrrrrrrrr",
                       "rrrrrrrwwwwrrrr",
                       "rrrrrwrwrrwrrrr",
                       "rrbrrwwwrrwrrrr",
                       "rrwwywrwwrwrrrr",
                       "rrwrrwrwwwwrrrr",
                       "rrwwwwwwwrwwrrr",
                       "rrrwrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr","06:4,4:2,6:2,4"],
                       
                        ["rrrrrrrrrrrrrrr",
                       "rrwwwwwrrrrwrrr",
                       "rrwrrrwwwwwwrrr",
                       "rryrwwwrrrrwrrr",
                       "rrrbwrwrwwrwrrr",
                       "rrrrwwwrwrwwrrr",
                       "rrrrrwwwwwwwrrr",
                       "rrrrrrrwwwwwrrr",
                       "rrrrrrrrrrrrrrr","07:2,3:6,2:3,4"],
                       
                        ["rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrryrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr","08:7,6:5,3:2,2"],
                       
                        ["rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrryrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr","09:7,6:5,3:2,2"],
                       
                        ["rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrrwrrrrrrr",
                       "rrrrrrryrrrrrrr",
                       "rrrrrrrrrrrrrrr",
                       "rrrrrrrrrrrrrrr","10:7,6:5,3:2,2"],]

        for seed in self.seeds:
            self.levels.append(Frame(self.parent.mainframe))

        self.toolbar = Toolbar(self.parent.mainframe, self, self.parent)

        self.establish_board(None)


    def establish_board(self, source): 
        """Creates the correct board for the current level, detects keypresses and calls the respective functions"""
        self.levels[self.curr_level].grid(row=1, column=0, columnspan=3)

        self.b = Board(self.seeds[self.curr_level], self, self.parent, source)

        self.toolbar.level_number.configure(text=self.curr_level+1)

        self.parent.parent.bind("<KeyRelease-w>", lambda i: self.b.character.move_up())
        self.parent.parent.bind("<KeyRelease-s>", lambda i: self.b.character.move_down())
        self.parent.parent.bind("<KeyRelease-d>", lambda i: self.b.character.move_right())
        self.parent.parent.bind("<KeyRelease-a>", lambda i: self.b.character.move_left())
        self.parent.parent.bind("<KeyRelease-f>", lambda i: self.b.character.actuated_location_detection())
        self.parent.parent.bind("<Return>", lambda i: self.toolbar.confirm_level())

    def prev_level(self):
        """Initiates the previous level"""
        self.levels[self.curr_level].grid_forget()
        self.curr_level -= 1
        self.establish_board("prev")

    def next_level(self):
        """Initiates the next level"""
        self.levels[self.curr_level].grid_forget()
        self.curr_level += 1
        self.establish_board("next")



class GUI:
    """Basic GUI class"""
    def __init__(self, parent):
        """Creates the GUI for the Game class to sit in, establishes its size"""
        self.parent = parent
        
        self.WINDOW_WIDTH = 750
        self.WINDOW_HEIGHT = 470

        self.mainframe = Frame(parent)

        self.mainframe.pack()

        self.game = Game(self)

        self.parent.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+200+200")
        self.parent.resizable(False, False)


class Movement:
    """Movement to be applied to the Box and Character classes"""
    def __init__(self, item, board):
        """Establishes an item to be moved"""
        self.item = item
        self.board = board

    def move_up(self):
        """Moves the item upwards, only if it is valid"""
        self.item.y -= 1
        try:
            if self.item.y < 0 or not self.check_validity():
                raise IndexError
            self.update_character("up")
        except IndexError:
            self.item.y += 1

    def move_down(self):
        """Moves the item downwards, only if it is valid"""
        self.item.y += 1
        try:
            if self.item.y > self.board.gui.WINDOW_HEIGHT or not self.check_validity():
                raise IndexError
            self.update_character("down")
        except IndexError:
            self.item.y -= 1

    def move_right(self):
        """Moves the item right, only if it is valid"""
        self.item.x += 1
        try:
            if self.item.x > self.board.gui.WINDOW_WIDTH or not self.check_validity():
                raise IndexError
            self.update_character("right")
        except IndexError:
            self.item.x -= 1

    def move_left(self):
        """Moves the item left, only if it is valid"""
        self.item.x -= 1
        try:
            if self.item.x < 0 or not self.check_validity():
                raise IndexError
            self.update_character("left")
        except IndexError:
            self.item.x += 1

    def check_validity(self):
        """Checks whether the movement direction is valid"""
        if self.board.colormap[self.item.y][self.item.x] == "red":
            return False
        else:
            return True
        
    def update_character(self, dir):
        """Updates the characters position on the visual board, and replaces the tile behind them as per the colormap"""
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
    """Create a toolbar above the board"""
    def __init__(self, frame, parent, GUI):
        """Create the toolbar at the top of the game"""
        self.frame = frame
        self.parent = parent
        self.GUI = GUI
        self.set_button()

        self.boxes_caught = Label(self.frame, text=f"Boxes caught: {self.parent.boxes}/{len(self.parent.levels)}")
        self.boxes_caught.grid(row=0, column=2)

    def set_button(self):
        """Make the level number into a button, also used for removing the entry widget once set"""
        self.level_number = Button(self.frame, width=10, text=f"{self.parent.curr_level+1}", command=self.change_level)
        self.level_number.grid(row=0, column=1)

    def change_level(self):
        """Change the level per the entry in the entry widget"""
        self.v = StringVar()
        self.level_number = Entry(self.frame, width=10, textvariable=self.v)
        self.level_number.grid(row=0, column=1)
        self.level_number.focus_set()

    def confirm_level(self):
        """Make sure that the level number entered is valid, else sets the level back to what it previously was"""
        try:
            self.parent.levels[self.parent.curr_level].grid_forget()
            if int(self.v.get())-1 <= len(self.parent.levels):
                self.parent.curr_level = int(self.v.get())-1 
            else:
                raise IndexError
            self.parent.establish_board(None)
            self.set_button()
        except ValueError:
            messagebox.showerror(title="Error", message="Invalid level")
            self.parent.establish_board(None)
            self.set_button()
        except IndexError:
            messagebox.showerror(title="Error", message=f"Level number too high! Maximum level is {len(self.parent.levels)}")
            self.parent.establish_board(None)
            self.set_button()



if __name__ == "__main__":
    root = Tk()
    GUI(root)
    root.mainloop()
