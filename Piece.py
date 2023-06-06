class Piece:
    def __init__(self, type, color, position):
        self.type = type
        self.color = color
        self.position = position
        self.inGame = True
    
    def isInGame(self):
        return self.inGame
    
    def removePiece(self):
        self.inGame = False
    
    def setPosition(self, position):
        self.position = position
        
    def getPosition(self):
        return self.position

    def getType(self):
        return self.type
    
    def getColor(self):
        return self.color