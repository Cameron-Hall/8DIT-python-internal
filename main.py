from tkinter import *
from tkinter import messagebox
import random

class GUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Sokoban")

        self.seed = """10x10:ryyyybgbbbryyyybbbbbryyyybbbbbrbbbbyybbbrbbbbyybbbrbbbbbbbbbrbbbbbbbbbrbbbbbbbbbrbbbbbbbbbrbbbbbbbbb"""

        self.TILE_SIZE = 25

        self.WINDOW_WIDTH = int(self.seed[0:2])
        self.WINDOW_HEIGHT = int(self.seed[3:5])
        self.parent.geometry(f"{self.WINDOW_WIDTH*self.TILE_SIZE}x{self.WINDOW_HEIGHT*self.TILE_SIZE}+200+200")

        if len(self.seed) != self.WINDOW_WIDTH*self.WINDOW_HEIGHT+6:
            messagebox.showerror("bad code", "stinky code")
            print(len(self.seed))
            print(self.WINDOW_WIDTH*self.WINDOW_HEIGHT+6)
        else:
            messagebox.showinfo("great code", "amazing")

        for i in range(self.WINDOW_HEIGHT):
            for j in range(self.WINDOW_WIDTH):
                color = self.seed[(i*self.WINDOW_HEIGHT)+j+6]
                if color == "b":
                    color = "blue"
                elif color == "r":
                    color = "red"
                elif color == "g":
                    color = "green"
                elif color == "y":
                    color = "yellow"
                
                f = Frame(self.parent, bg=color, width=self.TILE_SIZE, height=self.TILE_SIZE)
                f.grid(row=i, column=j)


if __name__ == "__main__":
    root = Tk()
    GUI(root)
    root.mainloop()