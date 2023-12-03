import random

from frisbee_simulator_web.models import TournamentTeam, Game, Team


class TeamInGameSimulation:
    def __init__(self, tournamentTeam):
        super().__init__()
        self.tournamentTeam = tournamentTeam
        self.team = tournamentTeam.team
        self.coinFlipChoice = None
        self.startPointWithDisc = None
        self.startFirstHalfWithDisc = None
        self.startSecondHalfWithDisc = None
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


class GameSimulation:
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.teamOne = TeamInGameSimulation(self.game.team_one)
        self.teamTwo = TeamInGameSimulation(self.game.team_two)
        self.sevenOnFieldForTeamOne = self.teamOne.team.o_line_players
        self.sevenOnFieldForTeamTwo = self.teamTwo.team.d_line_players
        self.determiner = 0
        self.teamOneScore = 0
        self.teamTwoScore = 0
        self.discLocationY = 0
        self.betterTeam = 0
        self.differenceInTeamsOverallRating = 0
        self.probabilityForWinner = 0
        self.winner = self.teamOne.tournamentTeam
        self.loser = self.teamTwo.tournamentTeam
        self.pointWinner = self.teamOne
        self.gameOver = False
        self.firstPointOfFirstHalf = False
        self.firstPointOfSecondHalf = False
        self.startsFirstHalfWithDisc = None
        self.startsSecondHalfWithDisc = None

    def coin_flip(self):
        self.teamOne.coinFlipChoice = 1
        self.teamTwo.coinFlipChoice = 2
        coinFlip = random.randint(1, 2)
        return coinFlip

    def flip_team_start_with_disc_at_halftime(self):
        if self.teamOne.startSecondHalfWithDisc:
            self.teamOne.startPointWithDisc = True
        elif self.teamTwo.startSecondHalfWithDisc:
            self.teamTwo.startPointWithDisc = True

    def simulate_point_by_player_rating(self):
        self.pointWinner = 0  # 1 means team1, 2 means team2

        if self.teamOne.startPointWithDisc:
            print('teamOne has disc to start')
            self.sevenOnFieldForTeamOne = self.teamOne.team.o_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.d_line_players
            self.discLocationY = 0
            if self.betterTeam == self.teamOne:
                # Team 1 has better chance to hold as better team
                self.determiner = random.randint(1, 100)
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                    print('team 1 held as better team')
                # Team 2 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                    print('team 2 broke as worse team')
            elif self.betterTeam == self.teamTwo:
                # Team 1 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                    print('team 1 held as worse team ')
                # Team 2 breaks as the better team
                else:
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                    print('team 2 broke as better team')
        else:
            print('team 2 has disc to start')
            self.sevenOnFieldForTeamOne = self.teamOne.team.d_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.o_line_players
            self.discLocationY = 70
            if self.betterTeam == self.teamTwo:
                # Team 2 has better chance to hold as better team
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                    print('team 2 holds as better team')
                # Team 1 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                    print('team 1 breaks as worse team')
            elif self.betterTeam == self.teamOne:
                # Team 2 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                    print('team 2 holds as worse team')
                # Team 1 breaks as the better team
                else:
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                    print('team 1 breaks as better team')

    def simulate_point_by_team_rating(self):
        self.pointWinner = 0  # 1 means team1, 2 means team2

        if self.teamOne.startPointWithDisc:
            print('teamOne has disc to start')
            self.sevenOnFieldForTeamOne = self.teamOne.team.o_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.d_line_players
            self.discLocationY = 0
            if self.betterTeam == self.teamOne:
                # Team 1 has better chance to hold as better team
                self.determiner = random.randint(1, 100)
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                    print('team 1 held as better team')
                # Team 2 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                    print('team 2 broke as worse team')
            elif self.betterTeam == self.teamTwo:
                # Team 1 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                    print('team 1 held as worse team ')
                # Team 2 breaks as the better team
                else:
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                    print('team 2 broke as better team')
        else:
            print('team 2 has disc to start')
            self.sevenOnFieldForTeamOne = self.teamOne.team.d_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.o_line_players
            self.discLocationY = 70
            if self.betterTeam == self.teamTwo:
                # Team 2 has better chance to hold as better team
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                    print('team 2 holds as better team')
                # Team 1 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                    print('team 1 breaks as worse team')
            elif self.betterTeam == self.teamOne:
                # Team 2 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamTwo
                    self.teamTwoScore += 1
                    print('team 2 holds as worse team')
                # Team 1 breaks as the better team
                else:
                    self.pointWinner = self.teamOne
                    self.teamOneScore += 1
                    print('team 1 breaks as better team')

    def simulate_full_game(self):
        self.calculate_difference_in_teams_overall_rating()
        self.calculate_probability_for_winner()
        self.simulate_point_by_team_rating()
        self.setup_next_point()
        while not self.gameOver:
            self.simulate_point_by_team_rating()
            print('team 1: ', self.teamOneScore)
            print('team 2: ', self.teamTwoScore)
            if self.teamOneScore == 15:
                self.winner = self.teamOne.tournamentTeam
                self.loser = self.teamTwo.tournamentTeam
                self.game.winner_score = self.teamOneScore
                self.game.loser_score = self.teamTwoScore
                self.gameOver = True
            elif self.teamTwoScore == 15:
                self.winner = self.teamTwo.tournamentTeam
                self.loser = self.teamOne.tournamentTeam
                self.game.winner_score = self.teamTwoScore
                self.game.loser_score = self.teamOneScore
                self.gameOver = True
            else:
                self.setup_next_point()
        print('game is over')

    def calculate_difference_in_teams_overall_rating(self):
        if self.teamOne.team.overall_rating > self.teamTwo.team.overall_rating:
            self.betterTeam = self.teamOne
            self.differenceInTeamsOverallRating = self.teamOne.team.overall_rating - self.teamTwo.team.overall_rating
        else:
            self.betterTeam = self.teamTwo
            self.differenceInTeamsOverallRating = self.teamTwo.team.overall_rating - self.teamOne.team.overall_rating

    def calculate_probability_for_winner(self):
        self.probabilityForWinner = self.differenceInTeamsOverallRating + 50

    def setup_next_point(self):
        if self.teamOneScore == 0 and self.teamOneScore == 0:
            self.setup_first_point_of_first_half()
        if self.teamOneScore == 8 and self.teamTwoScore < 8:
            self.setup_first_point_of_second_half()
        elif self.teamOneScore < 8 and self.teamTwoScore == 8:
            self.setup_first_point_of_second_half()
        else:
            self.firstPointOfFirstHalf = False
            self.firstPointOfSecondHalf = False
            if self.pointWinner == self.teamOne:
                self.teamOne.startPointWithDisc = False
                self.teamTwo.startPointWithDisc = True
                self.discLocationY = 70
            elif self.pointWinner == self.teamTwo:
                self.teamOne.startPointWithDisc = True
                self.teamTwo.startPointWithDisc = False
                self.discLocationY = 0

    def setup_first_point_of_first_half(self):
        coinFlip = self.coin_flip()
        self.firstPointOfFirstHalf = True
        if coinFlip == 1:
            self.teamOne.startPointWithDisc = True
            self.teamOne.startFirstHalfWithDisc = True
            self.teamOne.startSecondHalfWithDisc = False
            self.teamTwo.startFirstHalfWithDisc = False
            self.teamTwo.startSecondHalfWithDisc = True
            self.teamTwo.startPointWithDisc = False
        else:
            self.teamOne.startPointWithDisc = False
            self.teamOne.startGameWithDisc = False
            self.teamTwo.startPointWithDisc = True
            self.teamTwo.startGameWithDisc = True
        self.firstPointOfFirstHalf = True
        self.firstPointOfSecondHalf = False

    def setup_first_point_of_second_half(self):
        self.firstPointOfSecondHalf = True
        if self.teamOne.startSecondHalfWithDisc:
            self.teamOne.startPointWithDisc = True
            self.teamTwo.startPointWithDisc = False
        elif self.teamTwo.startSecondHalfWithDisc:
            self.teamOne.startPointWithDisc = False
            self.teamTwo.startPointWithDisc = True
