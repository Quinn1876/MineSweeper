from tkinter import Tk, Frame, Widget, Label, Text, Button
import tkinter
from random import randint

DEBUG=True

class Main(Tk):
    width = 250
    height = 300
    def __init__(self):
        super().__init__()
        self.__title = "Minesweeper"
        header = Header(master=self, title=self.__title); header.pack(fill=tkinter.X, expand=0)
        mineField = MineField(master=self, width = 16, height=16, numBombs=32); mineField.pack(fill=tkinter.BOTH, expand=0)

    @classmethod
    def run(cls):
        app = cls()
        #app.geometry("{}x{}".format(cls.width, cls.height))
        app.title(app.__title)
        app.mainloop()


class Header(Frame):
    def __init__(self, master, title):
        super().__init__(master)
        self.padleft = Label(master=self); self.padleft.pack(side=tkinter.LEFT, expand=1)
        self.title = Label(master=self, text=title); self.title.pack(side=tkinter.LEFT, expand=0)
        self.happyFace = tkinter.PhotoImage(file="happyFace.png")
        self.deadFace = tkinter.PhotoImage(file="deadFace.png")
        self.shadeFace = tkinter.PhotoImage(file="shadeFace.png")
        self.suprisedFace = tkinter.PhotoImage(file="suprisedFace.png")
        self.restartButton = Button(master=self, image=self.happyFace); self.restartButton.pack(side=tkinter.LEFT, expand=0)

        self.padright = Label(master=self); self.padright.pack(side=tkinter.RIGHT, expand=1)

class MineField(Frame):
    def __init__(self, master, width, height, numBombs):
        super().__init__(master, bd=5, relief=tkinter.SUNKEN)
        self.master = master
        self.__mineCoordinates = MineField.genBombs(numBombs, width, height)
        self.__mineMap = [['' for i in range(width)] for j in range(height)]
        for i in range(height):
            for j in range(width):
                if (j,i) in self.__mineCoordinates:
                    self.__mineMap[i][j] = MineSquare(master=self, width=10, height=10, bomb=True); self.__mines[i][j].grid(row=i, column=j)
                    self.incrementBombCounter(row=i, column=j)
                else:
                    self.__mineMap[i][j] = MineSquare(master=self, width=10, height=10); self.__mines[i][j].grid(row=i, column=j)

    def gameOver(self):
        # Display all of the bombs
        # TODO : IMPLEMENT
        pass

    @staticmethod
    def genBombs(numBombs, width, height):
        mineCords = [(-1,-1)]
        x, y = -1, -1
        for i in range(numBombs):
            while (x, y) in mineCords:
                x = randint(0, width-1)
                y = randint(0, height-1)
            mineCords.append((x,y))
        return mineCords[1:]

    def resetGame(self):
        # TODO : IMPLEMENT
        pass

    def incrementBombCounter(self, row, column):
      self.__mineMap[row][column].incrementNearBombs()
      if row == 0:
        if column == 0:
          self.__mineMap[row][column+1].incrementNearBombs()
          self.__mineMap[row+1][column].incrementNearBombs()
          self.__mineMap[row+1][column+1].incrementNearBombs()
        elif column == len(self.__mineMap[row]):
          self.__mineMap[row][column-1].incrementNearBombs()
          self.__mineMap[row+1][column].incrementNearBombs()
          self.__mineMap[row+1][column-1].incrementNearBombs()
        else:
          self.__mineMap[row][column+1].incrementNearBombs()
          self.__mineMap[row+1][column].incrementNearBombs()
          self.__mineMap[row+1][column+1].incrementNearBombs()
          self.__mineMap[row][column-1].incrementNearBombs()
          self.__mineMap[row+1][column-1].incrementNearBombs()
      elif row == len(self.__mineMap):
        if column == 0:
          self.__mineMap[row][column+1].incrementNearBombs()
          self.__mineMap[row-1][column].incrementNearBombs()
          self.__mineMap[row-1][column+1].incrementNearBombs()
        elif column == len(self.__mineMap[row]):
          self.__mineMap[row][column-1].incrementNearBombs()
          self.__mineMap[row-1][column].incrementNearBombs()
          self.__mineMap[row-1][column-1].incrementNearBombs()
        else:
          self.__mineMap[row][column+1].incrementNearBombs()
          self.__mineMap[row-1][column].incrementNearBombs()
          self.__mineMap[row-1][column+1].incrementNearBombs()
          self.__mineMap[row][column-1].incrementNearBombs()
          self.__mineMap[row-1][column-1].incrementNearBombs()
      else:
        if column == 0:
          self.__mineMap[row][column+1].incrementNearBombs()
          self.__mineMap[row-1][column].incrementNearBombs()
          self.__mineMap[row-1][column+1].incrementNearBombs()
          self.__mineMap[row+1][column].incrementNearBombs()
          self.__mineMap[row+1][column+1].incrementNearBombs()
        elif column == len(self.__mineMap[row]):
          self.__mineMap[row][column-1].incrementNearBombs()
          self.__mineMap[row-1][column].incrementNearBombs()
          self.__mineMap[row-1][column-1].incrementNearBombs()
          self.__mineMap[row+1][column].incrementNearBombs()
          self.__mineMap[row+1][column-1].incrementNearBombs()
        else:
          self.__mineMap[row][column+1].incrementNearBombs()
          self.__mineMap[row-1][column].incrementNearBombs()
          self.__mineMap[row-1][column+1].incrementNearBombs()
          self.__mineMap[row+1][column].incrementNearBombs()
          self.__mineMap[row+1][column+1].incrementNearBombs()
          self.__mineMap[row][column-1].incrementNearBombs()
          self.__mineMap[row-1][column-1].incrementNearBombs()
          self.__mineMap[row+1][column-1].incrementNearBombs()




class MineSquare(Button):

    def __init__(self, master, width, height, bomb=False):
        super().__init__(master, command=self.sweep)
        self.blankSquare = tkinter.PhotoImage(file="blankSquare.png")
        self.flagSquare = tkinter.PhotoImage(file="flag.png")
        self.__isBomb = bomb
        self.__nearBombs = 0
        self.__isRevealed = False
        self.__hasFlag = False
        if DEBUG and bomb:
            self.config(image=self.flagSquare, width=width, height=height)
            self.__hasFlag = True
        else:
            self.config(image=self.blankSquare, width=width, height=height)

        self.bind("<Button-3>", self.markFlag)


    def sweep(self):
        # TODO : IMPLEMENT
        if self.__isBomb:
            self.master.gameOver()

        pass

    def markFlag(self, event):
        # Bind this to right click
        if not self.__isRevealed:
            self.__hasFlag = not self.__hasFlag
            if self.__hasFlag:
                self.config(image=self.flagSquare)
            else:
                self.config(image=self.blankSquare)

    @property
    def nearBombs(self):
        return self.__nearBombs

    @nearBombs.setter
    def nearBombs(self, value):
        self.__nearBombs = value

    def incrementNearBombs(self):
      self.__nearBombs += 1


app = Main.run()
