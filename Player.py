from Piece import Piece


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pieces = []
        # self.resetPieces()

    def addPiece(self, piece):
        self.pieces.append(piece)
        
    def getPieces(self):
        pieces = []
        for piece in self.pieces:
            if piece.inGame:
                pieces.append(piece)
        return pieces
    
    def getPlayerColor(self):
        return self.color

    def resetPieces(self):
        if self.color == "w":
            pawnRow = 1
            otherRow = 0
        else:
            pawnRow = 6
            otherRow = 7

        # set up pawns
        for col in range(8):
            pawnPiece = Piece("p", self.color, (pawnRow, col))
            self.pieces.append(pawnPiece)

        # set up other pieces
        self.pieces.append(Piece("k", self.color, (otherRow, 3)))
        self.pieces.append(Piece("q", self.color, (otherRow, 4)))
        self.pieces.append(Piece("r", self.color, (otherRow, 0)))
        self.pieces.append(Piece("r", self.color, (otherRow, 7)))
        self.pieces.append(Piece("n", self.color, (otherRow, 1)))
        self.pieces.append(Piece("n", self.color, (otherRow, 6)))
        self.pieces.append(Piece("b", self.color, (otherRow, 2)))
        self.pieces.append(Piece("b", self.color, (otherRow, 5)))
