import pygame
import math
from defs import SCREEN_WIDTH, COLOR_1, COLOR_2, ASSET_PATH, SELECTED_CELL_COLOR


class ChessBoard:
    def __init__(self, screen, player1, player2):
        self.screen = screen
        self.player1 = player1
        self.player2 = player2
        self.turn = ""
        self.selectedCells = []
        self.lastClickedCell = None
        self.gameOver = False

    def isValidRow(self, row):
        return row >= 0 and row <= 7

    def isValidCol(self, col):
        return col >= 0 and col <= 7

    def printPieces(self):
        self.printPiecesForPlayer(self.player1)
        self.printPiecesForPlayer(self.player2)

    def printPiecesForPlayer(self, player):
        playerColor = player.getPlayerColor()
        pieces = player.getPieces()

        for piece in pieces:
            if piece.isInGame():
                self.putPiece(piece=piece)

    def putPiece(self, piece):
        if not self.gameOver:
            row, col = piece.getPosition()
            if row < 0 or row > 7 or col < 0 or col > 7:
                raise Exception("Invalid row or col")

            squareSize = SCREEN_WIDTH / 8

            path = f"{ASSET_PATH}/{piece.getColor()}/{piece.getType()}.png"

            self.screen.blit(
                pygame.transform.scale(pygame.image.load(path), (squareSize, squareSize)),
                (col * squareSize, row * squareSize),
            )

    def printBoard(self):
        if self.gameOver:
            self.screen.fill((0,0,0))
            self.drawGameOver()
        else:
            squareSize = SCREEN_WIDTH / 8

            for row in range(8):
                for col in range(8):
                    x = row * squareSize
                    y = col * squareSize

                    color = COLOR_1 if (row + col) % 2 else COLOR_2

                    pygame.draw.rect(self.screen, color, (x, y, squareSize, squareSize))
                    self.highlightSelectedCells()

    def moveChessPiece(self, piece, position):
        pieceOnTheTarget = self.getSelectedPiece(position)
        if pieceOnTheTarget:
            if pieceOnTheTarget.getColor() != piece.getColor():
                pieceOnTheTarget.removePiece()
            else:
                return

        piece.setPosition(position)
        self.turn = piece.getColor()
        self.swapTurn()

        if self.isGameOver():
            self.gameOver = True
            print("game over")

    def swapTurn(self):
        if self.turn:
            self.turn = "w" if self.turn == "b" else "b"
        else:
            self.turn = "w"

    def highlightSelectedCells(self):
        squareSize = SCREEN_WIDTH / 8

        for cell in self.selectedCells:
            (row, col) = cell
            pygame.draw.rect(
                self.screen,
                SELECTED_CELL_COLOR,
                (col * squareSize, row * squareSize, squareSize, squareSize),
                3,
            )

    def getClickedCell(self, position):
        (x, y) = position
        squareSize = SCREEN_WIDTH / 8

        row = int(math.floor(y / squareSize))
        col = int(math.floor(x / squareSize))

        return (row, col)

    def addSelectedCell(self, position):
        (row, col) = position

        if self.isValidRow(row) and self.isValidCol(col):
            self.selectedCells.append(position)
        else:
            raise Exception("Invalid row or columns")

    def clearSelectedCells(self):
        self.clickedCell = None
        self.selectedCells = []
        self.lastClickedCell = None

    def clickAndHighlightNextMoves(self, position):
        self.clearSelectedCells()

        self.addSelectedCell(position)
        selectedPiece = self.getSelectedPiece(position)
        if selectedPiece:
            nextMoves = self.getNextMoves(piece=selectedPiece)
            self.selectedCells.extend(nextMoves)

    def drawGameOver(self):
        font = pygame.font.Font(None, 100)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(text, text_rect)

    def handleClick(self, position):
        if self.gameOver:
            return

        clickedCell = self.getClickedCell(position)
        if clickedCell and self.lastClickedCell and clickedCell == self.lastClickedCell:
            return

        # if already some cells are selected
        if len(self.selectedCells):
            # if clicked cell is legal move
            if clickedCell in self.selectedCells:
                selectedPiece = self.getSelectedPiece(self.lastClickedCell)
                self.moveChessPiece(selectedPiece, clickedCell)
                self.clearSelectedCells()

            # if not legal move
            else:
                # if clicked cell is empty
                if self.isCellEmpty(clickedCell) or not self.canClickOnTheCell(
                    clickedCell
                ):
                    self.clearSelectedCells()
                # if it is not empty
                else:
                    # select the clicked cell and highlight next moves
                    self.clickAndHighlightNextMoves(clickedCell)
                    self.lastClickedCell = clickedCell

        # if none of the cells are selected
        else:
            # if selected cell is empty
            if self.isCellEmpty(clickedCell) or not self.canClickOnTheCell(clickedCell):
                pass
            else:
                self.clickAndHighlightNextMoves(clickedCell)
                self.lastClickedCell = clickedCell

    def canClickOnTheCell(self, position):
        piece = self.getSelectedPiece(position)

        if piece:
            return not self.turn or piece.getColor() == self.turn
        else:
            return False

    def getSelectedPiece(self, position):
        for player in [self.player1, self.player2]:
            pieces = player.getPieces()

            for piece in pieces:
                if piece.isInGame() and position == piece.getPosition():
                    return piece
        return None

    def isCellEmpty(self, position):
        return not bool(self.getSelectedPiece(position))

    def removeOutsideMoves(self, moves):
        updatedMoves = []
        for move in moves:
            (x, y) = move
            if not (x < 0 or x > 7 or y < 0 or y > 7):
                updatedMoves.append(move)
        return updatedMoves

    def removeIllegalMoves(self, piece, moves):
        updatedMoves = []
        for move in moves:
            (x, y) = move
            pieceOnTheTarget = self.getSelectedPiece(move)
            if not pieceOnTheTarget:
                updatedMoves.append(move)
            elif pieceOnTheTarget.getColor() != piece.getColor():
                updatedMoves.append(move)
        return updatedMoves

    def isPawnsFirstMove(self, color, position):
        (row, col) = position
        desiredRow = 1 if color == "w" else 6
        return row == desiredRow

    def getNextMovesForKnight(self, piece):
        position = piece.getPosition()
        (row, col) = position

        nextMoves = [
            (row - 2, col - 1),
            (row - 2, col + 1),
            (row + 2, col - 1),
            (row + 2, col + 1),
            (row - 1, col - 2),
            (row + 1, col - 2),
            (row - 1, col + 2),
            (row + 1, col + 2),
        ]

        nextMoves = self.removeIllegalMoves(piece, self.removeOutsideMoves(nextMoves))

        return nextMoves

    def getNextMovesForRook(self, piece):
        position = piece.getPosition()
        (row, col) = position

        nextMoves = []

        firstEnemy = True

        for i in range(col + 1, 8):
            sp = self.getSelectedPiece((row, i))
            if not sp:
                nextMoves.append((row, i))
            else:
                if self.canAttackByColor(piece, sp) and firstEnemy:
                    nextMoves.append((row, i))
                    firstEnemy = False
                else:
                    break

        firstEnemy = True
        for i in range(col - 1, -1, -1):
            sp = self.getSelectedPiece((row, i))
            if not sp:
                nextMoves.append((row, i))
            else:
                if self.canAttackByColor(piece, sp) and firstEnemy:
                    nextMoves.append((row, i))
                    firstEnemy = False
                else:
                    break

        firstEnemy = True
        for i in range(row + 1, 8):
            sp = self.getSelectedPiece((i, col))
            if not sp:
                nextMoves.append((i, col))
            else:
                if self.canAttackByColor(piece, sp) and firstEnemy:
                    nextMoves.append((i, col))
                    firstEnemy = False
                else:
                    break

        firstEnemy = True
        for i in range(row - 1, -1, -1):
            sp = self.getSelectedPiece((i, col))
            if not sp:
                nextMoves.append((i, col))
            else:
                if self.canAttackByColor(piece, sp) and firstEnemy:
                    nextMoves.append((i, col))
                    firstEnemy = False
                else:
                    break

        return self.removeIllegalMoves(piece, self.removeOutsideMoves(nextMoves))

    def getNextMovesForBishop(self, piece):
        position = piece.getPosition()
        (row, col) = position
        nextMoves = []

        firstEnemy = True
        for i in range(1, 8):
            move = (row + i, col + i)
            sp = self.getSelectedPiece(move)
            if not sp:
                nextMoves.append(move)
            else:
                if self.canAttackByColor(piece, sp) and firstEnemy:
                    nextMoves.append(move)
                    firstEnemy = False
                else:
                    break

        firstEnemy = True
        for i in range(1, 8):
            move = (row - i, col + i)
            sp = self.getSelectedPiece(move)
            if not sp:
                nextMoves.append(move)
            else:
                if self.canAttackByColor(piece, sp) and firstEnemy:
                    nextMoves.append(move)
                    firstEnemy = False
                else:
                    break

        firstEnemy = True
        for i in range(1, 8):
            move = (row + i, col - i)
            sp = self.getSelectedPiece(move)
            if not sp:
                nextMoves.append(move)
            else:
                if self.canAttackByColor(piece, sp) and firstEnemy:
                    nextMoves.append(move)
                    firstEnemy = False
                else:
                    break

        firstEnemy = True
        for i in range(1, 8):
            move = (row - i, col - i)
            sp = self.getSelectedPiece(move)
            if not sp:
                nextMoves.append(move)
            else:
                if self.canAttackByColor(piece, sp) and firstEnemy:
                    nextMoves.append(move)
                    firstEnemy = False
                else:
                    break

        return self.removeIllegalMoves(piece, self.removeOutsideMoves(nextMoves))

    def getNextMovesForQueen(self, piece):
        nextMoves = []

        nextMoves.extend(self.getNextMovesForBishop(piece))
        nextMoves.extend(self.getNextMovesForRook(piece))

        return list(set(nextMoves))

    def getNextMovesForPawns(self, piece):
        position = piece.getPosition()
        (row, col) = position
        color = piece.getColor()
        isPawnsFirstMove = self.isPawnsFirstMove(color, position)

        nextMovesOffset = []
        if color == "w":
            nextMovesOffset = [(1, 0)]
        else:
            nextMovesOffset = [(-1, 0)]

        if isPawnsFirstMove:
            if color == "w":
                nextMovesOffset.append((2, 0))
            else:
                nextMovesOffset.append((-2, 0))

        nextMoves = []
        for moveOffset in nextMovesOffset:
            nextMoves.append((row + moveOffset[0], col + moveOffset[1]))
        nextMoves = self.removeOutsideMoves(nextMoves)
        return nextMoves

    def canAttackByColor(self, attacker, target):
        return attacker.getColor() != target.getColor()

    def canPieceAttackAnyOtherPiece(self, piece):
        nextMoves = self.getNextMoves(piece)

        for move in nextMoves:
            if self.getSelectedPiece(move):
                return True

        return False

    def isGameOver(self):
        playerWithTurn = (
            self.player1 if self.player1.getPlayerColor() == self.turn else self.player2
        )

        pieces = playerWithTurn.getPieces()

        for piece in pieces:
            if self.canPieceAttackAnyOtherPiece(piece):
                return False

        return True

    def getNextMoves(self, piece):
        if piece.getType() == "p":
            return self.getNextMovesForPawns(piece)

        elif piece.getType() == "r":
            return self.getNextMovesForRook(piece)

        elif piece.getType() == "n":
            return self.getNextMovesForKnight(piece)

        elif piece.getType() == "b":
            return self.getNextMovesForBishop(piece)

        elif piece.getType() == "q":
            return self.getNextMovesForQueen(piece)
        else:
            return []
