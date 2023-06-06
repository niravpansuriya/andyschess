import pygame
from ChessBoard import ChessBoard
from Player import Player
from Piece import Piece
from defs import SCREEN_HEIGHT, SCREEN_WIDTH

def puzzle1(player1, player2):
    wPlayer = player1 if player1.getPlayerColor() == "w" else player2
    bPlayer = player1 if player1.getPlayerColor() == "b" else player2

    wPlayer.addPiece(Piece("q",wPlayer.getPlayerColor(), (4,2)))
    wPlayer.addPiece(Piece("n",wPlayer.getPlayerColor(), (3,2)))
    wPlayer.addPiece(Piece("b",wPlayer.getPlayerColor(), (3,3)))
    wPlayer.addPiece(Piece("r",wPlayer.getPlayerColor(), (3,4)))

    bPlayer.addPiece(Piece("r",bPlayer.getPlayerColor(), (4,3)))
    bPlayer.addPiece(Piece("r",bPlayer.getPlayerColor(), (4,4)))
    bPlayer.addPiece(Piece("b",bPlayer.getPlayerColor(), (2,2)))
    bPlayer.addPiece(Piece("q",bPlayer.getPlayerColor(), (2,3)))
    bPlayer.addPiece(Piece("n",bPlayer.getPlayerColor(), (2,4)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chess Board")

    player1 = Player("Nirav", "w")
    player2 = Player("Andy", "b")

    puzzle1(player1, player2)

    chessBoard = ChessBoard(screen, player1, player2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                chessBoard.handleClick(event.pos)
                
        if not running:
            break

        chessBoard.printBoard()
        chessBoard.printPieces()

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
