import json
class Player:
    def __init__(self, name, gamesWon=0):
        self.name = name
        self.gamesWon = gamesWon
        self.gamesLost = 0
        self.IsKingOfHill = False
        self.currStreak=0
        self.WP = 100





    def addWin(self):
        self.gamesWon += 1
        self.currStreak=self.gamesWon
        self.calcWP()

    def addLoss(self):
        self.gamesLost += 1
        self.currStreak = 0
        self.calcWP()

    def makeKingOfHill(self):
        self.IsKingOfHill = True

    def dethrone(self):
        self.IsKingOfHill = False
        self.addLoss()

    def calcWP(self):
        self.WP = (self.gamesWon / (self.gamesLost + self.gamesLost)) * 100

    def setWin(self, num):
        self.gamesWon = num
