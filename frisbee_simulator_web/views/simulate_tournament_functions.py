import threading
from itertools import chain, count
from django.db.models import Sum, F
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

    def rank_teams_for_pool_play(self):
        teams = list(self.tournament.teams.all())
        teams.sort(key=lambda team: (-team.overall_rating, team.location))
        for i, team in enumerate(teams):
            pool_play_seed = i = 1
            tournament_team = TournamentTeam.objects.create(team=team, tournament=self.tournament,
                                                            pool_play_seed=pool_play_seed,
                                                            bracket_play_seed=pool_play_seed, pool_play_wins=0)
            tournament_team.save()

    def generate_round_robin_schedule(self, teams):
        n = len(teams)
        rounds = n - 1
        schedule = []
        for i in range(rounds):
            round = []
            for j in range(n // 2):
                if i % 2 == 0:
                    round.append((teams[j], teams[n - j - 1]))
                else:
                    round.append((teams[n - j - 1], teams[j]))
            schedule.append(round)
        return schedule

    def generate_pools_and_games(self, request, num_teams):
        tournament_teams = TournamentTeam.objects.filter(tournament=self.tournament)[:num_teams]
        num_pools = num_teams // 4
        threads = []

        for i in range(num_pools):
            start_index = i * 4
            pool_teams = tournament_teams[start_index:start_index + 4]
            pool = TournamentPool.objects.create(tournament=self.tournament, number_of_teams=len(pool_teams))
            pool.teams.set(pool_teams)
            pool.save()
            schedule = self.generate_round_robin_schedule(pool_teams)

            for round in schedule:
                for match in round:
                    game = Game(team_one=match[0], team_two=match[1], tournament=self.tournament, game_type='Pool Play')
                    thread = threading.Thread(target=self.simulate_pool_play_game, args=(request, game))
                    thread.start()
                    threads.append(thread)

        for thread in threads:
            thread.join()

    def simulate_four_team_pool(self, request):
        self.generate_pools_and_games(request, 4)

    def simulate_eight_team_pool(self, request):
        self.generate_pools_and_games(request, 8)

    def simulate_sixteen_team_pool(self, request):
        self.generate_pools_and_games(request, 16)

    def simulate_pool_play_game(self, request, game):
        gameSimulation = GameSimulation(self.tournament, game)
        gameSimulation.coin_flip()
        gameSimulation.simulationType = game.tournament.simulation_type
        gameSimulation.simulate_full_game()
        self.gameSimulationsList.append(gameSimulation)

        # Calculate pool play stats
        if gameSimulation.winner == gameSimulation.teamInGameSimulationOne:
            game.winner = gameSimulation.teamInGameSimulationOne.tournamentTeam
            game.loser = gameSimulation.teamInGameSimulationTwo.tournamentTeam
            point_differential = abs(
                gameSimulation.teamInGameSimulationOne.score - gameSimulation.teamInGameSimulationTwo.score)
            TournamentTeam.objects.filter(pk=game.winner.pk).update(pool_play_wins=F('pool_play_wins') + 1,
                                                                    pool_play_point_differential=F(
                                                                        'pool_play_point_differential') + point_differential)
            TournamentTeam.objects.filter(pk=game.loser.pk).update(pool_play_losses=F('pool_play_losses') + 1,
                                                                   pool_play_point_differential=F(
                                                                       'pool_play_point_differential') - point_differential)
        else:
            game.winner = gameSimulation.teamInGameSimulationTwo.tournamentTeam
            game.loser = gameSimulation.teamInGameSimulationOne.tournamentTeam
            point_differential = abs(
                gameSimulation.teamInGameSimulationTwo.score - gameSimulation.teamInGameSimulationOne.score)
            TournamentTeam.objects.filter(pk=game.winner.pk).update(pool_play_wins=F('pool_play_wins') + 1,
                                                                    pool_play_point_differential=F(
                                                                        'pool_play_point_differential') + point_differential)
            TournamentTeam.objects.filter(pk=game.loser.pk).update(pool_play_losses=F('pool_play_losses') + 1,
                                                                   pool_play_point_differential=F(
                                                                       'pool_play_point_differential') - point_differential)
        game.save()
        return game

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

    def simulate_four_team_bracket(self, request):
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
        self.simulate_bracket_game(request, game_one)
        game_two = Game(team_one=teams_in_bracket[1], team_two=teams_in_bracket[2],
                        tournament=tournament_bracket.tournament,
                        game_type='Semifinal', created_by=created_by)
        self.simulate_bracket_game(request, game_two)
        game_three = Game(team_one=game_one.loser, team_two=game_two.loser, tournament=tournament_bracket.tournament,
                          game_type='Third-Place', created_by=created_by)
        self.simulate_bracket_game(request, game_three)
        game_four = Game(team_one=game_one.winner, team_two=game_two.winner, tournament=tournament_bracket.tournament,
                         game_type='Championship', created_by=created_by)
        self.simulate_bracket_game(request, game_four)
        tournament_bracket.champion = game_four.winner
        tournament_bracket.save()
        self.champion = tournament_bracket.champion.team
        self.tournament.champion = self.champion

    def simulate_eight_team_winners_bracket(self, request, number_of_teams):
        tournament_pools = TournamentPool.objects.filter(tournament=self.tournament)
        if number_of_teams == 8:
            poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
            poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
            # poolA1 v pool B4, pool B2vA3, pool B1vA4, pool A2vB3
            teamsInBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolASortedTeams[1], poolBSortedTeams[1],
                              poolASortedTeams[2], poolBSortedTeams[2], poolASortedTeams[3], poolBSortedTeams[3]]
            tournament_bracket = TournamentBracket.objects.create(tournament=self.tournament, number_of_teams=8,
                                                                  bracket_type='Championship')
        elif number_of_teams == 16:
            poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
            poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
            poolCSortedTeams = tournament_pools[2].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
            poolDSortedTeams = tournament_pools[3].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
            # poolA1 v pool D2, pool B1vC2, pool B2vC1, pool A2v pool D1
            teamsInBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolCSortedTeams[0], poolDSortedTeams[0],
                              poolASortedTeams[1], poolBSortedTeams[1], poolCSortedTeams[1], poolDSortedTeams[1]]
            tournament_bracket = TournamentBracket.objects.create(tournament=self.tournament, number_of_teams=8,
                                                                  bracket_type='Championship')
        else:
            print('ERROR with number of TEAMS')
        tournament_bracket.teams.set(teamsInBracket)
        tournament_bracket.save()
        for i, team in enumerate(teamsInBracket, start=1):
            team.bracket_play_seed = i
            team.save()
        teams_in_bracket = tournament_bracket.teams.all()
        created_by = request.user.profile
        game_one = Game.objects.create(team_one=teams_in_bracket[0], team_two=teams_in_bracket[7],
                                       tournament=self.tournament,
                                       game_type='Quarterfinal', created_by=created_by)
        self.simulate_bracket_game(request, game_one)
        game_two = Game.objects.create(team_one=teams_in_bracket[1], team_two=teams_in_bracket[6],
                                       tournament=self.tournament,
                                       game_type='Quarterfinal', created_by=created_by)
        self.simulate_bracket_game(request, game_two)
        game_three = Game.objects.create(team_one=teams_in_bracket[2], team_two=teams_in_bracket[5],
                                         tournament=self.tournament,
                                         game_type='Quarterfinal', created_by=created_by)
        self.simulate_bracket_game(request, game_three)
        game_four = Game.objects.create(team_one=teams_in_bracket[3], team_two=teams_in_bracket[4],
                                        tournament=self.tournament,
                                        game_type='Quarterfinal', created_by=created_by)
        self.simulate_bracket_game(request, game_four)
        # Loser's Bracket
        game_five = Game.objects.create(team_one=game_one.loser, team_two=game_two.loser, tournament=self.tournament,
                                        game_type='Loser-Semifinal', created_by=created_by)
        self.simulate_bracket_game(request, game_five)
        game_six = Game.objects.create(team_one=game_three.loser, team_two=game_four.loser, tournament=self.tournament,
                                       game_type='Loser-Semifinal', created_by=created_by)
        self.simulate_bracket_game(request, game_six)
        game_seven = Game.objects.create(team_one=game_five.winner, team_two=game_six.winner,
                                         tournament=self.tournament,
                                         game_type='Fifth-Place-Final', created_by=created_by)
        self.simulate_bracket_game(request, game_seven)
        game_eight = Game.objects.create(team_one=game_five.loser, team_two=game_six.loser, tournament=self.tournament,
                                         game_type='Seventh-Place-Final', created_by=created_by)
        self.simulate_bracket_game(request, game_eight)
        # Winner's Bracket
        game_nine = Game.objects.create(team_one=game_one.winner, team_two=game_two.winner, tournament=self.tournament,
                                        game_type='Semifinal', created_by=created_by)
        self.simulate_bracket_game(request, game_nine)
        game_ten = Game.objects.create(team_one=game_three.winner, team_two=game_four.winner,
                                       tournament=self.tournament,
                                       game_type='Semifinal', created_by=created_by)
        self.simulate_bracket_game(request, game_ten)
        game_eleven = Game.objects.create(team_one=game_nine.loser, team_two=game_ten.loser, tournament=self.tournament,
                                          game_type='Third-Place', created_by=created_by)
        self.simulate_bracket_game(request, game_eleven)
        game_twelve = Game.objects.create(team_one=game_nine.winner, team_two=game_ten.winner,
                                          tournament=self.tournament,
                                          game_type='Championship', created_by=created_by)
        self.simulate_bracket_game(request, game_twelve)
        tournament_bracket.champion = game_twelve.winner
        tournament_bracket.save()
        self.champion = tournament_bracket.champion.team
        self.tournament.champion = self.champion

    def simulate_eight_team_losers_bracket(self, request):
        tournament_pools = TournamentPool.objects.filter(tournament=self.tournament)
        poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        poolCSortedTeams = tournament_pools[2].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        poolDSortedTeams = tournament_pools[3].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
        # poolA3 v pool D4, pool A4v pool D3, pool B3vC4, pool B4vC3
        teamsInBracket = [poolASortedTeams[2], poolBSortedTeams[2], poolCSortedTeams[2], poolDSortedTeams[2],
                          poolASortedTeams[3], poolBSortedTeams[3], poolCSortedTeams[3], poolDSortedTeams[3]]
        tournament_bracket = TournamentBracket.objects.create(tournament=self.tournament, number_of_teams=8,
                                                              bracket_type='Loser')
        tournament_bracket.teams.set(teamsInBracket)
        tournament_bracket.save()
        for i, team in enumerate(teamsInBracket, start=1):
            team.bracket_play_seed = i
            team.save()
        teams_in_bracket = tournament_bracket.teams.all()
        created_by = request.user.profile
        game_one = Game.objects.create(team_one=teams_in_bracket[0], team_two=teams_in_bracket[7],
                                       tournament=self.tournament,
                                       game_type='9th-Place Quarterfinal', created_by=created_by)
        self.simulate_bracket_game(request, game_one)
        game_two = Game.objects.create(team_one=teams_in_bracket[1], team_two=teams_in_bracket[6],
                                       tournament=self.tournament,
                                       game_type='9th-Place Quarterfinal', created_by=created_by)
        self.simulate_bracket_game(request, game_two)
        game_three = Game.objects.create(team_one=teams_in_bracket[2], team_two=teams_in_bracket[5],
                                         tournament=self.tournament,
                                         game_type='9th-Place Quarterfinal', created_by=created_by)
        self.simulate_bracket_game(request, game_three)
        game_four = Game.objects.create(team_one=teams_in_bracket[3], team_two=teams_in_bracket[4],
                                        tournament=self.tournament,
                                        game_type='9th-Place Quarterfinal', created_by=created_by)
        self.simulate_bracket_game(request, game_four)
        # Loser's Bracket
        game_five = Game.objects.create(team_one=game_one.loser, team_two=game_two.loser, tournament=self.tournament,
                                        game_type='13th-Place Semifinal', created_by=created_by)
        self.simulate_bracket_game(request, game_five)
        game_six = Game.objects.create(team_one=game_three.loser, team_two=game_four.loser, tournament=self.tournament,
                                       game_type='13th-Place Semifinal', created_by=created_by)
        self.simulate_bracket_game(request, game_six)
        game_seven = Game.objects.create(team_one=game_five.winner, team_two=game_six.winner,
                                         tournament=self.tournament,
                                         game_type='13th-Place Final', created_by=created_by)
        self.simulate_bracket_game(request, game_seven)
        game_eight = Game.objects.create(team_one=game_five.loser, team_two=game_six.loser, tournament=self.tournament,
                                         game_type='15th-Place Final', created_by=created_by)
        self.simulate_bracket_game(request, game_eight)
        # Winner's Bracket
        game_nine = Game.objects.create(team_one=game_one.winner, team_two=game_two.winner, tournament=self.tournament,
                                        game_type='9th-Place Semifinal', created_by=created_by)
        self.simulate_bracket_game(request, game_nine)
        game_ten = Game.objects.create(team_one=game_three.winner, team_two=game_four.winner,
                                       tournament=self.tournament,
                                       game_type='9th-Place Semifinal', created_by=created_by)
        self.simulate_bracket_game(request, game_ten)
        game_eleven = Game.objects.create(team_one=game_nine.loser, team_two=game_ten.loser, tournament=self.tournament,
                                          game_type='11th-Place Final', created_by=created_by)
        self.simulate_bracket_game(request, game_eleven)
        game_twelve = Game.objects.create(team_one=game_nine.winner, team_two=game_ten.winner,
                                          tournament=self.tournament,
                                          game_type='9th-Place Final', created_by=created_by)
        self.simulate_bracket_game(request, game_twelve)
        tournament_bracket.champion = game_twelve.winner
        tournament_bracket.save()

    def save_tournament_player_stats_from_game_player_stats(self):
        for gameSimulation in self.gameSimulationsList:
            for teamInGameSimulation in [gameSimulation.teamInGameSimulationOne,
                                         gameSimulation.teamInGameSimulationTwo]:
                for gameSimulationPlayer in teamInGameSimulation.allPlayers:
                    gameStats = PlayerGameStat.objects.filter(player=gameSimulationPlayer.player,
                                                              tournament=self.tournament)
                    playerTournamentStat, created = PlayerTournamentStat.objects.get_or_create(
                        tournament=self.tournament,
                        player=gameSimulationPlayer.player,
                    )
                    aggregates = gameStats.aggregate(
                        goals=Sum('goals'),
                        assists=Sum('assists'),
                        swing_passes_thrown=Sum('swing_passes_thrown'),
                        swing_passes_completed=Sum('swing_passes_completed'),
                        under_passes_thrown=Sum('under_passes_thrown'),
                        under_passes_completed=Sum('under_passes_completed'),
                        short_hucks_thrown=Sum('short_hucks_thrown'),
                        short_hucks_completed=Sum('short_hucks_completed'),
                        deep_hucks_thrown=Sum('deep_hucks_thrown'),
                        deep_hucks_completed=Sum('deep_hucks_completed'),
                        throwing_yards=Sum('throwing_yards'),
                        receiving_yards=Sum('receiving_yards'),
                        turnovers_forced=Sum('turnovers_forced'),
                        throwaways=Sum('throwaways'),
                        drops=Sum('drops'),
                        callahans=Sum('callahans'),
                        pulls=Sum('pulls')
                    )
                    for attr, value in aggregates.items():
                        if value is not None:
                            setattr(playerTournamentStat, attr, value)
                    playerTournamentStat.save()
