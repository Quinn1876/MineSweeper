from tkinter import Tk, Frame, Widget, Label, Text, Button
import tkinter
from random import randint

DEBUG=False

class Main(Tk):
    width = 250
    height = 300
    def __init__(self):
        super().__init__()
        self.__title = "Minesweeper"
        self.header = Header(master=self, title=self.__title, restartCommand=self.restartCommand); self.header.pack(fill=tkinter.X, expand=0)
        self.mineField = MineField(master=self, width = 16, height=16, numBombs=32); self.mineField.pack(fill=tkinter.BOTH, expand=0)
        self.iconbitmap('assets\\minesquare\\bomb.png')

    @classmethod
    def run(cls):
        app = cls()
        #app.geometry("{}x{}".format(cls.width, cls.height))
        app.title(app.__title)
        app.mainloop()

    def setFace(self, face):
        self.header.restartButton.config(image=self.header.__getattribute__(face+'Face'))

    def restartCommand(self, event=None):
        self.mineField.destroy()
        self.mineField = MineField(master=self, width = 16, height=16, numBombs=32); self.mineField.pack(fill=tkinter.BOTH, expand=0)

class Header(Frame):
    def __init__(self, master, title, restartCommand):
        super().__init__(master)
        self.padleft = Label(master=self); self.padleft.pack(side=tkinter.LEFT, expand=1)
        self.title = Label(master=self, text=title); self.title.pack(side=tkinter.LEFT, expand=0)
        self.happyFace = tkinter.PhotoImage(file="assets/faces/happyFace.png")
        self.deadFace = tkinter.PhotoImage(file="assets/faces/deadFace.png")
        self.shadeFace = tkinter.PhotoImage(file="assets/faces/shadeFace.png")
        self.suprisedFace = tkinter.PhotoImage(file="assets/faces/suprisedFace.png")
        self.restartButton = Button(master=self, image=self.happyFace, command=restartCommand); self.restartButton.pack(side=tkinter.LEFT, expand=0)

        self.padright = Label(master=self); self.padright.pack(side=tkinter.RIGHT, expand=1)

class MineField(Frame):
    def __init__(self, master, width, height, numBombs):
        super().__init__(master, bd=5, relief=tkinter.SUNKEN)
        self.master = master
        self.bomb = tkinter.PhotoImage(file='assets\\minesquare\\bomb.png')
        self.__numSquaresLeft = (width*height) - numBombs
        self.__mineCoordinates = MineField.genBombs(numBombs, width, height)
        self.__mineMap = [[MineSquare(master=self, width=15, height=15, position=(i,j)) for i in range(width)] for j in range(height)]
        for i in range(height):
            for j in range(width):
                if (j,i) in self.__mineCoordinates:
                    self.__mineMap[i][j].setBomb(); self.__mineMap[i][j].grid(row=i, column=j)
                    self.incrementBombCounter(row=i, column=j)
                else:
                   self.__mineMap[i][j].grid(row=i, column=j)

    def gameOver(self):
        for i in self.__mineMap:
            for mine in i:
                mine.config(state=tkinter.DISABLED)
        for row, column in self.__mineCoordinates:
            self.__mineMap[column][row].config(image=self.bomb, state=tkinter.DISABLED)
        if self.__numSquaresLeft != 0:
            self.master.setFace('dead')

    def squareRevealed(self):
        self.__numSquaresLeft -= 1
        if self.__numSquaresLeft == 0:
            self.master.setFace('shade')
            self.gameOver()

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
        elif column == len(self.__mineMap[row]) - 1:
          self.__mineMap[row][column-1].incrementNearBombs()
          self.__mineMap[row+1][column].incrementNearBombs()
          self.__mineMap[row+1][column-1].incrementNearBombs()
        else:
          self.__mineMap[row][column+1].incrementNearBombs()
          self.__mineMap[row+1][column].incrementNearBombs()
          self.__mineMap[row+1][column+1].incrementNearBombs()
          self.__mineMap[row][column-1].incrementNearBombs()
          self.__mineMap[row+1][column-1].incrementNearBombs()
      elif row == len(self.__mineMap) - 1:
        if column == 0:
          self.__mineMap[row][column+1].incrementNearBombs()
          self.__mineMap[row-1][column].incrementNearBombs()
          self.__mineMap[row-1][column+1].incrementNearBombs()
        elif column == len(self.__mineMap[row]) - 1:
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
        elif column == len(self.__mineMap[row]) - 1:
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

    def showNumbers(self, mineSquare):
        column, row = mineSquare.position
        if row == 0:
            if column == 0:
                self.__mineMap[row][column+1].showNumber()
                self.__mineMap[row+1][column].showNumber()
                self.__mineMap[row+1][column+1].showNumber()
            elif column == len(self.__mineMap[row]) - 1:
                self.__mineMap[row][column-1].showNumber()
                self.__mineMap[row+1][column].showNumber()
                self.__mineMap[row+1][column-1].showNumber()
            else:
                self.__mineMap[row][column+1].showNumber()
                self.__mineMap[row+1][column].showNumber()
                self.__mineMap[row+1][column+1].showNumber()
                self.__mineMap[row][column-1].showNumber()
                self.__mineMap[row+1][column-1].showNumber()
        elif row == len(self.__mineMap) - 1:
            if column == 0:
                self.__mineMap[row][column+1].showNumber()
                self.__mineMap[row-1][column].showNumber()
                self.__mineMap[row-1][column+1].showNumber()
            elif column == len(self.__mineMap[row]) - 1:
                self.__mineMap[row][column-1].showNumber()
                self.__mineMap[row-1][column].showNumber()
                self.__mineMap[row-1][column-1].showNumber()
            else:
                self.__mineMap[row][column+1].showNumber()
                self.__mineMap[row-1][column].showNumber()
                self.__mineMap[row-1][column+1].showNumber()
                self.__mineMap[row][column-1].showNumber()
                self.__mineMap[row-1][column-1].showNumber()
        else:
            if column == 0:
                self.__mineMap[row][column+1].showNumber()
                self.__mineMap[row-1][column].showNumber()
                self.__mineMap[row-1][column+1].showNumber()
                self.__mineMap[row+1][column].showNumber()
                self.__mineMap[row+1][column+1].showNumber()
            elif column == len(self.__mineMap[row]) - 1:
                self.__mineMap[row][column-1].showNumber()
                self.__mineMap[row-1][column].showNumber()
                self.__mineMap[row-1][column-1].showNumber()
                self.__mineMap[row+1][column].showNumber()
                self.__mineMap[row+1][column-1].showNumber()
            else:
                self.__mineMap[row][column+1].showNumber()
                self.__mineMap[row-1][column].showNumber()
                self.__mineMap[row-1][column+1].showNumber()
                self.__mineMap[row+1][column].showNumber()
                self.__mineMap[row+1][column+1].showNumber()
                self.__mineMap[row][column-1].showNumber()
                self.__mineMap[row-1][column-1].showNumber()
                self.__mineMap[row+1][column-1].showNumber()


class MineSquare(Button):

    def __init__(self, master, width, height, position, bomb=False):
        super().__init__(master, command=self.sweep)
        self.position = position
        self.master = master
        self.__blankSquare = tkinter.PhotoImage(file="assets/minesquare/blankSquare.png")
        self.__flagSquare = tkinter.PhotoImage(file="assets/minesquare/flag.png")
        self.__isBomb = bomb
        self.__nearBombs = 0
        self.__isRevealed = False
        self.__hasFlag = False
        self.config(image=self.__blankSquare, width=width, height=height)
        self.bind("<Button-3>", self.markFlag)

        MineSquare.defineNumberImages()

    @classmethod
    def defineNumberImages(cls):
        cls.numberMap = [
            tkinter.PhotoImage(file='assets/minesquare/clear.png'),
            tkinter.PhotoImage(file="assets/minesquare/one.png"),
            tkinter.PhotoImage(file="assets/minesquare/two.png"),
            tkinter.PhotoImage(file="assets/minesquare/three.png"),
            tkinter.PhotoImage(file="assets/minesquare/four.png"),
            tkinter.PhotoImage(file="assets/minesquare/five.png"),
            tkinter.PhotoImage(file="assets/minesquare/six.png"),
            tkinter.PhotoImage(file="assets/minesquare/seven.png"),
            tkinter.PhotoImage(file="assets/minesquare/eight.png")
        ]

    def sweep(self):
        # bound to left click
        # TODO : IMPLEMENT
        if self.__hasFlag:
          return
        if self.__isBomb:
            self.master.gameOver()
        else:
            self.showNumber()

    def showNumber(self):
        if self.__isRevealed:
            return
        self.__isRevealed = True
        if self.__isBomb:
            return
        if self.__nearBombs != 0:
            self.config(image=MineSquare.numberMap[self.__nearBombs if self.__nearBombs < 9 else 8], state=tkinter.DISABLED)
        else:
            self.config(image=MineSquare.numberMap[0], state=tkinter.DISABLED)
            self.master.showNumbers(self)



    def markFlag(self, event):
        # bound to right click
        if not self.__isRevealed:
            self.toggleFlag()

    def toggleFlag(self):
      self.__hasFlag = not self.__hasFlag
      self.config(image=self.__flagSquare) if self.__hasFlag else self.config(image=self.__blankSquare)

    @property
    def nearBombs(self):
        return self.__nearBombs

    @nearBombs.setter
    def nearBombs(self, value):
        self.__nearBombs = value

    def incrementNearBombs(self):
      self.__nearBombs += 1

    def setBomb(self):
      self.__isBomb = True
      if DEBUG:
        self.toggleFlag()

    def isBomb(self):
      return self.__isBomb





app = Main.run()
