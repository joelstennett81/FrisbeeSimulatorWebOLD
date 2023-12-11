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
        self.score = 0
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
        self.playDirectionCoinFlipResult = None
        self.startWithDiscCoinFlipResult = None
        self.game = game
        self.teamOne = TeamInGameSimulation(self.game.team_one)
        self.teamTwo = TeamInGameSimulation(self.game.team_two)
        self.sevenOnFieldForTeamOne = self.teamOne.team.o_line_players
        self.sevenOnFieldForTeamTwo = self.teamTwo.team.d_line_players
        self.determiner = 0
        self.discLocationY = 0
        self.betterTeam = 0
        self.differenceInTeamsOverallRating = 0
        self.probabilityForWinner = 0
        self.winner = self.teamOne.tournamentTeam
        self.loser = self.teamTwo.tournamentTeam
        self.pointWinner = self.teamOne
        self.gameOver = False
        self.teamWithDiscToStartFirstHalf = None
        self.teamWithDiscToStartSecondHalf = None
        self.pointSimulation = PointSimulation(self)
        self.simulationType = 'player_rating'
        self.coinFlipResult = 0
        self.isFirstHalf = True
        self.isSecondHalf = False
        self.firstHalfPointsPlayed = 0
        self.secondHalfPointsPlayed = 0
        self.firstPointOfGamePlayDirection = 0
        self.playDirection = 0

    def coin_flip(self):
        self.teamOne.coinFlipChoice = 1
        self.teamTwo.coinFlipChoice = 2
        self.startWithDiscCoinFlipResult = random.randint(1, 2)
        teamOneChoice = random.randint(1, 2)
        if teamOneChoice == self.startWithDiscCoinFlipResult:
            # team one won flip, receives disc to start
            self.teamWithDiscToStartFirstHalf = self.teamOne
            self.teamWithDiscToStartSecondHalf = self.teamTwo
        else:
            # team two won flip
            self.teamWithDiscToStartFirstHalf = self.teamTwo
            self.teamWithDiscToStartSecondHalf = self.teamOne
        teamTwoChoice = random.randint(1, 2)
        self.playDirectionCoinFlipResult = random.randint(1, 2)
        if self.playDirectionCoinFlipResult == 1:
            self.pointSimulation.playDirection = 1
        else:
            self.pointSimulation.playDirection = -1
        self.firstPointOfGamePlayDirection = self.pointSimulation.playDirection

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
            print('team 1: ', self.teamOne.score)
            print('team 2: ', self.teamTwo.score)
            if self.teamOne.score == 15:
                self.winner = self.teamOne.tournamentTeam
                self.loser = self.teamTwo.tournamentTeam
                self.game.winner_score = self.teamOne.score
                self.game.loser_score = self.teamTwo.score
                self.gameOver = True
            elif self.teamTwo.score == 15:
                self.winner = self.teamTwo.tournamentTeam
                self.loser = self.teamOne.tournamentTeam
                self.game.winner_score = self.teamTwo.score
                self.game.loser_score = self.teamOne.score
                self.gameOver = True
            else:
                self.setup_next_point()

    def setup_next_point(self):
        if self.teamOne.score == 8 and self.teamTwo.score < 8:
            if self.isFirstHalf:
                self.setup_first_point_of_second_half()
                return
        elif self.teamOne.score < 8 and self.teamTwo.score == 8:
            if self.isFirstHalf:
                self.setup_first_point_of_second_half()
                return
        if self.pointWinner == self.teamOne:
            self.teamOne.startPointWithDisc = False
            self.teamTwo.startPointWithDisc = True
        elif self.pointWinner == self.teamTwo:
            self.teamOne.startPointWithDisc = True
            self.teamTwo.startPointWithDisc = False
        self.pointSimulation.flip_play_direction()

    def setup_first_point_of_first_half(self):
        self.isFirstHalf = True
        self.isSecondHalf = False
        self.isStartOfFirstHalf = True
        self.isStartOfSecondHalf = False
        self.teamWithDiscToStartFirstHalf.startPointWithDisc = True
        self.teamWithDiscToStartFirstHalf.startFirstHalfWithDisc = True
        self.teamWithDiscToStartFirstHalf.startSecondHalfWithDisc = False
        self.teamWithDiscToStartFirstHalf.hasDisc = True
        self.teamWithDiscToStartSecondHalf.startFirstHalfWithDisc = False
        self.teamWithDiscToStartSecondHalf.startSecondHalfWithDisc = True
        self.teamWithDiscToStartSecondHalf.startPointWithDisc = False
        self.teamWithDiscToStartSecondHalf.hasDisc = False
        if self.firstPointOfGamePlayDirection == 1:
            # pull will go 70 -> 0, then play will go 0->70
            self.pointSimulation.playDirection = 1
            self.pointSimulation.discPrePullLocation = 70
            self.pointSimulation.discCurrentLocation = 70
            self.pointSimulation.discPostGoalLocation = 70
        else:
            # pull will go 0 -> 70, then play will go 70->0
            self.pointSimulation.playDirection = -1
            self.pointSimulation.discPrePullLocation = 0
            self.pointSimulation.discCurrentLocation = 0
            self.pointSimulation.discPostGoalLocation = 0

    def setup_first_point_of_second_half(self):
        self.isFirstHalf = False
        self.isSecondHalf = True
        self.isStartOfFirstHalf = False
        self.isStartOfSecondHalf = True
        self.teamWithDiscToStartSecondHalf.startPointWithDisc = True
        self.teamWithDiscToStartFirstHalf.startPointWithDisc = False
        if self.firstPointOfGamePlayDirection == 1:
            # pull will go 70 -> 0, then play will go 0->70
            self.pointSimulation.playDirection = 1
            self.pointSimulation.discPrePullLocation = 70
            self.pointSimulation.discCurrentLocation = 70
            self.pointSimulation.discPostGoalLocation = 70
        else:
            # pull will go 0 -> 70, then play will go 70->0
            self.pointSimulation.playDirection = -1
            self.pointSimulation.discPrePullLocation = 0
            self.pointSimulation.discCurrentLocation = 0
            self.pointSimulation.discPostGoalLocation = 0
