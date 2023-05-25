import pygame
from ChessBoard import ChessBoard
from Player import Player
from defs import SCREEN_HEIGHT, SCREEN_WIDTH


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chess Board")

    player1 = Player("Nirav", "white")
    player2 = Player("Andy", "black")

    chessBoard = ChessBoard(screen, player1, player2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        chessBoard.printBoard()
        chessBoard.printPieces()

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
