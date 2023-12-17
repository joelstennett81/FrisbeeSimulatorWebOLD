from itertools import chain
from django.db.models import Sum
from django.shortcuts import render

from frisbee_simulator_web.models import PlayerTournamentStat, TournamentTeam, TournamentPool, Game, TournamentBracket, \
    PlayerGameStat, Tournament
from frisbee_simulator_web.views.simulate_game_functions import GameSimulation


# class TeamInTournamentSimulation:
#     def __init__(self, tournamentTeam, tournament):
#         super().__init__()
#         self.tournamentTeam = tournamentTeam
#         self.team = tournamentTeam.team
#         self.tournament = tournament
#         self.coinFlipChoice = None
#         self.startPointWithDisc = None
#         self.startFirstHalfWithDisc = None
#         self.startSecondHalfWithDisc = None
#         self.score = 0
#         self.oLineH1 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.o_line_players.all()[0])
#         self.oLineH2 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.o_line_players.all()[1])
#         self.oLineH3 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.o_line_players.all()[2])
#         self.oLineC1 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.o_line_players.all()[3])
#         self.oLineC2 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.o_line_players.all()[4])
#         self.oLineC3 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.o_line_players.all()[5])
#         self.oLineC4 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.o_line_players.all()[6])
#         self.dLineH1 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.d_line_players.all()[0])
#         self.dLineH2 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.d_line_players.all()[1])
#         self.dLineH3 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.d_line_players.all()[2])
#         self.dLineC1 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.d_line_players.all()[3])
#         self.dLineC2 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.d_line_players.all()[4])
#         self.dLineC3 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.d_line_players.all()[5])
#         self.dLineC4 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.d_line_players.all()[6])
#         self.benchH1 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.bench_players.all()[0])
#         self.benchH2 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.bench_players.all()[1])
#         self.benchH3 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.bench_players.all()[2])
#         self.benchC1 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.bench_players.all()[3])
#         self.benchC2 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.bench_players.all()[4])
#         self.benchC3 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.bench_players.all()[5])
#         self.benchC4 = PlayerInTournamentSimulation(self.team, self.tournament, self.team.bench_players.all()[6])
#         self.oLinePlayers = [self.oLineH1, self.oLineH2, self.oLineH3, self.oLineC1, self.oLineC2, self.oLineC3,
#                              self.oLineC4]
#         self.dLinePlayers = [self.dLineH1, self.dLineH2, self.dLineH3, self.dLineC1, self.dLineC2, self.dLineC3,
#                              self.dLineC4]
#         self.benchPlayers = [self.benchH1, self.benchH2, self.benchH3, self.benchC1, self.benchC2, self.benchC3,
#                              self.benchC4]
#         self.allPlayers = [self.oLineH1, self.oLineH2, self.oLineH3, self.oLineC1, self.oLineC2, self.oLineC3,
#                            self.oLineC4, self.dLineH1, self.dLineH2, self.dLineH3, self.dLineC1, self.dLineC2,
#                            self.dLineC3, self.dLineC4, self.benchH1, self.benchH2, self.benchH3, self.benchC1,
#                            self.benchC2, self.benchC3, self.benchC4]
#         self.sevenOnField = None
#         self.hasDisc = None
#         self.poolPlayWins = 0
#         self.poolPlayLosses = 0
#         self.poolPlayPointDifferential = 0
#         self.poolPlayFinishPlacement = None
#
#     def __str__(self):
#         return self.team.location + ' ' + self.team.mascot
#
#
# class PlayerInTournamentSimulation:
#     def __init__(self, team, tournament, player):
#         super().__init__()
#         self.team = team
#         self.tournament = tournament
#         self.player = player
#         self.onOffense = None
#         self.onDefense = None
#         self.hasDisc = False
#         self.playerGuarding = None
#         self.guardingDisc = None
#         self.guardingPlayerBeingThrownTo = None
#         self.tournamentStats = PlayerStatsInTournamentSimulation(tournament=self.tournament, player=self.player)
#         self.points = []
#         self.allPointStats = []
#
#     def __str__(self):
#         return self.player.first_name + ' ' + self.player.last_name
#
#
# class PoolInTournamentSimulation:
#     def __init__(self, tournament, teamInTournamentSimulationOne, teamInTournamentSimulationTwo,
#                  teamInTournamentSimulationThree,
#                  teamInTournamentSimulationFour):
#         self.teamInTournamentSimulationOne = teamInTournamentSimulationOne
#         self.teamInTournamentSimulationTwo = teamInTournamentSimulationTwo
#         self.teamInTournamentSimulationThree = teamInTournamentSimulationThree
#         self.teamInTournamentSimulationFour = teamInTournamentSimulationFour
#         self.tournament = tournament
#         self.first_place_finisher = None
#         self.second_place_finisher = None
#         self.third_place_finisher = None
#         self.fourth_place_finisher = None
#         self.gameInTournamentSimulationOne = GameInTournamentSimulation(self.teamInTournamentSimulationOne,
#                                                                         self.teamInTournamentSimulationTwo, tournament)
#         self.gameInTournamentSimulationTwo = GameInTournamentSimulation(self.teamInTournamentSimulationOne,
#                                                                         self.teamInTournamentSimulationThree,
#                                                                         tournament)
#         self.gameInTournamentSimulationThree = GameInTournamentSimulation(self.teamInTournamentSimulationOne,
#                                                                           self.teamInTournamentSimulationFour,
#                                                                           tournament)
#         self.gameInTournamentSimulationFour = GameInTournamentSimulation(self.teamInTournamentSimulationTwo,
#                                                                          self.teamInTournamentSimulationThree,
#                                                                          tournament)
#         self.gameInTournamentSimulationFive = GameInTournamentSimulation(self.teamInTournamentSimulationTwo,
#                                                                          self.teamInTournamentSimulationFour,
#                                                                          tournament)
#         self.gameInTournamentSimulationSix = GameInTournamentSimulation(self.teamInTournamentSimulationThree,
#                                                                         self.teamInTournamentSimulationFour, tournament)
#
#
# class GameInTournamentSimulation:
#     def __init__(self, game, teamInTournamentSimulationOne, teamInTournamentSimulationTwo, tournament):
#         super().__init__()
#         self.game = game
#         self.tournament = tournament
#         self.teamInTournamentSimulationOne = teamInTournamentSimulationOne
#         self.teamInTournamentSimulationTwo = teamInTournamentSimulationTwo
#         self.winner = None
#         self.loser = None
#
#
# class PlayerStatsInTournamentSimulation:
#     def __init__(self, tournament, player):
#         super().__init__()
#         self.tournament = tournament
#         self.player = player
#         self.goals = 0
#         self.assists = 0
#         self.swingPassesThrown = 0
#         self.swingPassesCompleted = 0
#         self.underPassesThrown = 0
#         self.underPassesCompleted = 0
#         self.shortHucksThrown = 0
#         self.shortHucksCompleted = 0
#         self.deepHucksThrown = 0
#         self.deepHucksCompleted = 0
#         self.throwingYards = 0
#         self.receivingYards = 0
#         self.turnoversForced = 0
#         self.throwaways = 0
#         self.drops = 0
#         self.callahans = 0
#         self.pulls = 0


class TournamentSimulation:
    def __init__(self, tournament):
        super().__init__()
        self.teamInGameSimulationTwo = None
        self.teamInGameSimulationOne = None
        self.tournamentTeamPlayingTwo = None
        self.tournamentTeamPlayingOne = None
        self.gameSimulationsList = []
        self.gameSimulation = None
        self.tournament = tournament
        self.gameSimulation = None
        self.champion = None
        self.numberOfTeams = self.tournament.number_of_teams
        self.tournament_teams = TournamentTeam.objects.filter(tournament=self.tournament)
        self.teamInTournamentSimulationOne = None
        self.teamInTournamentSimulationTwo = None
        self.teamInTournamentSimulationThree = None
        self.teamInTournamentSimulationFour = None
        self.teamInTournamentSimulationFive = None
        self.teamInTournamentSimulationSix = None
        self.teamInTournamentSimulationSeven = None
        self.teamInTournamentSimulationEight = None
        self.poolOne = None
        self.poolTwo = None
        self.gameBeingPlayed = None
        self.gameInTournamentSimulation = None

    def rank_teams_for_pool_play(self):
        teams = list(self.tournament.teams.all())
        teams.sort(key=lambda team: (-team.overall_rating, team.location))
        for i, team in enumerate(teams):
            pool_play_seed = i = 1
            tournament_team = TournamentTeam.objects.create(team=team, tournament=self.tournament,
                                                            pool_play_seed=pool_play_seed,
                                                            bracket_play_seed=pool_play_seed, pool_play_wins=0)
            tournament_team.save()

    def simulate_four_team_pool(self):
        tournament_teams = TournamentTeam.objects.filter(tournament=self.tournament)
        pool = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=4)
        pool.teams.set(tournament_teams)
        pool.save()
        teams_in_pool = pool.teams.all()
        game_one = Game(team_one=teams_in_pool[0], team_two=teams_in_pool[1],
                        tournament=self.tournament,
                        game_type='Pool Play')
        game_two = Game(team_one=teams_in_pool[0], team_two=teams_in_pool[2],
                        tournament=self.tournament,
                        game_type='Pool Play')
        game_three = Game(team_one=teams_in_pool[0], team_two=teams_in_pool[3],
                          tournament=self.tournament,
                          game_type='Pool Play')
        game_four = Game(team_one=teams_in_pool[1], team_two=teams_in_pool[2],
                         tournament=self.tournament,
                         game_type='Pool Play')
        game_five = Game(team_one=teams_in_pool[1], team_two=teams_in_pool[3],
                         tournament=self.tournament,
                         game_type='Pool Play')
        game_six = Game(team_one=teams_in_pool[2], team_two=teams_in_pool[3],
                        tournament=self.tournament,
                        game_type='Pool Play')
        self.simulate_pool_play_game(game_one)
        self.simulate_pool_play_game(game_two)
        self.simulate_pool_play_game(game_three)
        self.simulate_pool_play_game(game_four)
        self.simulate_pool_play_game(game_five)
        self.simulate_pool_play_game(game_six)

    def simulate_eight_team_pool(self):
        tournament_teams = TournamentTeam.objects.filter(tournament=self.tournament)
        poolOne = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=4)
        poolTwo = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=4)
        for tournament_team in tournament_teams:
            if tournament_team.pool_play_seed in [1, 4, 5, 8]:
                poolOne.teams.add(tournament_team.team)
            else:
                poolTwo.teams.add(tournament_team.team)
        poolOne.save()
        poolTwo.save()
        for i in range(3):  # 3 rounds for 4 teams each
            for j in range(2):  # 2 matches per round
                game1 = Game(home_team=poolOne.teams.all()[j], away_team=poolOne.teams.all()[3 - j],
                             tournament=self.tournament, game_type='Pool Play')
                game2 = Game(home_team=poolTwo.teams.all()[j], away_team=poolTwo.teams.all()[3 - j],
                             tournament=self.tournament, game_type='Pool Play')
                game1.save()
                game2.save()
                self.simulate_pool_play_game(game1)
                self.simulate_pool_play_game(game2)
                game1.save()
                game2.save()

    def simulate_pool_play_game(self, game):
        gameSimulation = GameSimulation(self.tournament, game)
        gameSimulation.coin_flip()
        gameSimulation.simulationType = game.tournament.simulation_type
        gameSimulation.simulate_full_game()
        self.gameSimulationsList.append(gameSimulation)
        if gameSimulation.winner == gameSimulation.teamInGameSimulationOne:
            game.winner = gameSimulation.teamInGameSimulationOne.tournamentTeam
            game.loser = gameSimulation.teamInGameSimulationTwo.tournamentTeam
            point_differential = gameSimulation.teamInGameSimulationOne.score - gameSimulation.teamInGameSimulationTwo.score
        else:
            game.winner = gameSimulation.teamInGameSimulationTwo.tournamentTeam
            game.loser = gameSimulation.teamInGameSimulationOne.tournamentTeam
            point_differential = gameSimulation.teamInGameSimulationTwo.score - gameSimulation.teamInGameSimulationOne.score
        game.save()
        game.winner.pool_play_wins += 1
        game.loser.pool_play_losses += 1
        game.loser.pool_play_point_differential = point_differential
        game.loser.pool_play_point_differential = point_differential * (-1)
        game.save()
        return game

    def simulate_bracket_game(self, game):
        gameSimulation = GameSimulation(self.tournament, game)
        gameSimulation.coin_flip()
        gameSimulation.simulate_full_game()
        self.gameSimulationsList.append(gameSimulation)
        if gameSimulation.winner == gameSimulation.tournamentTeamOne:
            game.winner = gameSimulation.tournamentTeamOne
            game.loser = gameSimulation.tournamentTeamTwo
        else:
            game.winner = gameSimulation.tournamentTeamTwo
            game.loser = gameSimulation.tournamentTeamOne
        game.save()
        game.winner.bracket_play_wins += 1
        game.loser.bracket_play_losses += 1
        game.save()
        return game

    def simulate_four_team_bracket(self):
        tournament_pool = TournamentPool.objects.get(tournament=self.tournament)
        teams = tournament_pool.teams.all()
        sorted_teams = teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        tournament_bracket = TournamentBracket(tournament=self.tournament, number_of_teams=4,
                                               bracket_type='Championship')
        tournament_bracket.save()
        tournament_bracket.teams.set(sorted_teams)
        tournament_bracket.save()
        for i, team in enumerate(sorted_teams, start=1):
            team.bracket_play_seed = i
            team.save()
        teams_in_bracket = tournament_bracket.teams.all()
        game_one = Game(team_one=teams_in_bracket[0], team_two=teams_in_bracket[3],
                        tournament=tournament_bracket.tournament,
                        game_type='Semifinal')
        self.simulate_bracket_game(game_one)
        game_two = Game(team_one=teams_in_bracket[1], team_two=teams_in_bracket[2],
                        tournament=tournament_bracket.tournament,
                        game_type='Semifinal')
        self.simulate_bracket_game(game_two)
        game_three = Game(team_one=game_one.loser, team_two=game_two.loser, tournament=tournament_bracket.tournament,
                          game_type='Third-Place')
        self.simulate_bracket_game(game_three)
        game_four = Game(team_one=game_one.winner, team_two=game_two.winner, tournament=tournament_bracket.tournament,
                         game_type='Championship')
        self.simulate_bracket_game(game_four)
        tournament_bracket.champion = game_four.winner
        tournament_bracket.save()
        return tournament_bracket

    def simulate_eight_team_bracket(self):
        tournament_pools = TournamentPool.objects.filter(tournament=self.tournament)
        teams_list = list(chain.from_iterable(pool.teams.all() for pool in tournament_pools))
        sorted_teams = sorted(
            teams_list,
            key=lambda team: (team.pool_play_wins, team.pool_play_point_differential),
            reverse=True
        )
        tournament_bracket = TournamentBracket.objects.create(tournament=self.tournament, number_of_teams=8,
                                                              bracket_type='Championship')
        tournament_bracket.teams.set(sorted_teams)
        tournament_bracket.save()
        for i, team in enumerate(sorted_teams, start=1):
            team.bracket_play_seed = i
            team.save()
        teams_in_bracket = tournament_bracket.teams.all()
        game_one = Game.objects.create(team_one=teams_in_bracket[0], team_two=teams_in_bracket[7],
                                       tournament=self.tournament,
                                       game_type='Quarterfinal')
        self.tournament.simulate_bracket_game(game_one)
        game_two = Game.objects.create(team_one=teams_in_bracket[1], team_two=teams_in_bracket[6],
                                       tournament=self.tournament,
                                       game_type='Quarterfinal')
        self.tournament.simulate_bracket_game(game_two)
        game_three = Game.objects.create(team_one=teams_in_bracket[2], team_two=teams_in_bracket[5],
                                         tournament=self.tournament,
                                         game_type='Quarterfinal')
        self.tournament.simulate_bracket_game(game_three)
        game_four = Game.objects.create(team_one=teams_in_bracket[3], team_two=teams_in_bracket[4],
                                        tournament=self.tournament,
                                        game_type='Quarterfinal')
        self.simulate_bracket_game(game_four)
        # Loser's Bracket
        game_five = Game.objects.create(team_one=game_one.loser, team_two=game_two.loser, tournament=self.tournament,
                                        game_type='Loser-Semifinal')
        self.simulate_bracket_game(game_five)
        game_six = Game.objects.create(team_one=game_three.loser, team_two=game_four.loser, tournament=self.tournament,
                                       game_type='Loser-Semifinal')
        self.simulate_bracket_game(game_six)
        game_seven = Game.objects.create(team_one=game_five.winner, team_two=game_six.winner, tournament=self.tournament,
                                         game_type='Fifth-Place-Final')
        self.simulate_bracket_game(game_seven)
        game_eight = Game.objects.create(team_one=game_five.loser, team_two=game_six.loser, tournament=self.tournament,
                                         game_type='Seventh-Place-Final')
        self.simulate_bracket_game(game_eight)
        # Winner's Bracket
        game_nine = Game.objects.create(team_one=game_one.winner, team_two=game_two.winner, tournament=self.tournament,
                                        game_type='Semifinal')
        self.simulate_bracket_game(game_nine)
        game_ten = Game.objects.create(team_one=game_three.winner, team_two=game_four.winner, tournament=self.tournament,
                                       game_type='Semifinal')
        self.simulate_bracket_game(game_ten)
        game_eleven = Game.objects.create(team_one=game_nine.loser, team_two=game_ten.loser, tournament=self.tournament,
                                          game_type='Third-Place')
        self.simulate_bracket_game(game_eleven)
        game_twelve = Game.objects.create(team_one=game_nine.winner, team_two=game_ten.winner, tournament=self.tournament,
                                          game_type='Championship')
        self.simulate_bracket_game(game_twelve)
        tournament_bracket.champion = game_twelve.winner
        tournament_bracket.save()
        return tournament_bracket

    def simulate_tournament(self, request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        number_of_teams = tournament.number_of_teams
        self.rank_teams_for_pool_play()
        self.simulate_four_team_pool()
        if number_of_teams == 4:
            tournament_bracket = self.simulate_four_team_bracket()
        elif number_of_teams == 8:
            tournament_bracket = self.simulate_eight_team_bracket(tournament)
        else:
            return render(request, 'tournaments/tournament_error.html')
        tournament.champion = tournament_bracket.champion.team
        tournament.is_complete = True
        tournament.save()
        self.save_tournament_player_stats_from_game_player_stats()

    def save_tournament_player_stats_from_game_player_stats(self):
        for gameSimulation in self.gameSimulationsList:
            for gameSimulationPlayer in gameSimulation.teamInGameSimulationOne.allPlayers:
                gameStats = PlayerGameStat.objects.filter(player=gameSimulationPlayer.player,
                                                          tournament=self.tournament)
                # Update the player's game stats
                playerTournamentStat = PlayerTournamentStat.objects.create(
                    tournament=self.tournament,
                    player=gameSimulationPlayer.player,
                    goals=gameStats.aggregate(Sum('goals'))['goals__sum'],
                    assists=gameStats.aggregate(Sum('assists'))['assists__sum'],
                    swing_passes_thrown=gameStats.aggregate(Sum('swing_passes_thrown'))[
                        'swing_passes_thrown__sum'],
                    swing_passes_completed=gameStats.aggregate(Sum('swing_passes_completed'))[
                        'swing_passes_completed__sum'],
                    under_passes_thrown=gameStats.aggregate(Sum('under_passes_thrown'))['under_passes_thrown__sum'],
                    under_passes_completed=gameStats.aggregate(Sum('under_passes_completed'))[
                        'under_passes_completed__sum'],
                    short_hucks_thrown=gameStats.aggregate(Sum('short_hucks_thrown'))['short_hucks_thrown__sum'],
                    short_hucks_completed=gameStats.aggregate(Sum('short_hucks_completed'))[
                        'short_hucks_completed__sum'],
                    deep_hucks_thrown=gameStats.aggregate(Sum('deep_hucks_thrown'))['deep_hucks_thrown__sum'],
                    deep_hucks_completed=gameStats.aggregate(Sum('deep_hucks_completed'))[
                        'deep_hucks_completed__sum'],
                    throwing_yards=gameStats.aggregate(Sum('throwing_yards'))['throwing_yards__sum'],
                    receiving_yards=gameStats.aggregate(Sum('receiving_yards'))['receiving_yards__sum'],
                    turnovers_forced=gameStats.aggregate(Sum('turnovers_forced'))['turnovers_forced__sum'],
                    throwaways=gameStats.aggregate(Sum('throwaways'))['throwaways__sum'],
                    drops=gameStats.aggregate(Sum('drops'))['drops__sum'],
                    callahans=gameStats.aggregate(Sum('callahans'))['callahans__sum'],
                    pulls=gameStats.aggregate(Sum('pulls'))['pulls__sum'],
                )
                playerTournamentStat.save()
            for gameSimulationPlayer in gameSimulation.teamInGameSimulationTwo.allPlayers:
                gameStats = PlayerGameStat.objects.filter(player=gameSimulationPlayer.player,
                                                          tournament=self.tournament)
                # Update the player's game stats
                playerTournamentStat = PlayerTournamentStat.objects.create(
                    tournament=self.tournament,
                    player=gameSimulationPlayer.player,
                    goals=gameStats.aggregate(Sum('goals'))['goals__sum'],
                    assists=gameStats.aggregate(Sum('assists'))['assists__sum'],
                    swing_passes_thrown=gameStats.aggregate(Sum('swing_passes_thrown'))[
                        'swing_passes_thrown__sum'],
                    swing_passes_completed=gameStats.aggregate(Sum('swing_passes_completed'))[
                        'swing_passes_completed__sum'],
                    under_passes_thrown=gameStats.aggregate(Sum('under_passes_thrown'))['under_passes_thrown__sum'],
                    under_passes_completed=gameStats.aggregate(Sum('under_passes_completed'))[
                        'under_passes_completed__sum'],
                    short_hucks_thrown=gameStats.aggregate(Sum('short_hucks_thrown'))['short_hucks_thrown__sum'],
                    short_hucks_completed=gameStats.aggregate(Sum('short_hucks_completed'))[
                        'short_hucks_completed__sum'],
                    deep_hucks_thrown=gameStats.aggregate(Sum('deep_hucks_thrown'))['deep_hucks_thrown__sum'],
                    deep_hucks_completed=gameStats.aggregate(Sum('deep_hucks_completed'))[
                        'deep_hucks_completed__sum'],
                    throwing_yards=gameStats.aggregate(Sum('throwing_yards'))['throwing_yards__sum'],
                    receiving_yards=gameStats.aggregate(Sum('receiving_yards'))['receiving_yards__sum'],
                    turnovers_forced=gameStats.aggregate(Sum('turnovers_forced'))['turnovers_forced__sum'],
                    throwaways=gameStats.aggregate(Sum('throwaways'))['throwaways__sum'],
                    drops=gameStats.aggregate(Sum('drops'))['drops__sum'],
                    callahans=gameStats.aggregate(Sum('callahans'))['callahans__sum'],
                    pulls=gameStats.aggregate(Sum('pulls'))['pulls__sum'],
                )
                playerTournamentStat.save()
