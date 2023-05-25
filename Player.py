class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pieces = dict()
        self.resetPieces()

    def getPieces(self):
        return self.pieces

    def getPlayerColor(self):
        return self.color

    def resetPieces(self):
        if self.color == "white":
            pawnRow = 1
            otherRow = 0
        else:
            pawnRow = 6
            otherRow = 7

        self.pieces["p"] = []

        # set up pawns
        for col in range(8):
            self.pieces["p"].append((pawnRow, col))

        # set up other pieces
        self.pieces["k"] = (otherRow, 3)
        self.pieces["q"] = (otherRow, 4)
        self.pieces["r"] = [(otherRow, 0), (otherRow, 7)]
        self.pieces["n"] = [(otherRow, 1), (otherRow, 6)]
        self.pieces["b"] = [(otherRow, 2), (otherRow, 5)]
