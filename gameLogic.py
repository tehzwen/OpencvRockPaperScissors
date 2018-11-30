import random


class rockPaperScissorsGame:

    def __init__(self):
        self.choice = 0
        self.choices = ["rock", "paper", "scissors"]
        self.gesture = ""

    def makeChoice(self):
        for i in range(random.randint(0, 2)):
            self.choice = i
        
        self.gesture = self.choices[self.choice]

        
    def printChoice(self):
        print (self.gesture)


def runGame():
    game = rockPaperScissorsGame()
    game.makeChoice()

    return game.gesture

def handleWinner(player, computer):

    if (player == "rock" and computer == "scissors"):
        return "Player Wins!"

    elif (player == "scissors" and computer == "paper"):
        return "Player Wins!"

    elif (player == "paper" and computer == "rock"):
        return "Player Wins!"

    elif (computer == "rock" and player == "scissors"):
        return "Computer Wins!"

    elif (computer == "scissors" and player == "paper"):
        return "Computer Wins!"

    elif (computer == "paper" and player == "rock"):
        return "Computer Wins!"

    elif (player == ""):
        return "Need to make a move!"

    else:
        return "Its a tie!"