import random

from frisbee_simulator_web.models import TournamentTeam, Game, Team
from frisbee_simulator_web.views.simulate_point_functions import PointSimulation, PlayerInPointSimulation


class TeamInGameSimulation:
    def __init__(self, tournamentTeam):
        super().__init__()
        self.tournamentTeam = tournamentTeam
        self.team = tournamentTeam.team
        self.coinFlipChoice = None
        self.startPointWithDisc = None
        self.startFirstHalfWithDisc = None
        self.startSecondHalfWithDisc = None
        self.oLineH1 = PlayerInPointSimulation(self.team.o_line_players.all()[0]).player
        self.oLineH2 = PlayerInPointSimulation(self.team.o_line_players.all()[1]).player
        self.oLineH3 = PlayerInPointSimulation(self.team.o_line_players.all()[2]).player
        self.oLineC1 = PlayerInPointSimulation(self.team.o_line_players.all()[3]).player
        self.oLineC2 = PlayerInPointSimulation(self.team.o_line_players.all()[4]).player
        self.oLineC3 = PlayerInPointSimulation(self.team.o_line_players.all()[5]).player
        self.oLineC4 = PlayerInPointSimulation(self.team.o_line_players.all()[6]).player
        self.dLineH1 = PlayerInPointSimulation(self.team.d_line_players.all()[0]).player
        self.dLineH2 = PlayerInPointSimulation(self.team.d_line_players.all()[1]).player
        self.dLineH3 = PlayerInPointSimulation(self.team.d_line_players.all()[2]).player
        self.dLineC1 = PlayerInPointSimulation(self.team.d_line_players.all()[3]).player
        self.dLineC2 = PlayerInPointSimulation(self.team.d_line_players.all()[4]).player
        self.dLineC3 = PlayerInPointSimulation(self.team.d_line_players.all()[5]).player
        self.dLineC4 = PlayerInPointSimulation(self.team.d_line_players.all()[6]).player
        self.benchH1 = PlayerInPointSimulation(self.team.bench_players.all()[0]).player
        self.benchH2 = PlayerInPointSimulation(self.team.bench_players.all()[1]).player
        self.benchH3 = PlayerInPointSimulation(self.team.bench_players.all()[2]).player
        self.benchC1 = PlayerInPointSimulation(self.team.bench_players.all()[3]).player
        self.benchC2 = PlayerInPointSimulation(self.team.bench_players.all()[4]).player
        self.benchC3 = PlayerInPointSimulation(self.team.bench_players.all()[5]).player
        self.benchC4 = PlayerInPointSimulation(self.team.bench_players.all()[6]).player
        self.oLinePlayers = [self.oLineH1, self.oLineH2, self.oLineH3, self.oLineC1, self.oLineC2, self.oLineC3,
                             self.oLineC4]
        self.dLinePlayers = [self.dLineH1, self.dLineH2, self.dLineH3, self.dLineC1, self.dLineC2, self.dLineC3,
                             self.dLineC4]
        self.benchPlayers = [self.benchH1, self.benchH2, self.benchH3, self.benchC1, self.benchC2, self.benchC3,
                             self.benchC4]
        self.sevenOnField = None
        self.hasDisc = None


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
        self.startsFirstHalfWithDisc = None
        self.startsSecondHalfWithDisc = None
        self.pointSimulation = PointSimulation(self)
        self.simulationType = 'player_rating'
        self.coinFlipResult = 0
        self.isFirstHalf = True
        self.isSecondHalf = False
        self.firstHalfPointsPlayed = 0
        self.secondHalfPointsPlayed = 0

    def coin_flip(self):
        self.teamOne.coinFlipChoice = 1
        self.teamTwo.coinFlipChoice = 2
        coinFlip = random.randint(1, 2)
        self.coinFlipResult = coinFlip

    def simulate_point(self):
        self.pointSimulation = PointSimulation(self)
        self.pointSimulation.simulate_point()
        self.pointWinner = self.pointSimulation.pointWinner

    def simulate_full_game(self):
        self.setup_first_point_of_first_half()
        self.isFirstHalf = True
        self.isSecondHalf = False
        while not self.gameOver:
            print('game isnt over, about to simulate point')
            self.simulate_point()
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

    def setup_next_point(self):
        if self.teamOneScore == 8 and self.teamTwoScore < 8:
            if self.isFirstHalf:
                self.setup_first_point_of_second_half()
                return
        elif self.teamOneScore < 8 and self.teamTwoScore == 8:
            if self.isFirstHalf:
                self.setup_first_point_of_second_half()
                return
        if self.pointWinner == self.teamOne:
            self.teamOne.startPointWithDisc = False
            self.teamTwo.startPointWithDisc = True
            self.discLocationY = 70
        elif self.pointWinner == self.teamTwo:
            self.teamOne.startPointWithDisc = True
            self.teamTwo.startPointWithDisc = False
            self.discLocationY = 0

    def setup_first_point_of_first_half(self):
        self.isFirstHalf = True
        self.isSecondHalf = False
        if self.coinFlipResult == 1:
            self.teamOne.startPointWithDisc = True
            self.teamOne.startFirstHalfWithDisc = True
            self.teamOne.startSecondHalfWithDisc = False
            self.teamOne.hasDisc = True
            self.teamTwo.startFirstHalfWithDisc = False
            self.teamTwo.startSecondHalfWithDisc = True
            self.teamTwo.startPointWithDisc = False
            self.teamTwo.hasDisc = False
        else:
            self.teamOne.startPointWithDisc = False
            self.teamOne.startFirstHalfWithDisc = False
            self.teamOne.startSecondHalfWithDisc = True
            self.teamOne.hasDisc = False
            self.teamTwo.startFirstHalfWithDisc = True
            self.teamTwo.startSecondHalfWithDisc = False
            self.teamTwo.startPointWithDisc = True
            self.teamTwo.hasDisc = True

    def setup_first_point_of_second_half(self):
        self.isFirstHalf = False
        self.isSecondHalf = True
        if self.teamOne.startSecondHalfWithDisc:
            self.teamOne.startPointWithDisc = True
            self.teamTwo.startPointWithDisc = False
        elif self.teamTwo.startSecondHalfWithDisc:
            self.teamOne.startPointWithDisc = False
            self.teamTwo.startPointWithDisc = True
