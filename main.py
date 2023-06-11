import pygame
from ChessBoard import ChessBoard
from Player import Player
from Piece import Piece
from Menu import Menu
from defs import SCREEN_HEIGHT, SCREEN_WIDTH


def puzzle1(player1, player2):
    wPlayer = player1 if player1.getPlayerColor() == "w" else player2
    bPlayer = player1 if player1.getPlayerColor() == "b" else player2

    wPlayer.addPiece(Piece("q", wPlayer.getPlayerColor(), (4, 2)))
    wPlayer.addPiece(Piece("n", wPlayer.getPlayerColor(), (3, 2)))
    wPlayer.addPiece(Piece("b", wPlayer.getPlayerColor(), (3, 3)))
    wPlayer.addPiece(Piece("r", wPlayer.getPlayerColor(), (3, 4)))

    bPlayer.addPiece(Piece("r", bPlayer.getPlayerColor(), (4, 3)))
    bPlayer.addPiece(Piece("r", bPlayer.getPlayerColor(), (4, 4)))
    bPlayer.addPiece(Piece("b", bPlayer.getPlayerColor(), (2, 2)))
    bPlayer.addPiece(Piece("q", bPlayer.getPlayerColor(), (2, 3)))
    bPlayer.addPiece(Piece("n", bPlayer.getPlayerColor(), (2, 4)))


def puzzle2(player1, player2):
    wPlayer = player1 if player1.getPlayerColor() == "w" else player2
    bPlayer = player1 if player1.getPlayerColor() == "b" else player2

    wPlayer.addPiece(Piece("n", wPlayer.getPlayerColor(), (0, 4)))
    wPlayer.addPiece(Piece("n", wPlayer.getPlayerColor(), (2, 2)))
    wPlayer.addPiece(Piece("r", wPlayer.getPlayerColor(), (0, 2)))
    wPlayer.addPiece(Piece("r", wPlayer.getPlayerColor(), (4, 2)))

    bPlayer.addPiece(Piece("b", bPlayer.getPlayerColor(), (3, 1)))
    bPlayer.addPiece(Piece("q", bPlayer.getPlayerColor(), (3, 4)))
    bPlayer.addPiece(Piece("n", bPlayer.getPlayerColor(), (2, 3)))
    bPlayer.addPiece(Piece("n", bPlayer.getPlayerColor(), (3, 0)))


def main():
    def handleMenuOptions(selectedOption):
        if selectedOption == menuOptions[0]:
            puzzle1(player1, player2)
        elif selectedOption == menuOptions[1]:
            puzzle2(player1, player2)
        elif selectedOption == menuOptions[-1]:
            exit()
        else:
            pass

    # initial setup of the screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # set the header
    pygame.display.set_caption("Chess Board")

    # check if menu should be shown or not
    showMenu = True

    # init menu object
    menuOptions = ["Level 1", "Level 2", "Level 3", "Exit"]
    menu = Menu(screen=screen, options=menuOptions)

    # init player1 and player2
    player1 = Player("Nirav", "w")
    player2 = Player("Andy", "b")

    # init chess board
    chessBoard = ChessBoard(screen, player1, player2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = event.pos
                if showMenu:
                    selectedOption = menu.getClickedOption(position)
                    if selectedOption:
                        handleMenuOptions(selectedOption)
                        showMenu = False
                else:
                    chessBoard.handleClick(position)

        if not running:
            break

        if showMenu:
            menu.showMenu()
        else:
            chessBoard.printBoard()
            chessBoard.printPieces()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
