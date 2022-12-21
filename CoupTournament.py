from CoupPlayer import *
from CoupGame import CoupGame
import itertools
import random
UTILITY = [8,4,2,1]
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
            self.addPlayer(CoupPlayer("Strat 1-" + str(i)))
            self.addPlayer(CoupPlayer("Strat 2-" + str(i)))
            self.addPlayer(CoupPlayer("Strat 3-" + str(i)))
            self.addPlayer(CoupPlayer("Strat 4-" + str(i)))

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
        schedule = schedule[:2]

        self.schedule = schedule

'''
    def run(self):
        current_matchup = self.schedule[self.gamesPlayed]
        current_games
        for id in current_matchup:

        playRound()

    def playRound(self, player1, player2, player3, player4):

'''

if __name__ == "__main__":
    tournament = CoupTournament()
    tournament.createPlayers()
    tournament.createSchedule(100)


