import random

from frisbee_simulator_web.models import TournamentTeam, Game, Team


class TeamInGameSimulation(TournamentTeam):
    def __init__(self, tournamentTeam):
        super().__init__()
        self.team = tournamentTeam.team
        self.coinFlipChoice = None
        self.startPointWithDisc = None
        self.oLineP1 = self.team.o_line_players.all()[0]
        self.oLineP2 = self.team.o_line_players.all()[1]
        self.oLineP3 = self.team.o_line_players.all()[2]
        self.oLineP4 = self.team.o_line_players.all()[3]
        self.oLineP5 = self.team.o_line_players.all()[4]
        self.oLineP6 = self.team.o_line_players.all()[5]
        self.oLineP7 = self.team.o_line_players.all()[6]
        self.dLineP1 = self.team.d_line_players.all()[0]
        self.dLineP2 = self.team.d_line_players.all()[1]
        self.dLineP3 = self.team.d_line_players.all()[2]
        self.dLineP4 = self.team.d_line_players.all()[3]
        self.dLineP5 = self.team.d_line_players.all()[4]
        self.dLineP6 = self.team.d_line_players.all()[5]
        self.dLineP7 = self.team.d_line_players.all()[6]
        self.benchP1 = self.team.bench_players.all()[0]
        self.benchP2 = self.team.bench_players.all()[1]
        self.benchP3 = self.team.bench_players.all()[2]
        self.benchP4 = self.team.bench_players.all()[3]
        self.benchP5 = self.team.bench_players.all()[4]
        self.benchP6 = self.team.bench_players.all()[5]
        self.benchP7 = self.team.bench_players.all()[6]


class GameSimulation(Game):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.teamOne = TeamInGameSimulation(game.team_one)
        self.teamTwo = TeamInGameSimulation(game.team_two)
        self.sevenOnFieldForTeamOne = self.teamOne.team.o_line_players
        self.sevenOnFieldForTeamTwo = self.teamTwo.team.d_line_players
        self.teamOneScore = 0
        self.teamTwoScore = 0
        self.discLocationY = 0
        self.betterTeam = 0
        self.differenceInTeamsOverallRating = 0
        self.probabilityForWinner = 0
        self.winner = self.teamOne
        self.gameOver = False

    def coin_flip(self):
        self.teamOne.coinFlipChoice = 1
        self.teamTwo.coinFlipChoice = 2
        coinFlip = random.randint(1, 2)
        if coinFlip == 1:
            self.teamOne.startPointWithDisc = True
            self.teamTwo.startPointWithDisc = False
            print("Team 1 won the disc flip")
        else:
            self.teamOne.startPointWithDisc = False
            self.teamTwo.startPointWithDisc = True
            print("Team 2 won the disc flip")

    def simulate_point(self):
        self.determiner = random.randint(1, 100)
        self.pointWinner = 0  # 1 means team1, 2 means team2

        if self.teamOne.startPointWithDisc:
            print('teamOne has disc to start')
            self.sevenOnFieldForTeamOne = self.teamOne.team.o_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.d_line_players
            self.discLocationY = 0
            if self.betterTeam == self.teamOne:
                # Team 1 has better chance to hold as better team
                if self.determiner <= (self.probabilityForWinner + 10):
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                # Team 2 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
            elif self.betterTeam == self.teamTwo:
                # Team 1 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner) + 10:
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                # Team 2 breaks as the better team
                else:
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
        else:
            self.sevenOnFieldForTeamOne = self.teamOne.team.d_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.o_line_players
            self.discLocationY = 70
            if self.betterTeam == self.teamTwo:
                # Team 2 has better chance to hold as better team
                if self.determiner <= (self.probabilityForWinner + 10):
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                # Team 1 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
            elif self.betterTeam == self.teamOne:
                # Team 2 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner) + 10:
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                # Team 1 breaks as the better team
                else:
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1

    def simulate_full_game(self):
        while not self.gameOver:
            self.simulate_point()
            print('team 1: ', self.teamOneScore)
            print('team 2: ', self.teamTwoScore)
            self.determine_next_points_info()

    def calculate_difference_in_teams_overall_rating(self):
        if self.teamOne.team.overall_rating > self.teamTwo.team.overall_rating:
            self.betterTeam = self.teamOne
            self.difference_in_teams_overall_rating = self.teamOne.team.overall_rating - self.teamTwo.team.overall_rating
        else:
            self.betterTeam = self.teamTwo
            self.difference_in_teams_overall_rating = self.teamTwo.team.overall_rating - self.teamOne.team.overall_rating

    def calculate_probability_for_winner(self):
        self.probability_for_winner = self.difference_in_teams_overall_rating + 50

    def determine_next_points_info(self):
        if self.pointWinner == self.teamOne:
            self.teamOne.startPointWithDisc = False
            self.teamTwo.startPointWithDisc = True
            self.teamOneScore += 1
            self.discLocationY = 70
        elif self.pointWinner == self.teamTwo:
            self.teamOne.startPointWithDisc = True
            self.teamTwo.startPointWithDisc = False
            self.teamTwoScore += 1
            self.discLocationY = 0
        if (self.teamOneScore == 15) or (self.teamTwoScore == 15):
            self.gameOver = True
        else:
            self.gameOver = False
