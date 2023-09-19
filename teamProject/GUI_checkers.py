# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Noah Saria
#               Minh Nguyen
#               Brendan Hon
#               Vijay Seetharam
# Section:      507
# Assignment:   Group Project
# Date:         01 05 2022
#
print("This program needs module pygame v2.1.2 installed IDE in order to run properly\n"
      "For more information, check the provided design document or visit https://pypi.org/project/pygame/")
print("Our group project game is checkers. It follows the standard ruleset for the game."
      "This program offers 2P and AI play. \nRed pieces will always have the first move and play as the AI.")
import pygame
import random

# Board and Piece Setup
pygame.init()
width, height = 800, 800
rows, cols = 8, 8
squareSize = width//cols
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)
green = (218, 247, 166)
crown = pygame.transform.scale(pygame.image.load('crown1.png'),(60, 30))
smallCircleRadius = 20
fps = 60
font = pygame.font.Font('freesansbold.ttf', 50)


win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Checkers")

def getGrid():
    '''
    Takes mouse input, and gets position of mouse to return as tuple.

    :return: tuple of mouse coordinates.

    '''
    pos = pygame.mouse.get_pos()
    return pos[1] // squareSize, pos[0] // squareSize


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.red_left = self.blue_left = 12
        self.red_kings = self.blue_kings = 0

    def drawSquares(self, win):
        '''
        Creates alternating checker pattern on board.

        :param win: pygame display window.

        :return: n/a
        '''
        win.fill(black)
        for row in range(rows):
            for col in range(row%2, cols, 2):
                pygame.draw.rect(win, white, (row*squareSize, col*squareSize,
                                              squareSize, squareSize))

    def createBoard(self):
        '''
        Creates functional board for gameplay in the form
        of an array of pieces.

        :return: n/a
        '''
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, red))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, blue))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)


    def draw(self, win):
        '''
        Draws pieces onto the board based on createboard array.

        :param win: pygame display window.

        :return: n/a
        '''
        self.drawSquares(win)
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] != 0:
                    self.board[row][col].draw(win)

    def remove(self, piece):
        '''
        Removes pieces from the board via capturing movement options.

        :param piece: piece object to be removed.
        :return: n/a
        '''
        self.board[piece.row][piece.col] = 0
        if piece.color == red:
            self.red_left -= 1
        else:
            self.blue_left -= 1

    def move(self, piece, newRow, newCol):
        '''
        Move piece from current position to valid position.

        :param piece: piece object to move.
        :param newRow: new row coordinate to move.
        :param newCol: new col coordinate to move.

        :return: n/a
        '''
        if abs(piece.row - newRow) == 2:
            self.remove(self.board[(piece.row + newRow) // 2][(piece.col + newCol) // 2])
        self.board[piece.row][piece.col] = 0
        piece.move(newRow, newCol)
        self.board[piece.row][piece.col] = piece


class Piece:
    padding = 10
    outline = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        if self.color == red:
            self.direction = 1
        else:
            self.direction = -1
        self.x = 0
        self.y = 0

    def calcPos(self):
        '''
        Calculates coordinates of a piece on the board.

        :return: n/a
        '''
        self.x = squareSize * self.col + squareSize//2
        self.y = squareSize * self.row + squareSize//2

    def make_king(self):
        '''
        Makes a piece a king piece.

        :return: n/a
        '''
        self.king = True

    def draw(self, win):
        '''
        Draws two circles (outline and main) for a piece given
        position, if king is true draw crown on top of piece.

        :param win: pygame display window.

        :return: n/a
        '''
        self.calcPos()
        radius = squareSize//2 - self.padding
        pygame.draw.circle(win, grey, (self.x, self.y), radius + self.outline)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(crown, (self.x-crown.get_width()//2, self.y-crown.get_height()//2))

    def move(self, row, col):
        '''
        Updates position, handles condition to become king.

        :param row: new position row
        :param col: new position col
        :return: n/a
        '''
        self.row = row
        self.col = col
        self.calcPos()
        if row == 0 or row == rows - 1:
            self.make_king()

    def posIfGoDirection(self, x, y, board, jumpMove):
        '''
        Returns coordinates of new position based on possible moves
        and jumping condition. Primarily used in posibleMove.

        :param x: Direction change in x axis integer.
        :param y: Direction change in y axis integer.
        :param board: board object.
        :param jumpMove: boolean dictating whether a move is a jump move.

        :return: list of coordinate if given move is possible.
        '''
        if self.row + x < 0 or self.row + x >= rows:
            return []
        if self.col + y < 0 or self.col + y >= cols:
            return []
        if not jumpMove and board.board[self.row + x][self.col + y] == 0:
            return [self.row + x, self.col + y]
        if board.board[self.row + x][self.col + y] == 0 or board.board[self.row + x][self.col + y].color == self.color:
            return []
        if self.row + x * 2 < 0 or self.row + x * 2 >= rows:
            return []
        if self.col + y * 2 < 0 or self.col + y * 2 >= cols:
            return []
        if board.board[self.row + x * 2][self.col + y * 2] == 0:
            return [self.row + x * 2, self.col + y * 2, board.board[self.row + x][self.col + y]]
        return []

    def posibleMove(self, board, jumpMove):
        '''
        Tests all possible moves given color, king etc. and returns a list
        for all possible moves, including captures.

        :param board: board object.
        :param jumpMove: boolean dictating whether a move is a jump move.

        :return: list of all possible move coordinates.
        '''
        positions = []
        dir = -1
        if self.color == red:
            dir = 1
        temp = self.posIfGoDirection(dir, -1, board, jumpMove)
        if len(temp):
            positions.append(temp)
        temp = self.posIfGoDirection(dir, 1, board, jumpMove)
        if len(temp):
            positions.append(temp)
        if self.king:
            temp = self.posIfGoDirection(-dir, -1, board, jumpMove)
            if len(temp):
                positions.append(temp)
            temp = self.posIfGoDirection(-dir, 1, board, jumpMove)
            if len(temp):
                positions.append(temp)
        return positions

    def displayPosibleMove(self, board, jumpMove):
        '''
        Displays all possible moves to user as grey circles for clicking.

        :param board: board object
        :param jumpMove: boolean dictating whether a move is a jump move.

        :return: n/a
        '''
        positions = self.posibleMove(board, jumpMove)
        for pos in positions:
            x = pos[0] * squareSize + squareSize // 2
            y = pos[1] * squareSize + squareSize // 2
            pygame.draw.circle(win, grey, (y, x), smallCircleRadius)
        pygame.display.update()


class Game2P:
    def __init__(self, win):
        self.turn = red
        self.board = Board()
        self.board.createBoard()
        self.win = win

    def changeTurn(self):
        '''
        Flips the turns, to other color's turn.

        :return: n/a
        '''
        if self.turn == red:
            self.turn = blue
        else:
            self.turn = red

    def gameIsEnded(self):
        '''
         Finds if one side has 0 pieces left, returns color of victor.

         :return: tuples blue or red of color value of victor.
                  boolean false if no victors found.
         '''
        if self.board.red_left == 0:
            return blue
        elif self.board.blue_left == 0:
            return red
        else:
            return False

    def play(self):
        '''
        Contains event loop and conditions for user input such as quitting,
        selecting, and moving pieces.

        :return: boolean True if exiting, False if game is continued.
        '''

        run = True
        row, col = getGrid()
        if self.board.board[row][col] == 0 or self.board.board[row][col].color != self.turn:
            return False
        piece = self.board.board[row][col]
        jumpMove = False
        piece.displayPosibleMove(self.board, jumpMove)
        possibleMove = piece.posibleMove(self.board, jumpMove)
        while run and len(possibleMove) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    newRow, newCol = getGrid()
                    validMove = False
                    for x in possibleMove:
                        if newRow == x[0] and newCol == x[1]:
                            # if selected move is a possible move
                            jumpMove = True
                            validMove = True
                            self.board.move(piece, x[0], x[1])
                            if len(x) == 3:
                                # this move is a capture move
                                if self.gameIsEnded():
                                    self.winingWindow()
                                    return True
                                possibleMove = piece.posibleMove(self.board, jumpMove)
                                numberOfPossibleCapturePieces = 0
                                for x in possibleMove:
                                    if len(x) == 3:
                                        numberOfPossibleCapturePieces += 1
                                if numberOfPossibleCapturePieces == 0:
                                    # there is no other possible jump
                                    self.changeTurn()
                                    return False
                            else:
                                self.changeTurn()
                                return False
                            break

                    if not validMove:
                        if jumpMove:
                            self.changeTurn()
                        return False
                    else:
                        self.board.draw(win)
                        piece.displayPosibleMove(self.board, jumpMove)
                        pygame.display.update()
        return False

    def ai(self):
        '''
        Contains ai decision making, moves and capturing for single player.

        :return: boolean True if exiting, False if game is continued.
        '''
        normalMoves = []
        captureMoves = []
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] and self.board.board[i][j].color == red:
                    currentPossibleMoves = self.board.board[i][j].posibleMove(self.board,False)
                    for x in currentPossibleMoves:
                        if len(x) == 3:
                            captureMoves.append([self.board.board[i][j], x])
                        else:
                            normalMoves.append([self.board.board[i][j], x])

        if len(captureMoves):  # AI behaviour for favorable moves (Capture/king)
            AIMove = random.choice(captureMoves)
        else:
            AIMove = random.choice(normalMoves)
        self.board.move(AIMove[0], AIMove[1][0], AIMove[1][1])
        self.changeTurn()
        self.board.draw(win)
        pygame.display.update()
        if self.gameIsEnded():
            self.winingWindow()
            return True
        return False

    def winingWindow(self):
        '''
        Displays victory screen depending on which color wins.

        :return: empty return when program is quit.
        '''
        winner = self.gameIsEnded()
        print(winner)
        if winner == blue:
            text = font.render('Blue is the winner', True, blue, green)
        else:
            text = font.render('red is the winner', True, red, green)
        run = True
        display_surface = pygame.display.set_mode((width, height))
        display_surface.fill(green)
        textRect = text.get_rect()
        textRect.center = (squareSize * 4, squareSize * 4)
        display_surface.blit(text, textRect)
        pygame.display.update()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

def homeScreen():
    '''
    Displays homescreen that gives palyer option for 2 players or
    single players.

    :return: n/a
    '''
    display_surface = pygame.display.set_mode((width, height))
    display_surface.fill(green)
    text1 = font.render('2 players mode', True, blue, green)
    text2 = font.render('Player vs. AI', True, blue, green)
    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect1.center = (squareSize * 4, squareSize * 3 + squareSize // 2)
    textRect2.center = (squareSize * 4, squareSize * 4 + squareSize // 2)
    display_surface.blit(text1, textRect1)
    display_surface.blit(text2, textRect2)
    pygame.display.update()

def AIMainProgram():
    '''
    Event loop for single player against AI.

    :return: empty return when program ended.
    '''
    run = True
    clock = pygame.time.Clock()
    game = Game2P(win)
    while run:
        clock.tick(fps)
        if game.turn == red:
            out = game.ai()
            if out:
                return
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    out = game.play()
                    if out:
                        return
        game.board.draw(win)
        pygame.display.update()
    pygame.quit()

def pvpMainProgram():
    '''
    Event loop for two player against human.

    :return: empty return when program ended.
    '''
    run = True
    clock = pygame.time.Clock()
    game = Game2P(win)
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                out = game.play()
                if out:
                    return
        game.board.draw(win)
        pygame.display.update()
    pygame.quit()

def main():
    run = True
    clock = pygame.time.Clock()
    type = ""
    while run:
        clock.tick(fps)
        homeScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 210 <= pos[0] <= 590 and 320 <= pos[1] <= 380:
                    type = '2p'
                    break
                elif 240 <= pos[0] <= 560 and 420 <= pos[1] <= 480:
                    type = 'ai'
                    break
        if len(type):
            break
    if type == 'ai':
        AIMainProgram()
    else:
        pvpMainProgram()


main()
