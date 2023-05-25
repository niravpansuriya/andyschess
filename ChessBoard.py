import pygame
from defs import SCREEN_WIDTH, COLOR_1, COLOR_2, ASSET_PATH


class ChessBoard:
    def __init__(self, screen, player1, player2):
        self.screen = screen
        self.player1 = player1
        self.player2 = player2

    def printPieces(self):
        self.printPiecesForPlayer(self.player1)
        self.printPiecesForPlayer(self.player2)

    def printPiecesForPlayer(self, player):
        playerColor = player.getPlayerColor()
        pieces = player.getPieces()

        #print pawns
        for position in pieces["p"]:
            self.putPiece("p", playerColor, position)

    def putPiece(self, piece, color, position):
        row, col = position
        if row < 0 or row > 7 or col < 0 or col > 7:
            raise Exception("Invalid row or col")

        squareSize = SCREEN_WIDTH / 8

        path = f"{ASSET_PATH}/{color}/{piece}.png"

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
