import random
import threading
from itertools import chain, count
from django.db.models import Sum, F, Prefetch
from django.shortcuts import render

from frisbee_simulator_web.models import PlayerTournamentStat, TournamentTeam, TournamentPool, Game, TournamentBracket, \
    PlayerGameStat, Tournament
from frisbee_simulator_web.views.simulate_game_functions import GameSimulation


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
        self.tourneyPrintStatements = {}
        self.poolPlayGamesDoneSimulating = 0
        self.poolPlayTotalGamesCount = 0
        self.semifinalGamesDoneSimulating = 0
        self.semifinalTotalGamesCount = 0
        self.finalRoundGamesDoneSimulating = 0
        self.finalRoundTotalGamesCount = 0

    def rank_teams_for_pool_play(self):
        teams = list(self.tournament.teams.all())
        teams.sort(key=lambda team: (-team.overall_rating, team.location))
        for i, team in enumerate(teams):
            pool_play_seed = i = 1
            tournament_team = TournamentTeam.objects.create(team=team, tournament=self.tournament,
                                                            pool_play_seed=pool_play_seed,
                                                            bracket_play_seed=pool_play_seed, pool_play_wins=0)
            tournament_team.save()

    def setup_manual_pool_play_games_for_simulation(self):
        self.rank_teams_for_pool_play()
        tournament_teams = list(TournamentTeam.objects.filter(tournament=self.tournament))
        num_teams = len(tournament_teams)
        games = []
        # Check the number of teams and create games accordingly
        if num_teams == 4:
            pool = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=len(tournament_teams),
                                                 name='Pool A')
            pool.teams.set(tournament_teams)
            pool.save()
            # Round  1
            games.extend([
                Game.objects.create(team_one=tournament_teams[0], team_two=tournament_teams[1],
                                    tournament=self.tournament, game_type='Pool Play'),
                Game.objects.create(team_one=tournament_teams[2], team_two=tournament_teams[3],
                                    tournament=self.tournament, game_type='Pool Play')
            ])
            # Round  2
            games.extend([
                Game.objects.create(team_one=tournament_teams[0], team_two=tournament_teams[2],
                                    tournament=self.tournament, game_type='Pool Play'),
                Game.objects.create(team_one=tournament_teams[1], team_two=tournament_teams[3],
                                    tournament=self.tournament, game_type='Pool Play')
            ])
            # Round  3
            games.extend([
                Game.objects.create(team_one=tournament_teams[0], team_two=tournament_teams[3],
                                    tournament=self.tournament, game_type='Pool Play'),
                Game.objects.create(team_one=tournament_teams[1], team_two=tournament_teams[2],
                                    tournament=self.tournament, game_type='Pool Play')
            ])
        elif num_teams == 8:
            poolATeams = tournament_teams[:4]
            poolBTeams = tournament_teams[4:]
            poolA = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=len(poolATeams),
                                                  name='Pool A')
            poolB = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=len(poolBTeams),
                                                  name='Pool B')
            poolA.teams.set(poolATeams)
            poolA.save()
            poolB.teams.set(poolBTeams)
            poolB.save()
            # Pool A games
            games.extend([
                # Round  1
                Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[1], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolATeams[2], team_two=poolATeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  2
                Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[2], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  3
                Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[2], tournament=self.tournament,
                                    game_type='Pool Play')
            ])
            # Pool B games
            games.extend([
                # Round  1
                Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[1], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolBTeams[2], team_two=poolBTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  2
                Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[2], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  3
                Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[2], tournament=self.tournament,
                                    game_type='Pool Play')
            ])
        elif num_teams == 16:
            poolATeams = tournament_teams[:4]
            poolBTeams = tournament_teams[4:8]
            poolCTeams = tournament_teams[8:12]
            poolDTeams = tournament_teams[12:]
            poolA = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=len(poolATeams),
                                                  name='Pool A')
            poolB = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=len(poolBTeams),
                                                  name='Pool B')
            poolC = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=len(poolCTeams),
                                                  name='Pool C')
            poolD = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=len(poolDTeams),
                                                  name='Pool D')
            poolA.teams.set(poolATeams)
            poolA.save()
            poolB.teams.set(poolBTeams)
            poolB.save()
            poolC.teams.set(poolCTeams)
            poolD.save()
            poolD.teams.set(poolDTeams)
            poolD.save()
            # Pool A games
            games.extend([
                # Round  1
                Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[1], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolATeams[2], team_two=poolATeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  2
                Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[2], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  3
                Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[2], tournament=self.tournament,
                                    game_type='Pool Play')
            ])
            # Pool B games
            games.extend([
                # Round  1
                Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[1], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolBTeams[2], team_two=poolBTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  2
                Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[2], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  3
                Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[2], tournament=self.tournament,
                                    game_type='Pool Play')
            ])
            games.extend([
                # Round  1
                Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[1], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolCTeams[2], team_two=poolCTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  2
                Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[2], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolCTeams[1], team_two=poolCTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  3
                Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolCTeams[1], team_two=poolCTeams[2], tournament=self.tournament,
                                    game_type='Pool Play')
            ])
            games.extend([
                # Round  1
                Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[1], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolDTeams[2], team_two=poolDTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  2
                Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[2], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolDTeams[1], team_two=poolDTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                # Round  3
                Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[3], tournament=self.tournament,
                                    game_type='Pool Play'),
                Game.objects.create(team_one=poolDTeams[1], team_two=poolDTeams[2], tournament=self.tournament,
                                    game_type='Pool Play')
            ])
        self.tournament.pool_play_initialized = True
        self.tournament.pool_play_games.set(games)
        self.tournament.save()

    def setup_semifinal_round_for_four_team_bracket(self, request):
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
        created_by = request.user.profile
        game_one = Game(team_one=teams_in_bracket[0], team_two=teams_in_bracket[3],
                        tournament=tournament_bracket.tournament,
                        game_type='Semifinal', created_by=created_by)
        game_two = Game(team_one=teams_in_bracket[1], team_two=teams_in_bracket[2],
                        tournament=tournament_bracket.tournament,
                        game_type='Semifinal', created_by=created_by)
        game_one.save()
        game_two.save()
        games = [game_one, game_two]
        self.tournament.semifinal_round_initialized = True
        self.tournament.semifinal_round_games.set(games)
        self.tournament.save()

    def setup_final_round_for_four_team_bracket(self, request):
        semifinalGames = self.tournament.semifinal_round_games.all()
        semifinalGameOne = semifinalGames[0]
        semifinalGameTwo = semifinalGames[1]
        created_by = request.user.profile
        third_place_game = Game(team_one=semifinalGameOne.loser, team_two=semifinalGameTwo.loser,
                                tournament=self.tournament,
                                game_type='3rd-Place Final', created_by=created_by)
        championship_game = Game(team_one=semifinalGameOne.winner, team_two=semifinalGameTwo.winner,
                                 tournament=self.tournament,
                                 game_type='Championship', created_by=created_by)
        third_place_game.save()
        championship_game.save()
        games = [third_place_game, championship_game]
        self.tournament.final_round_initialized = True
        self.tournament.final_round_games.set(games)
        self.tournament.save()

    def setup_quarterfinal_round_for_8_team_bracket(self, request):
        poolA = TournamentPool.objects.get(tournament=self.tournament, name='Pool A')
        poolB = TournamentPool.objects.get(tournament=self.tournament, name='Pool B')
        poolASortedTeams = poolA.teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        poolBSortedTeams = poolB.teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        # poolA1 v pool B4, pool B2vA3, pool B1vA4, pool A2vB3
        teamsInBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolASortedTeams[1], poolBSortedTeams[1],
                          poolASortedTeams[2], poolBSortedTeams[2], poolASortedTeams[3], poolBSortedTeams[3]]
        tournament_bracket = TournamentBracket.objects.create(tournament=self.tournament, number_of_teams=8,
                                                              bracket_type='Championship')
        tournament_bracket.teams.set(teamsInBracket)
        tournament_bracket.save()
        for i, team in enumerate(teamsInBracket, start=1):
            team.bracket_play_seed = i
            team.save()
        teams_in_bracket = tournament_bracket.teams.all()
        created_by = request.user.profile
        game_one = Game(team_one=teams_in_bracket[0], team_two=teams_in_bracket[7],
                        tournament=tournament_bracket.tournament,
                        game_type='Quarterfinal', created_by=created_by)
        game_two = Game(team_one=teams_in_bracket[1], team_two=teams_in_bracket[6],
                        tournament=tournament_bracket.tournament,
                        game_type='Quarterfinal', created_by=created_by)
        game_three = Game(team_one=teams_in_bracket[2], team_two=teams_in_bracket[5],
                          tournament=tournament_bracket.tournament,
                          game_type='Quarterfinal', created_by=created_by)
        game_four = Game(team_one=teams_in_bracket[3], team_two=teams_in_bracket[4],
                         tournament=tournament_bracket.tournament,
                         game_type='Quarterfinal', created_by=created_by)
        game_one.save()
        game_two.save()
        game_three.save()
        game_four.save()
        games = [game_one, game_two, game_three, game_four]
        self.tournament.quarterfinal_round_initialized = True
        self.tournament.quarterfinal_round_games.set(games)
        self.tournament.save()

    def setup_semifinal_round_for_eight_team_bracket(self, request):
        quarterFinalGames = self.tournament.quarterfinal_round_games.all()
        quarterFinalGameOne = quarterFinalGames[0]
        quarterFinalGameTwo = quarterFinalGames[1]
        quarterFinalGameThree = quarterFinalGames[2]
        quarterFinalGameFour = quarterFinalGames[3]
        created_by = request.user.profile
        semiFinalGameOne = Game(team_one=quarterFinalGameOne.winner, team_two=quarterFinalGameTwo.winner,
                                tournament=self.tournament,
                                game_type='Semifinal', created_by=created_by)
        semiFinalGameTwo = Game(team_one=quarterFinalGameThree.winner, team_two=quarterFinalGameFour.winner,
                                tournament=self.tournament,
                                game_type='Semifinal', created_by=created_by)
        loserSemiFinalGameOne = Game(team_one=quarterFinalGameOne.loser, team_two=quarterFinalGameTwo.loser,
                                     tournament=self.tournament,
                                     game_type='5th-Place Semifinal', created_by=created_by)
        loserSemiFinalGameTwo = Game(team_one=quarterFinalGameThree.loser, team_two=quarterFinalGameFour.loser,
                                     tournament=self.tournament,
                                     game_type='5th-Place Semifinal', created_by=created_by)
        semiFinalGameOne.save()
        semiFinalGameTwo.save()
        loserSemiFinalGameOne.save()
        loserSemiFinalGameTwo.save()
        games = [semiFinalGameOne, semiFinalGameTwo, loserSemiFinalGameOne, loserSemiFinalGameTwo]
        self.tournament.semifinal_round_initialized = True
        self.tournament.semifinal_round_games.set(games)
        self.tournament.save()

    def setup_final_round_for_eight_team_bracket(self, request):
        semiFinalGames = self.tournament.semifinal_round_games.all()
        semiFinalGameOne = semiFinalGames[0]
        semiFinalGameTwo = semiFinalGames[1]
        loserSemiFinalGameOne = semiFinalGames[2]
        loserSemiFinalGameTwo = semiFinalGames[3]
        created_by = request.user.profile
        championshipGame = Game(team_one=semiFinalGameOne.winner, team_two=semiFinalGameTwo.winner,
                                tournament=self.tournament,
                                game_type='Championship', created_by=created_by)
        thirdPlaceGame = Game(team_one=semiFinalGameOne.loser, team_two=semiFinalGameTwo.loser,
                              tournament=self.tournament,
                              game_type='3rd-Place Final', created_by=created_by)
        fifthPlaceGame = Game(team_one=loserSemiFinalGameOne.winner, team_two=loserSemiFinalGameTwo.winner,
                              tournament=self.tournament,
                              game_type='5th-Place Final', created_by=created_by)
        seventhPlaceGame = Game(team_one=loserSemiFinalGameOne.loser, team_two=loserSemiFinalGameTwo.loser,
                                tournament=self.tournament,
                                game_type='7th-Place Final', created_by=created_by)
        championshipGame.save()
        thirdPlaceGame.save()
        fifthPlaceGame.save()
        seventhPlaceGame.save()
        games = [championshipGame, thirdPlaceGame, fifthPlaceGame, seventhPlaceGame]
        self.tournament.final_round_initialized = True
        self.tournament.final_round_games.set(games)
        self.tournament.save()

    def setup_quarterfinal_round_for_sixteen_team_bracket(self, request):
        # set up two rounds, a winners and losers quarterfinals
        tournament_pools = TournamentPool.objects.filter(tournament=self.tournament)
        poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        poolCSortedTeams = tournament_pools[2].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        poolDSortedTeams = tournament_pools[3].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        # poolA3 v pool D4, pool A4v pool D3, pool B3vC4, pool B4vC3
        teamsInLosersBracket = [poolASortedTeams[2], poolBSortedTeams[2], poolCSortedTeams[2], poolDSortedTeams[2],
                                poolASortedTeams[3], poolBSortedTeams[3], poolCSortedTeams[3], poolDSortedTeams[3]]
        # poolA1 v pool D2, pool B1vC2, pool B2vC1, pool A2v pool D1
        teamsInWinnersBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolCSortedTeams[0], poolDSortedTeams[0],
                                 poolASortedTeams[1], poolBSortedTeams[1], poolCSortedTeams[1], poolDSortedTeams[1]]
        losersBracket = TournamentBracket.objects.create(tournament=self.tournament, number_of_teams=8,
                                                         bracket_type='Loser')
        winnersBracket = TournamentBracket.objects.create(tournament=self.tournament, number_of_teams=8,
                                                          bracket_type='Championship')
        losersBracket.teams.set(teamsInLosersBracket)
        winnersBracket.teams.set(teamsInWinnersBracket)
        losersBracket.save()
        winnersBracket.save()
        for i, team in enumerate(teamsInLosersBracket, start=1):
            team.bracket_play_seed = i
            team.save()
        for i, team in enumerate(teamsInWinnersBracket, start=1):
            team.bracket_play_seed = i
            team.save()
        created_by = request.user.profile
        loser_game_one = Game.objects.create(team_one=teamsInLosersBracket[0], team_two=teamsInLosersBracket[7],
                                             tournament=self.tournament,
                                             game_type='9th-Place Quarterfinal', created_by=created_by)
        loser_game_two = Game.objects.create(team_one=teamsInLosersBracket[1], team_two=teamsInLosersBracket[6],
                                             tournament=self.tournament,
                                             game_type='9th-Place Quarterfinal', created_by=created_by)
        loser_game_three = Game.objects.create(team_one=teamsInLosersBracket[2], team_two=teamsInLosersBracket[5],
                                               tournament=self.tournament,
                                               game_type='9th-Place Quarterfinal', created_by=created_by)
        loser_game_four = Game.objects.create(team_one=teamsInLosersBracket[3], team_two=teamsInLosersBracket[4],
                                              tournament=self.tournament,
                                              game_type='9th-Place Quarterfinal', created_by=created_by)
        winner_game_one = Game(team_one=teamsInWinnersBracket[0], team_two=teamsInWinnersBracket[7],
                               tournament=self.tournament,
                               game_type='Quarterfinal', created_by=created_by)
        winner_game_two = Game(team_one=teamsInWinnersBracket[1], team_two=teamsInWinnersBracket[6],
                               tournament=self.tournament,
                               game_type='Quarterfinal', created_by=created_by)
        winner_game_three = Game(team_one=teamsInWinnersBracket[2], team_two=teamsInWinnersBracket[5],
                                 tournament=self.tournament,
                                 game_type='Quarterfinal', created_by=created_by)
        winner_game_four = Game(team_one=teamsInWinnersBracket[3], team_two=teamsInWinnersBracket[4],
                                tournament=self.tournament,
                                game_type='Quarterfinal', created_by=created_by)
        loser_game_one.save()
        loser_game_two.save()
        loser_game_three.save()
        loser_game_four.save()
        winner_game_one.save()
        winner_game_two.save()
        winner_game_three.save()
        winner_game_four.save()
        loser_games = [loser_game_one, loser_game_two, loser_game_three, loser_game_four]
        winner_games = [winner_game_one, winner_game_two, winner_game_three, winner_game_four]
        self.tournament.losers_quarterfinal_round_initialized = True
        self.tournament.quarterfinal_round_initialized = True
        self.tournament.losers_quarterfinal_round_games.set(loser_games)
        self.tournament.quarterfinal_round_games.set(winner_games)
        self.tournament.save()

    def setup_semifinal_round_for_sixteen_team_bracket(self, request):
        winnerQuarterFinalGames = self.tournament.quarterfinal_round_games.all()
        winnerQuarterFinalGameOne = winnerQuarterFinalGames[0]
        winnerQuarterFinalGameTwo = winnerQuarterFinalGames[1]
        winnerQuarterFinalGameThree = winnerQuarterFinalGames[2]
        winnerQuarterFinalGameFour = winnerQuarterFinalGames[3]
        created_by = request.user.profile
        winnerSemiFinalGameOne = Game(team_one=winnerQuarterFinalGameOne.winner,
                                      team_two=winnerQuarterFinalGameTwo.winner,
                                      tournament=self.tournament,
                                      game_type='Semifinal', created_by=created_by)
        winnerSemiFinalGameTwo = Game(team_one=winnerQuarterFinalGameThree.winner,
                                      team_two=winnerQuarterFinalGameFour.winner,
                                      tournament=self.tournament,
                                      game_type='Semifinal', created_by=created_by)
        fifthPlaceSemiFinalGameOne = Game(team_one=winnerQuarterFinalGameOne.loser,
                                          team_two=winnerQuarterFinalGameTwo.loser,
                                          tournament=self.tournament,
                                          game_type='5th-Place Semifinal', created_by=created_by)
        fifthPlaceSemiFinalGameTwo = Game(team_one=winnerQuarterFinalGameThree.loser,
                                          team_two=winnerQuarterFinalGameFour.loser,
                                          tournament=self.tournament,
                                          game_type='5th-Place Semifinal', created_by=created_by)
        winnerSemiFinalGameOne.save()
        winnerSemiFinalGameTwo.save()
        fifthPlaceSemiFinalGameOne.save()
        fifthPlaceSemiFinalGameTwo.save()
        winnerGames = [winnerSemiFinalGameOne, winnerSemiFinalGameTwo, fifthPlaceSemiFinalGameOne,
                       fifthPlaceSemiFinalGameTwo]
        self.tournament.semifinal_round_initialized = True
        self.tournament.semifinal_round_games.set(winnerGames)
        self.tournament.save()
        loserQuarterFinalGames = self.tournament.losers_quarterfinal_round_games.all()
        loserQuarterFinalGameOne = loserQuarterFinalGames[0]
        loserQuarterFinalGameTwo = loserQuarterFinalGames[1]
        loserQuarterFinalGameThree = loserQuarterFinalGames[2]
        loserQuarterFinalGameFour = loserQuarterFinalGames[3]
        ninthPlaceSemiFinalGameOne = Game(team_one=loserQuarterFinalGameOne.winner,
                                          team_two=loserQuarterFinalGameTwo.winner,
                                          tournament=self.tournament,
                                          game_type='9th-Place Semifinal', created_by=created_by)
        ninthPlaceSemiFinalGameTwo = Game(team_one=loserQuarterFinalGameThree.winner,
                                          team_two=loserQuarterFinalGameFour.winner,
                                          tournament=self.tournament,
                                          game_type='9th-Place Semifinal', created_by=created_by)
        thirteenthPlaceSemiFinalGameOne = Game(team_one=loserQuarterFinalGameOne.loser,
                                               team_two=loserQuarterFinalGameTwo.loser,
                                               tournament=self.tournament,
                                               game_type='13th-Place Semifinal', created_by=created_by)
        thirteenthPlaceSemiFinalGameTwo = Game(team_one=loserQuarterFinalGameThree.loser,
                                               team_two=loserQuarterFinalGameFour.loser,
                                               tournament=self.tournament,
                                               game_type='13th-Place Semifinal', created_by=created_by)
        ninthPlaceSemiFinalGameOne.save()
        ninthPlaceSemiFinalGameTwo.save()
        thirteenthPlaceSemiFinalGameOne.save()
        thirteenthPlaceSemiFinalGameTwo.save()
        loserGames = [ninthPlaceSemiFinalGameOne, ninthPlaceSemiFinalGameTwo, thirteenthPlaceSemiFinalGameOne,
                      thirteenthPlaceSemiFinalGameTwo]
        self.tournament.losers_semifinal_round_initialized = True
        self.tournament.losers_semifinal_round_games.set(loserGames)
        self.tournament.save()

    def setup_final_round_for_sixteen_team_bracket(self, request):
        winnerSemiFinalGames = self.tournament.semifinal_round_games.all()
        semiFinalGameOne = winnerSemiFinalGames[0]
        semiFinalGameTwo = winnerSemiFinalGames[1]
        fifthPlaceSemifinalGameOne = winnerSemiFinalGames[2]
        fifthPlaceSemifinalGameTwo = winnerSemiFinalGames[3]
        created_by = request.user.profile
        championshipGame = Game(team_one=semiFinalGameOne.winner, team_two=semiFinalGameTwo.winner,
                                tournament=self.tournament,
                                game_type='Championship', created_by=created_by)
        thirdPlaceGame = Game(team_one=semiFinalGameOne.loser, team_two=semiFinalGameTwo.loser,
                              tournament=self.tournament,
                              game_type='3rd-Place Final', created_by=created_by)
        fifthPlaceGame = Game(team_one=fifthPlaceSemifinalGameOne.winner, team_two=fifthPlaceSemifinalGameTwo.winner,
                              tournament=self.tournament,
                              game_type='5th-Place Final', created_by=created_by)
        seventhPlaceGame = Game(team_one=fifthPlaceSemifinalGameOne.loser, team_two=fifthPlaceSemifinalGameTwo.loser,
                                tournament=self.tournament,
                                game_type='7th-Place Final', created_by=created_by)
        championshipGame.save()
        thirdPlaceGame.save()
        fifthPlaceGame.save()
        seventhPlaceGame.save()
        winnerGames = [championshipGame, thirdPlaceGame, fifthPlaceGame, seventhPlaceGame]
        self.tournament.final_round_initialized = True
        self.tournament.final_round_games.set(winnerGames)
        self.tournament.save()
        loserSemiFinalGames = self.tournament.losers_semifinal_round_games.all()
        ninthPlaceSemiFinalGameOne = loserSemiFinalGames[0]
        ninthPlaceSemiFinalGameTwo = loserSemiFinalGames[1]
        thirteenthPlaceSemiFinalGameOne = loserSemiFinalGames[2]
        thirteenthPlaceSemiFinalGameTwo = loserSemiFinalGames[3]
        ninthPlaceGame = Game(team_one=ninthPlaceSemiFinalGameOne.winner, team_two=ninthPlaceSemiFinalGameTwo.winner,
                              tournament=self.tournament,
                              game_type='9th-Place Final', created_by=created_by)
        eleventhPlaceGame = Game(team_one=ninthPlaceSemiFinalGameOne.loser, team_two=ninthPlaceSemiFinalGameTwo.loser,
                                 tournament=self.tournament,
                                 game_type='11th-Place Final', created_by=created_by)
        thirteenthPlaceGame = Game(team_one=thirteenthPlaceSemiFinalGameOne.winner,
                                   team_two=thirteenthPlaceSemiFinalGameTwo.winner,
                                   tournament=self.tournament,
                                   game_type='13th-Place Final', created_by=created_by)
        fifteenthPlaceGame = Game(team_one=thirteenthPlaceSemiFinalGameOne.loser,
                                  team_two=thirteenthPlaceSemiFinalGameOne.loser,
                                  tournament=self.tournament,
                                  game_type='15th-Place Final', created_by=created_by)
        ninthPlaceGame.save()
        eleventhPlaceGame.save()
        thirteenthPlaceGame.save()
        fifteenthPlaceGame.save()
        loserGames = [ninthPlaceGame, thirdPlaceGame, fifthPlaceGame, seventhPlaceGame]
        self.tournament.losers_final_round_initialized = True
        self.tournament.losers_final_round_games.set(loserGames)
        self.tournament.save()

    def simulate_bracket_game(self, request, game):
        gameSimulation = GameSimulation(self.tournament, game)
        gameSimulation.coin_flip()
        gameSimulation.simulationType = game.tournament.simulation_type
        gameSimulation.simulate_full_game()
        self.gameSimulationsList.append(gameSimulation)
        # Determine the winner and loser
        if gameSimulation.winner == gameSimulation.tournamentTeamOne:
            game.winner = gameSimulation.tournamentTeamOne
            game.loser = gameSimulation.tournamentTeamTwo
        else:
            game.winner = gameSimulation.tournamentTeamTwo
            game.loser = gameSimulation.tournamentTeamOne
        # Increment the winner and loser's statistics
        game.winner.bracket_play_wins += 1
        game.loser.bracket_play_losses += 1
        game.save()
        game.created_by = request.user.profile
        game.save()
        return game
