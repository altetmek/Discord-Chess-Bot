import json
class Player:
    def __init__(self, name, gamesWon=0):
        self.name = name
        self.gamesWon = gamesWon
        self.gamesLost = 0
        self.IsKingOfHill = False
        self.currStreak=0
        self.WP = 100

        self.add()

    def loaddata(self):
        with open('data.json') as json_file:
            data = json.load(json_file)
            return data

    def writedata(self, data):
        writing = open("data.json", "w")
        json.dump(data, writing)
        writing.close()

    def add(self):
        data = self.loaddata()

        data['people'].append({
            "name": self.name,
            "isKingOfHill": False,
            "gamesWon": 0,
            "gamesLost": 0,
            "currentStreak": 0,
            "WP": 100
        })
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

    def addWin(self):
        people = self.loaddata()["people"]
        index = self.getPlayerIndex
        people[index]["gamesWon"] += 1
        people[index]["currentStreak"] += 1
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

    def getPlayerIndex(self, name):
        data = self.loaddata()
        people = data["people"]
        playerIndex = people.index(name)
        return playerIndex