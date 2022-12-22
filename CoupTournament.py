from CoupPlayer import *
from CoupGame import CoupGame
import itertools
import random
from datetime import datetime

from Agents.AutomatedAgent import *
from Agents.BluffingLongVisionAgent import *
from Agents.BluffingShortVisionAgent import *
from Agents.TruthfulLongVisionAgent import *
from Agents.TruthfulShortVisionAgent import *

UTILITY = [8,4,2,1]
STR_TIME = datetime.now().strftime("%b%d_%H%M")
FILE_CSV = "./Results/" + STR_TIME + ".csv"
FILE_TXT = "./Results/" + STR_TIME + "_utilities.txt"
PLAYERS_PER_GAME = 4


class CoupTournament:

    def __init__(self):
        self.players = {}
        self.gamesPlayed = 0
        self.schedule = []
        self.utils = {}

    def addPlayer(self, player:CoupPlayer):
        assert isinstance(player, CoupPlayer)
        self.players[player.id] = player
        self.utils[player.id] = 0
        print(player.name, "is in the tournament")

    # create players to add to the tournament.
    # if repeat > 1 then there can be more than 1 of the same player type in one game
    def createPlayers(self, repeat:int = 1):
        for i in range(repeat):
            self.addPlayer(TruthfulShortVisionAgent())
            self.addPlayer(BluffingShortVisionAgent())
            self.addPlayer(TruthfulLongVisionAgent())
            self.addPlayer(BluffingLongVisionAgent())

    # returns a list of games with length > minGames, where every player plays equal amounts
    # if uniqueGames = False, then players can play against themselves
    def createSchedule(self, minGames:int):
        playerIds = []        
        #playerIds = [1,2,3,4,5,6,7,8]
        schedule = []
        for id in self.players:
            playerIds.append(id)
                
        # all 4-length permutations of player ids
        possibilities = [p for p in itertools.permutations(playerIds, PLAYERS_PER_GAME)]

        while (len(schedule) < minGames):
                schedule += possibilities

        random.shuffle(schedule)        

        print("Schedule created with total", len(schedule), "games")

        # confirm that players play approx the same amount of games
        # allowance for difference in games is scheduleLeeway
        games = {}      # number of games that a player is scheduled
        order = {}      # if we want to verify that player order is equal
        for id in playerIds:
            games[id] = 0
            order[id] = [0]*PLAYERS_PER_GAME

        for game in schedule:
            for i in range(PLAYERS_PER_GAME):
                order[game[i]][i] += 1
                games[game[i]] += 1

        mostPlayed = 0
        leastPlayed = -1
        for id in games:
            if games[id] > mostPlayed:
                mostPlayed = games[id]
            if (leastPlayed == -1) or (games[id] < leastPlayed):
                leastPlayed = games[id]
        print("Least and most played:", leastPlayed, mostPlayed)
        scheduleLeeway = 0.05   
        assert (leastPlayed + int(minGames * scheduleLeeway) >= mostPlayed)

        # COMMENT THIS OUT
        #print("***Trimming schedule to 2 games for debugging :)")
        #schedule = schedule[:2]

        self.schedule = schedule


    def run(self):
        self.writeToCsv(["First", "Second", "Third", "Fourth"], new=True)
        for i in range(len(self.schedule)):
            self.playRound()
            self.gamesPlayed += 1

        f = open(FILE_TXT, "w")
        for id in self.players:
            output = str(id) + ": " + self.players[id].name + ", " + str(self.utils[id])
            print(output)
            f.write(output + "\n")
        f.close()

    def playRound(self):
        current_matchup_ids = self.schedule[self.gamesPlayed]
        current_matchup = []
        for id in current_matchup_ids:
            current_matchup.append(self.players[id])
        
        game = CoupGame()
        for player in current_matchup:
            game.addPlayer(player)
        
        assert game.playerCount == PLAYERS_PER_GAME

        rankings = game.run(endgame=True)
        rankingsId = []
        resultString = "GAME OVER: "
        for i in range(PLAYERS_PER_GAME):
            rankings[i].newGame()

            self.utils[rankings[i].id] += UTILITY[i]
            rankingsId.append(rankings[i].id)
            
            resultString += rankings[i].name
            resultString += " "

        print(resultString)
        self.writeToCsv(rankingsId)

    # store results to CSV file. 
    # If the game is starting then wipe the file, otherwise append
    def writeToCsv(self, data, new:bool = False):
        mode = "a"
        if (new):
            mode = "w"

        f = open(FILE_CSV, mode)
        for i in range(len(data)):
            f.write(str(data[i]))
            if (i == len(data) - 1):
                f.write("\n")
            else:
                f.write(",")

        f.close()

    

if __name__ == "__main__":
    tournament = CoupTournament()
    tournament.createPlayers()
    tournament.createSchedule(100)
    tournament.run()

