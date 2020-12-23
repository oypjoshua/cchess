import numpy as np

# b - black, r - red
# R - Rook, H - Horse, C - cannon, E - elephant, G - guard, K - king P - Pawn


class GameState():
    def __init__(self):
        self.board = np.array([
            ["bR", "bH", "bE", "bG", "bK", "bG", "bE", "bH", "bR", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "bC", "--", "--", "--", "--", "--", "bC", "--", ],
            ["bP", "--", "bP", "--", "bP", "--", "bP", "--", "bP", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", ],
            ["rP", "--", "rP", "--", "rP", "--", "rP", "--", "rP", ],
            ["--", "rC", "--", "--", "--", "--", "--", "rC", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", ],
            ["rR", "rH", "rE", "rG", "rK", "rG", "rE", "rH", "rR", ]
        ])

        self.redToMove = True
        self.moveLog = []
        self.redKing = (9, 4)
        self.blackKing = (0, 4)

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        if move.pieceMoved == 'rK':
            self.redKing = move.endSq
        if move.pieceMoved == 'bK':
            self.blackKing = move.endSq
        # (move.startSq, move.endSq, move.pieceMoved, move.pieceCaptured)
        self.redToMove = not self.redToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.redToMove = not self.redToMove
            if move.pieceMoved == "rK":
                self.redKing = move.startSq
            if move.pieceMoved == "bK":
                self.blackKing = move.startSq

    def getValidMoves(self):
        validMoves = []
        possibleMoves = self.getAllPossibleMoves()
        boardState = self.board
        if self.redToMove:
            for movement in possibleMoves:
                hypotheticalMove = Move(movement[0], movement[1], boardState)
                self.makeMove(hypotheticalMove)
                if self.redUnderCheck() == False:
                    validMoves.append(hypotheticalMove.moveID)
                    self.undoMove()
                else:
                    self.undoMove()
        else:
            for movement in possibleMoves:
                hypotheticalMove = Move(movement[0], movement[1], boardState)
                self.makeMove(hypotheticalMove)
                if self.blackUnderCheck() == False:
                    validMoves.append(hypotheticalMove.moveID)
                    self.undoMove()
                else:
                    self.undoMove()
        return validMoves

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                turn = self.board[r][c][0]
                if (turn == "r" and self.redToMove) or (turn == "b" and not self.redToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'E':
                        self.getElephantMoves(r, c, moves)
                    elif piece == 'G':
                        self.getGuardMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'C':
                        self.getCannonMoves(r, c, moves)
                    elif piece == 'H':
                        self.getHorseMoves(r, c, moves)

        return moves

    def getPawnMoves(self, r, c, moves):
        if self.redToMove:
            if r == 5 or r == 6:
                pawnMoveDown = Move((r, c), (r - 1, c), self.board)
                if pawnMoveDown.notOwnPiece:
                    moves.append(pawnMoveDown.moveID)
            elif r == 0:
                if c == 0:
                    pawnMoveRight = Move((r, c), (r, c + 1), self.board)
                    if pawnMoveRight.notOwnPiece:
                        moves.append(pawnMoveRight.moveID)
                elif c == 8:
                    pawnMoveLeft = Move((r, c), (r, c - 1), self.board)
                    if pawnMoveLeft.notOwnPiece:
                        moves.append(pawnMoveLeft.moveID)
                else:
                    pawnMoveLeft = Move((r, c), (r, c - 1), self.board)
                    pawnMoveRight = Move((r, c), (r, c + 1), self.board)
                    if pawnMoveLeft.notOwnPiece:
                        moves.append(pawnMoveLeft.moveID)
                    if pawnMoveRight.notOwnPiece:
                        moves.append(pawnMoveRight.moveID)
            else:
                pawnMoveDown = Move((r, c), (r - 1, c), self.board)
                if pawnMoveDown.notOwnPiece:
                    moves.append(pawnMoveDown.moveID)
                if c == 0:
                    pawnMoveRight = Move((r, c), (r, c + 1), self.board)
                    if pawnMoveRight.notOwnPiece:
                        moves.append(pawnMoveRight.moveID)
                elif c == 8:
                    pawnMoveLeft = Move((r, c), (r, c - 1), self.board)
                    if pawnMoveLeft.notOwnPiece:
                        moves.append(pawnMoveLeft.moveID)
                else:
                    pawnMoveLeft = Move((r, c), (r, c - 1), self.board)
                    pawnMoveRight = Move((r, c), (r, c + 1), self.board)
                    if pawnMoveLeft.notOwnPiece:
                        moves.append(pawnMoveLeft.moveID)
                    if pawnMoveRight.notOwnPiece:
                        moves.append(pawnMoveRight.moveID)
        else:
            if r == 3 or r == 4:
                moves.append(Move((r, c), (r + 1, c), self.board).moveID)
            elif r == 9:
                if c == 0:
                    moves.append(Move((r, c), (r, c + 1), self.board).moveID)
                elif c == 8:
                    moves.append(Move((r, c), (r, c - 1), self.board).moveID)
                else:
                    moves.append(Move((r, c), (r, c - 1), self.board).moveID)
                    moves.append(Move((r, c), (r, c + 1), self.board).moveID)
            else:
                if c == 0:
                    moves.append(Move((r, c), (r, c + 1), self.board).moveID)
                elif c == 8:
                    moves.append(Move((r, c), (r, c - 1), self.board).moveID)
                else:
                    moves.append(Move((r, c), (r, c - 1), self.board).moveID)
                    moves.append(Move((r, c), (r, c + 1), self.board).moveID)
                moves.append(Move((r, c), (r + 1, c), self.board).moveID)

    def getElephantMoves(self, r, c, moves):
        if r == 9 or r == 4:
            if self.board[r-1][c-1] == '--':
                elephantMoveLeft = Move((r, c), (r-2, c-2), self.board)
                if elephantMoveLeft.notOwnPiece:
                    moves.append(elephantMoveLeft.moveID)
            if self.board[r-1][c+1] == '--':
                elephantMoveRight = Move((r, c), (r-2, c+2), self.board)
                if elephantMoveRight.notOwnPiece:
                    moves.append(elephantMoveRight.moveID)
        elif r == 0 or r == 5:
            if self.board[r+1][c-1] == '--':
                elephantMoveLeft = Move((r, c), (r+2, c-2), self.board)
                if elephantMoveLeft.notOwnPiece:
                    moves.append(elephantMoveLeft.moveID)
            if self.board[r+1][c+1] == '--':
                elephantMoveRight = Move((r, c), (r+2, c+2), self.board)
                if elephantMoveRight.notOwnPiece:
                    moves.append(elephantMoveRight.moveID)
        else:
            if c == 0 or c == 4:
                if self.board[r+1][c+1] == '--':
                    elephantMoveDown = Move((r, c), (r+2, c+2), self.board)
                    if elephantMoveDown.notOwnPiece:
                        moves.append(elephantMoveDown.moveID)
                if self.board[r-1][c+1] == '--':
                    elephantMoveUp = Move((r, c), (r-2, c+2), self.board)
                    if elephantMoveUp.notOwnPiece:
                        moves.append(elephantMoveUp.moveID)
            if c == 4 or c == 8:
                if self.board[r+1][c-1] == '--':
                    elephantMoveDown = Move((r, c), (r+2, c-2), self.board)
                    if elephantMoveDown.notOwnPiece:
                        moves.append(elephantMoveDown.moveID)
                if self.board[r-1][c-1] == '--':
                    elephantMoveUp = Move((r, c), (r-2, c-2), self.board)
                    if elephantMoveUp.notOwnPiece:
                        moves.append(elephantMoveUp.moveID)

    def getGuardMoves(self, r, c, moves):
        if self.redToMove:
            if c != 4:
                moveGuardCenter = Move((r, c), (8, 4), self.board)
                if moveGuardCenter.notOwnPiece:
                    moves.append(moveGuardCenter.moveID)
            else:
                fourMoves = [(9, 5), (9, 3), (7, 5), (7, 3)]
                for moveGuard in fourMoves:
                    moveGuardAround = Move((r, c), moveGuard, self.board)
                    if moveGuardAround.notOwnPiece:
                        moves.append(moveGuardAround.moveID)
        else:
            if c != 4:
                moveGuardCenter = Move((r, c), (1, 4), self.board)
                if moveGuardCenter.notOwnPiece:
                    moves.append(moveGuardCenter.moveID)
            else:
                fourMoves = [(0, 5), (0, 3), (2, 5), (2, 3)]
                for moveGuard in fourMoves:
                    moveGuardAround = Move((r, c), moveGuard, self.board)
                    if moveGuardAround.notOwnPiece:
                        moves.append(moveGuardAround.moveID)

    def getKingMoves(self, r, c, moves):
        if c == 3 or c == 4:
            moveKingRight = Move((r, c), (r, c+1), self.board)
            if moveKingRight.notOwnPiece:
                moves.append(moveKingRight.moveID)
        if c == 4 or c == 5:
            moveKingLeft = Move((r, c), (r, c-1), self.board)
            if moveKingLeft.notOwnPiece:
                moves.append(moveKingLeft.moveID)
        if r in [0, 1, 7, 8]:
            moveKingDown = Move((r, c), (r+1, c), self.board)
            if moveKingDown.notOwnPiece:
                moves.append(moveKingDown.moveID)
        if r in [1, 2, 8, 9]:
            moveKingUp = Move((r, c), (r-1, c), self.board)
            if moveKingUp.notOwnPiece:
                moves.append(moveKingUp.moveID)

    def getRookMoves(self, r, c, moves):
        turn = self.board[r][c][0]
        stateUp = 1
        stateDown = 1
        stateLeft = 1
        stateRight = 1
        row = r
        col = c
        while stateUp == 1 and row > 0:
            if self.board[row - 1][c] == '--':
                moveRookUp = Move((r, c), (row - 1, c), self.board)
                moves.append(moveRookUp.moveID)
                row = row - 1
            elif self.board[row - 1][c][0] == turn:
                # for own piece dont append moves
                stateUp = 2
            else:
                moveRookUp = Move((r, c), (row - 1, c), self.board)
                moves.append(moveRookUp.moveID)
                stateUp = 2
        row = r
        col = c
        while stateDown == 1 and row < 9:
            if self.board[row + 1][c] == '--':
                moveRookDown = Move((r, c), (row + 1, c), self.board)
                moves.append(moveRookDown.moveID)
                row = row + 1
            elif self.board[row + 1][c][0] == turn:
                # for own piece dont append moves
                stateDown = 2
            else:
                moveRookDown = Move((r, c), (row + 1, c), self.board)
                moves.append(moveRookDown.moveID)
                stateDown = 2
        row = r
        col = c
        while stateLeft == 1 and col > 0:
            if self.board[r][col - 1] == '--':
                moveRookLeft = Move((r, c), (r, col - 1), self.board)
                moves.append(moveRookLeft.moveID)
                col = col - 1
            elif self.board[r][col - 1][0] == turn:
                # for own piece dont append moves
                stateLeft = 2
            else:
                moveRookLeft = Move((r, c), (r, col - 1), self.board)
                moves.append(moveRookLeft.moveID)
                stateLeft = 2
        row = r
        col = c
        while stateRight == 1 and col < 8:
            if self.board[r][col + 1] == '--':
                moveRookRight = Move((r, c), (r, col + 1), self.board)
                moves.append(moveRookRight.moveID)
                col = col + 1
            elif self.board[r][col + 1][0] == turn:
                # for own piece dont append moves
                stateRight = 2
            else:
                moveRookRight = Move((r, c), (r, col + 1), self.board)
                moves.append(moveRookRight.moveID)
                stateRight = 2

    def getCannonMoves(self, r, c, moves):
        turn = self.board[r][c][0]
        stateUp = 1
        stateDown = 1
        stateLeft = 1
        stateRight = 1
        row = r
        col = c
        while stateUp == 1 and row > 0:
            if self.board[row - 1][c] == '--':
                moveCannonUp = Move((r, c), (row - 1, c), self.board)
                moves.append(moveCannonUp.moveID)
                row = row - 1
            else:
                row = row - 1
                stateUp = 2
        # v for cannon passed first piece, checking if there is anything to eat behind
        while stateUp == 2 and row > 0:
            if self.board[row - 1][c] == '--':
                row = row - 1
            elif self.board[row - 1][c][0] == turn:
                stateUp = 3
            else:
                moveCannonUp = Move((r, c), (row - 1, c), self.board)
                moves.append(moveCannonUp.moveID)
                stateUp = 3
        row = r
        col = c
        while stateDown == 1 and row < 9:
            if self.board[row + 1][c] == '--':
                moveCannonDown = Move((r, c), (row + 1, c), self.board)
                moves.append(moveCannonDown.moveID)
                row = row + 1
            else:
                rowDown = row + 1
                stateDown = 2
        # v for cannon passed first piece, checking if there is anything to eat behind
        while stateDown == 2 and rowDown < 9:
            if self.board[rowDown + 1][c] == '--':
                rowDown = rowDown + 1
            elif self.board[rowDown + 1][c][0] == turn:
                stateDown = 3
            else:
                moveCannonDown = Move((r, c), (rowDown + 1, c), self.board)
                moves.append(moveCannonDown.moveID)
                stateDown = 3
        row = r
        col = c
        while stateLeft == 1 and col > 0:
            if self.board[r][col - 1] == '--':
                moveCannonLeft = Move((r, c), (r, col - 1), self.board)
                moves.append(moveCannonLeft.moveID)
                col = col - 1
            else:
                col = col - 1
                stateLeft = 2
        # v for cannon passed first piece, checking if there is anything to eat behind
        while stateLeft == 2 and col > 0:
            if self.board[r][col - 1] == '--':
                col = col - 1
            elif self.board[r][col - 1][0] == turn:
                stateLeft = 3
            else:
                moveCannonLeft = Move((r, c), (r, col - 1), self.board)
                moves.append(moveCannonLeft.moveID)
                stateLeft = 3

        row = r
        col = c
        while stateRight == 1 and col < 8:
            if self.board[r][col + 1] == '--':
                moveCannonRight = Move((r, c), (r, col + 1), self.board)
                moves.append(moveCannonRight.moveID)
                col = col + 1
            else:
                col = col + 1
                stateRight = 2

        # v for cannon passed first piece, checking if there is anything to eat behind
        while stateRight == 2 and col < 8:
            if self.board[r][col + 1] == '--':
                col = col + 1
            elif self.board[r][col + 1][0] == turn:
                stateRight = 3
            else:
                moveCannonRight = Move((r, c), (r, col + 1), self.board)
                moves.append(moveCannonRight.moveID)
                stateRight = 3

    def getHorseMoves(self, r, c, moves):
        if r != 9 and r != 8:
            if self.board[r + 1][c] == '--':
                if c < 8:
                    moveHorseDownRight = Move(
                        (r, c), (r + 2, c + 1), self.board)
                    if moveHorseDownRight.notOwnPiece:
                        moves.append(moveHorseDownRight.moveID)
                if c > 0:
                    moveHorseDownLeft = Move(
                        (r, c), (r + 2, c - 1), self.board)
                    if moveHorseDownLeft.notOwnPiece:
                        moves.append(moveHorseDownLeft.moveID)
        if r != 0 and r != 1:
            if self.board[r - 1][c] == '--':
                if c < 8:
                    moveHorseUpRight = Move(
                        (r, c), (r - 2, c + 1), self.board)
                    if moveHorseUpRight.notOwnPiece:
                        moves.append(moveHorseUpRight.moveID)
                if c > 0:
                    moveHorseUpLeft = Move(
                        (r, c), (r - 2, c - 1), self.board)
                    if moveHorseUpLeft.notOwnPiece:
                        moves.append(moveHorseUpLeft.moveID)
        if c != 8 and c != 7:
            if self.board[r][c + 1] == '--':
                if r < 9:
                    moveHorseRightDown = Move(
                        (r, c), (r + 1, c + 2), self.board)
                    if moveHorseRightDown.notOwnPiece:
                        moves.append(moveHorseRightDown.moveID)
                if r > 0:
                    moveHorseRightUp = Move((r, c), (r - 1, c + 2), self.board)
                    if moveHorseRightUp.notOwnPiece:
                        moves.append(moveHorseRightUp.moveID)
        if c != 0 and c != 1:
            if self.board[r][c - 1] == '--':
                if r < 9:
                    moveHorseLeftDown = Move(
                        (r, c), (r + 1, c - 2), self.board)
                    if moveHorseLeftDown.notOwnPiece:
                        moves.append(moveHorseLeftDown.moveID)
                if r > 0:
                    moveHorseLeftUp = Move((r, c), (r - 1, c - 2), self.board)
                    if moveHorseLeftUp.notOwnPiece:
                        moves.append(moveHorseLeftUp.moveID)

    def blackUnderCheck(self):
        storage = self.redToMove
        underCheck = False
        self.redToMove = True
        redMoves = self.getAllPossibleMoves()
        for squares in redMoves:
            if squares[1] == self.blackKing:
                underCheck = True
        if self.redKing[1] == self.blackKing[1] and underCheck == False:
            underCheck = True
            for inBetween in range(self.blackKing[0] + 1, self.redKing[0]):
                if self.board[inBetween][self.redKing[1]] != "--":
                    underCheck = False
        self.redToMove = storage
        return underCheck

    def redUnderCheck(self):
        storage = self.redToMove
        underCheck = False
        self.redToMove = False
        blackMoves = self.getAllPossibleMoves()
        for squares in blackMoves:
            if squares[1] == self.redKing:
                underCheck = True
        if self.redKing[1] == self.blackKing[1] and underCheck == False:
            underCheck = True
            for inBetween in range(self.blackKing[0] + 1, self.redKing[0]):
                if self.board[inBetween][self.redKing[1]] != "--":
                    underCheck = False
        self.redToMove = storage
        return underCheck

# 123


class Move():
    def __init__(self, startSq, endSq, board):
        self.startSq = startSq
        self.endSq = endSq
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = (startSq, endSq, board)
        self.notOwnPiece = (self.pieceMoved[0] != self.pieceCaptured[0])

    def withinBoard(self):
        if self.endSq[0] >= 0 and self.endSq[0] <= 9 and self.endSq[1] >= 0 and self.endSq[1] <= 8:
            return True
        else:
            return False
