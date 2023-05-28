import pygame
import math
from defs import SCREEN_WIDTH, COLOR_1, COLOR_2, ASSET_PATH, SELECTED_CELL_COLOR


class ChessBoard:
    def __init__(self, screen, player1, player2):
        self.screen = screen
        self.player1 = player1
        self.player2 = player2
        self.turn = "w"
        self.selectedCells = []
        self.lastClickedCell = None

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
            self.putPiece(piece=piece)

    def putPiece(self, piece):
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
        squareSize = SCREEN_WIDTH / 8

        for row in range(8):
            for col in range(8):
                x = row * squareSize
                y = col * squareSize

                color = COLOR_1 if (row + col) % 2 else COLOR_2

                pygame.draw.rect(self.screen, color, (x, y, squareSize, squareSize))
                self.highlightSelectedCells()

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

    def clickAndHighlightNextMoves(self, position):
        self.clearSelectedCells()

        self.addSelectedCell(position)
        selectedPiece = self.getSelectedPiece(position)
        if selectedPiece:
            nextMoves = self.getNextMoves(piece=selectedPiece)
            self.selectedCells.extend(nextMoves)

    def handleClick(self, position):
        clickedCell = self.getClickedCell(position)

        if clickedCell == self.lastClickedCell:
            return

        # if already some cells are selected
        if len(self.selectedCells):
            # if clicked cell is legal move
            if clickedCell in self.selectedCells:
                print("Move the piece and clear selection")
                self.clearSelectedCells()

            # if not legal move
            else:
                # if clicked cell is empty
                if self.isCellEmpty(clickedCell):
                    self.clearSelectedCells()
                # if it is not empty
                else:
                    # select the clicked cell and highlight next moves
                    self.clickAndHighlightNextMoves(clickedCell)

        # if none of the cells are selected
        else:
            # if selected cell is empty
            if self.isCellEmpty(clickedCell):
                pass
            else:
                self.clickAndHighlightNextMoves(clickedCell)

        self.lastClickedCell = clickedCell

    def getSelectedPiece(self, position):
        for player in [self.player1, self.player2]:
            pieces = player.getPieces()

            for piece in pieces:
                if position == piece.getPosition():
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

    def isPawnsFirstMove(self, color, position):
        (row, col) = position
        desiredRow = 1 if color == "w" else 6
        return row == desiredRow

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

    def getNextMoves(self, piece):
        if piece.getType() == "p":
            return self.getNextMovesForPawns(piece)
