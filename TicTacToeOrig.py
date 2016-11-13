from time import *
from graphics import *
import sys

BLANK = " "
X = "X"
O = "O"

WIN = 100    #Points awarded to the computer for a win
LOSS = -100  #Points awarded to the computer for a loss
TIE = 0     #Points awarded to the computer for a tie

NO_WIN = "NO_WIN"

EMPTY = "EMPTY"

COMP = X
PLAYER = O


def main():
    #try:
        turnNumber = 0
        window = Window("Tic-Tac-Toe", 500, 700)
        opponent = Computer()
        board = Board(EMPTY, 500, 500)
        
        #Loops until a player wins or there is a tie
        while (board.checkForWin(turnNumber) == NO_WIN):
            window.draw(board);
            #If turn number is even, the computer (X) goes
            if (turnNumber % 2 == 0):
                opponent.selectBestMove(board, COMP, turnNumber, True)
                turnNumber += 1
            #If turn number is odd, the player (O) goes
            else:
                while (turnNumber % 2 == 1):
                    window.displayText("Select a move!", board)
                    c, r = window.getMouseEntry(board)
                    if (board.isEmptyAt(c, r)):
                        window.displayText("Good move!", board)
                        board.setValueAt(c, r, PLAYER)
                        turnNumber += 1
                    else:
                        window.displayText("Invalid move!", board)
            board.draw(window)
            time.sleep(1)
    
            if (board.checkForWin(turnNumber) == TIE):
                window.displayText("Tie!", board)
            if (board.checkForWin(turnNumber) == PLAYER):
                window.displayText("You win!", board)
            if (board.checkForWin(turnNumber) == COMP):
                window.displayText("You lose!", board)
        
        time.sleep(2)
#except:
#print("Something went wrong")




class Window:
    text = BLANK
    
    #Creates a window given a title, width, and height
    def __init__(self, title, width, height):
        self.window = GraphWin(title, width, height)
        self.width = width
        self.height = height
    
    #Draws the console at the bottom of the screen
    def draw(self, board):
        rect = Rectangle(Point(0, board.getHeight()), Point(self.width, self.height))
        rect.setFill('black')
        rect.draw(self.getWindow())
    
    #Returns the coordinates of the entry clicked on
    def getMouseEntry(self, board):
        point = self.window.getMouse()
        return int(point.getX() / board.getWidth() * 3), int(point.getY() / board.getHeight() * 3)
    
    #Displays text in the window
    def displayText(self, text, board):
        if (self.text != BLANK):
            (self.text).undraw()
        self.text = Text(Point(self.window.getWidth() / 2.0, (self.window.getHeight() - board.getHeight()) / 2 + board.getHeight()), text)
        (self.text).setStyle('italic')
        (self.text).setSize(32)
        (self.text).setFill('green')
        (self.text).draw(self.getWindow())
    
    def getWindow(self):
        return self.window
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height




class Table:
    #Creates a 3x3 copied from the inputted table
    def __init__(self, table):
        if (table == EMPTY):
            self.table = [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK]
        else:
            self.table = list(table)

    #Sets the entry at the given x, y coordinates to the given value
    def setValueAt(self, x, y, value):
        self.table[y * 3 + x] = value
    
    #Gets the entry at the given x, y coordinates
    def getValueAt(self, x, y):
        return self.table[y * 3 + x]
    
    #Finds the largest value in the table
    #Returns the coordinates of the largest value and the largest value
    def getLargestValue(self):
        largestValue = LOSS - 1
        row = 0
        column = 0
        for y in range (3):
            for x in range (3):
                if (self.getValueAt(x, y) != BLANK and self.getValueAt(x, y) > largestValue):
                    largestValue = self.getValueAt(x, y)
                    row = y
                    column = x

        return column, row, largestValue

    #Finds the smallest value in the table
    #Returns the coordinates of the smallest value and the smallest value
    def getSmallestValue(self):
        smallestValue = WIN + 1
        row = 0
        column = 0
        for y in range (3):
            for x in range (3):
                if (self.getValueAt(x, y) != BLANK and self.getValueAt(x, y) < smallestValue):
                    smallestValue = self.getValueAt(x, y)
                    row = y
                    column = x
    
        return column, row, smallestValue

    #Returns the array containing the board
    def getTable(self):
        return self.table




class Board:
    def __init__(self, board, width, height):
        if (board == EMPTY):
            self.board = Table(EMPTY)
        else:
            self.board = Table(board.getBoard().getTable())
        self.width = width
        self.height = height

    def draw(self, window):
        for y in range (1, 3):
            Line(Point(0, y * self.height / 3.0), Point(self.width, y * self.height / 3.0)).draw(window.getWindow())
        for x in range (1, 3):
            Line(Point(x * self.width / 3.0, 0), Point(x * self.width / 3.0, self.height)).draw(window.getWindow())

        for x in range (3):
            for y in range (3):
                point = Point(x * self.width / 3.0 + self.width / 6.0, y * self.height / 3.0 + self.height / 6.0)
                if (self.board.getValueAt(x, y) == O):
                    image = Image(point, 'o.gif')
                if (self.board.getValueAt(x, y) == X):
                    image = Image(point, 'x.gif')
                if (self.board.getValueAt(x, y) != BLANK):
                    image.draw(window.getWindow())

    def isEmptyAt(self, x, y):
        return (self.board.getValueAt(x, y) == BLANK)
    
    def setValueAt(self, x, y, x_or_o):
        self.board.setValueAt(x, y, x_or_o)
    
    #Checks if the game has ended
    #Returns X or O if game ended in a win,
    #TIE if the game tied and NO_WIN if the game has not ended
    def checkForWin(self, turnNumber):
        if (turnNumber < 5):
            return NO_WIN
        #Checks for any vertical wins
        for x in range (3):
            if (self.board.getValueAt(x, 0) != BLANK and
                self.board.getValueAt(x, 0) == self.board.getValueAt(x, 1) and
                self.board.getValueAt(x, 0) == self.board.getValueAt(x, 2)):
                return self.board.getValueAt(x, 0)
        #Checks for any horizontal wins
        for y in range (3):
            if (self.board.getValueAt(0, y) != BLANK and
                self.board.getValueAt(0, y) == self.board.getValueAt(1, y) and
                self.board.getValueAt(0, y) == self.board.getValueAt(2, y)):
                return self.board.getValueAt(0, y)
        #Checks for any diagonal wins
        if (self.board.getValueAt(0, 0) != BLANK and
            self.board.getValueAt(0, 0) == self.board.getValueAt(1, 1) and
            self.board.getValueAt(0, 0) == self.board.getValueAt(2, 2)):
            return self.board.getValueAt(1, 1)
        if (self.board.getValueAt(2, 0) != BLANK and
            self.board.getValueAt(2, 0) == self.board.getValueAt(1, 1) and
            self.board.getValueAt(2, 0) == self.board.getValueAt(0, 2)):
            return self.board.getValueAt(1, 1)
            
        if (turnNumber == 9):
            return TIE
            
        return NO_WIN;

    #Returns the board, ONLY USED BY THE BOARD OBJECT
    def getBoard(self):
        return self.board
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height




class Computer:
    def makeMove(self, board, player, turnNumber):
        self.selectBestMove(boardCopy, PLAYER, turnNumber)
    
    #Selects the best next move using a minimax algorithm
    #Input: player - player whose move it is (X or O),
    #firstGameState - only false when the function is called from itself
    #Returns WIN if game is won by the computer
    def selectBestMove(self, board, player, turnNumber, firstGameState):
        #List of scores for the NEXT gamestates, NOT INPUTTED GAMESTATE
        if (turnNumber == 0):
            board.setValueAt(1, 1, COMP)
            return
        scores = Table(EMPTY)
        for y in range (3):
            for x in range (3):
                if (board.isEmptyAt(x, y)):
                    #Create a copy of the inputted gamestate
                    boardCopy = Board(board, 0, 0)
                    boardCopy.setValueAt(x, y, player)
                    #If the computer wins, assign +10 to the previous gamestate
                    #If the player wins, assign +10 to the previous gamestate
                    if (boardCopy.checkForWin(turnNumber) == COMP):
                        scores.setValueAt(x, y, WIN - turnNumber)
                    if (boardCopy.checkForWin(turnNumber) == PLAYER):
                        scores.setValueAt(x, y, LOSS)
                    if (boardCopy.checkForWin(turnNumber) == TIE):
                        scores.setValueAt(x, y, TIE)
                    if (boardCopy.checkForWin(turnNumber) == NO_WIN):
                        if (player == PLAYER):
                            scores.setValueAt(x, y, self.selectBestMove(boardCopy, COMP, turnNumber + 1, False))
                        if (player == COMP):
                            scores.setValueAt(x, y, self.selectBestMove(boardCopy, PLAYER, turnNumber + 1, False))

        if (player == PLAYER):
            column, row, score = scores.getSmallestValue()
        if (player == COMP):
            column, row, score = scores.getLargestValue()
        
        if (firstGameState):
            board.setValueAt(column, row, player)
        else:
            return score



main()
