import random
import threading
from itertools import chain, count

from django.contrib import messages
from django.db.models import Sum, F, Prefetch
from django.shortcuts import render, redirect

from frisbee_simulator_web.models import PlayerTournamentStat, TournamentTeam, TournamentPool, Game, TournamentBracket, \
    PlayerGameStat, Tournament
from frisbee_simulator_web.views.simulate_game_functions import GameSimulation


def setup_manual_pool_play_games_for_simulation(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_teams = list(TournamentTeam.objects.filter(tournament=tournament))
    num_teams = len(tournament_teams)
    games = []
    # Check the number of teams and create games accordingly
    if num_teams == 4:
        pool = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(tournament_teams),
                                             name='Pool A')
        pool.teams.set(tournament_teams)
        for team in tournament_teams:
            team.pool = pool
            team.save()
        pool.save()
        # Round  1
        games.extend([
            Game.objects.create(team_one=tournament_teams[0], team_two=tournament_teams[1],
                                tournament=tournament, game_type='Pool Play'),
            Game.objects.create(team_one=tournament_teams[2], team_two=tournament_teams[3],
                                tournament=tournament, game_type='Pool Play')
        ])
        # Round  2
        games.extend([
            Game.objects.create(team_one=tournament_teams[0], team_two=tournament_teams[2],
                                tournament=tournament, game_type='Pool Play'),
            Game.objects.create(team_one=tournament_teams[1], team_two=tournament_teams[3],
                                tournament=tournament, game_type='Pool Play')
        ])
        # Round  3
        games.extend([
            Game.objects.create(team_one=tournament_teams[0], team_two=tournament_teams[3],
                                tournament=tournament, game_type='Pool Play'),
            Game.objects.create(team_one=tournament_teams[1], team_two=tournament_teams[2],
                                tournament=tournament, game_type='Pool Play')
        ])
    elif num_teams == 8:
        poolATeams = tournament_teams[:4]
        poolBTeams = tournament_teams[4:]
        poolA = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolATeams),
                                              name='Pool A')
        poolB = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolBTeams),
                                              name='Pool B')
        poolA.teams.set(poolATeams)
        for team in poolATeams:
            team.pool = poolA
            team.save()
        poolA.save()
        poolB.teams.set(poolBTeams)
        for team in poolBTeams:
            team.pool = poolB
            team.save()
        poolB.save()
        # Pool A games
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[2], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  2
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  3
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA)
        ])
        # Pool B games
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[2], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  2
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  3
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB)
        ])
    elif num_teams == 16:
        poolATeams = tournament_teams[:4]
        poolBTeams = tournament_teams[4:8]
        poolCTeams = tournament_teams[8:12]
        poolDTeams = tournament_teams[12:]
        poolA = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolATeams),
                                              name='Pool A')
        poolB = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolBTeams),
                                              name='Pool B')
        poolC = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolCTeams),
                                              name='Pool C')
        poolD = TournamentPool.objects.create(tournament=tournament, number_of_teams=len(poolDTeams),
                                              name='Pool D')
        poolA.teams.set(poolATeams)
        poolA.save()
        poolB.teams.set(poolBTeams)
        poolB.save()
        poolC.teams.set(poolCTeams)
        poolC.save()
        poolD.teams.set(poolDTeams)
        poolD.save()
        for team in poolATeams:
            team.pool = poolA
            team.save()
        for team in poolBTeams:
            team.pool = poolB
            team.save()
        for team in poolCTeams:
            team.pool = poolC
            team.save()
        for team in poolDTeams:
            team.pool = poolD
            team.save()
        # Pool A games
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[2], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  2
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            # Round  3
            Game.objects.create(team_one=poolATeams[0], team_two=poolATeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolA),
            Game.objects.create(team_one=poolATeams[1], team_two=poolATeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolA)
        ])
        # Pool B games
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[2], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  2
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            # Round  3
            Game.objects.create(team_one=poolBTeams[0], team_two=poolBTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolB),
            Game.objects.create(team_one=poolBTeams[1], team_two=poolBTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolB)
        ])
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[2], team_two=poolCTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            # Round  2
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[1], team_two=poolCTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            # Round  3
            Game.objects.create(team_one=poolCTeams[0], team_two=poolCTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolC),
            Game.objects.create(team_one=poolCTeams[1], team_two=poolCTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolC)
        ])
        games.extend([
            # Round  1
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[1], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[2], team_two=poolDTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            # Round  2
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[1], team_two=poolDTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            # Round  3
            Game.objects.create(team_one=poolDTeams[0], team_two=poolDTeams[3], tournament=tournament,
                                game_type='Pool Play', pool=poolD),
            Game.objects.create(team_one=poolDTeams[1], team_two=poolDTeams[2], tournament=tournament,
                                game_type='Pool Play', pool=poolD)
        ])
    tournament.pool_play_initialized = True
    tournament.pool_play_games.set(games)
    tournament.save()


def automatically_rank_teams_for_pool_play(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    teams = list(tournament.teams.all())
    teams.sort(key=lambda team: (-team.overall_rating, team.location))
    for i, team in enumerate(teams):
        pool_play_seed = i + 1
        tournament_team = TournamentTeam.objects.create(team=team, tournament=tournament,
                                                        pool_play_seed=pool_play_seed,
                                                        bracket_play_seed=pool_play_seed, pool_play_wins=0)
        tournament_team.save()
    tournament.save()


def manually_rank_teams_for_pool_play(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_teams = TournamentTeam.objects.filter(tournament=tournament)
    if request.method == 'POST':
        # Extract seeds from the POST data
        seeds = {key.split('-')[1]: int(value) for key, value in request.POST.items() if key.startswith('seed-')}

        # Check if all seeds are unique and within the valid range
        if len(seeds) != tournament.teams.count():
            messages.error(request, "Each team must have a unique seed.")
            return render(request, 'pool_play/manually_rank_teams_for_pool_play.html',
                          {'tournament': tournament, 'teams': tournament_teams})
        if len(set(seeds.values())) != len(seeds):
            messages.error(request, "Seeds must be unique.")
            return render(request, 'pool_play/manually_rank_teams_for_pool_play.html',
                          {'tournament': tournament, 'teams': tournament_teams})
        min_seed = 1
        max_seed = tournament.teams.count()
        if not all(min_seed <= seed <= max_seed for seed in seeds.values()):
            messages.error(request, f"Seeds must be between {min_seed} and {max_seed}.")
            return render(request, 'pool_play/manually_rank_teams_for_pool_play.html',
                          {'tournament': tournament, 'teams': tournament_teams})

        # If validation passes, update the teams' seeds
        for team_id, seed in seeds.items():
            team = TournamentTeam.objects.get(id=team_id, tournament=tournament)
            team.seed = seed
            team.save()

        # Mark the seeds as set for the tournament
        tournament.pool_play_seeds_set = True
        tournament.save()

        # Redirect back to the pool play overview or another appropriate view
        return redirect('pool_play_overview', tournament_id=tournament.id)
    else:
        # Render the template for manual seed setting
        return render(request, 'pool_play/manually_rank_teams_for_pool_play.html',
                      {'tournament': tournament, 'teams': tournament_teams})


def setup_semifinal_round_for_four_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_pool = TournamentPool.objects.get(tournament=tournament)
    teams = tournament_pool.teams.all()
    sorted_teams = teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    tournament_bracket = TournamentBracket(tournament=tournament, number_of_teams=4,
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
    tournament.semifinal_round_initialized = True
    tournament.semifinal_round_games.set(games)
    tournament.save()


def setup_final_round_for_four_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    semifinalGames = tournament.semifinal_round_games.all()
    semifinalGameOne = semifinalGames[0]
    semifinalGameTwo = semifinalGames[1]
    created_by = request.user.profile
    third_place_game = Game(team_one=semifinalGameOne.loser, team_two=semifinalGameTwo.loser,
                            tournament=tournament,
                            game_type='3rd-Place Final', created_by=created_by)
    championship_game = Game(team_one=semifinalGameOne.winner, team_two=semifinalGameTwo.winner,
                             tournament=tournament,
                             game_type='Championship', created_by=created_by)
    third_place_game.save()
    championship_game.save()
    games = [third_place_game, championship_game]
    tournament.final_round_initialized = True
    tournament.final_round_games.set(games)
    tournament.save()


def setup_quarterfinal_round_for_8_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    poolA = TournamentPool.objects.get(tournament=tournament, name='Pool A')
    poolB = TournamentPool.objects.get(tournament=tournament, name='Pool B')
    poolASortedTeams = poolA.teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolBSortedTeams = poolB.teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    # poolA1 v pool B4, pool B2vA3, pool B1vA4, pool A2vB3
    teamsInBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolASortedTeams[1], poolBSortedTeams[1],
                      poolASortedTeams[2], poolBSortedTeams[2], poolASortedTeams[3], poolBSortedTeams[3]]
    tournament_bracket = TournamentBracket.objects.create(tournament=tournament, number_of_teams=8,
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
    tournament.quarterfinal_round_initialized = True
    tournament.quarterfinal_round_games.set(games)
    tournament.save()


def setup_semifinal_round_for_eight_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    quarterFinalGames = tournament.quarterfinal_round_games.all()
    quarterFinalGameOne = quarterFinalGames[0]
    quarterFinalGameTwo = quarterFinalGames[1]
    quarterFinalGameThree = quarterFinalGames[2]
    quarterFinalGameFour = quarterFinalGames[3]
    created_by = request.user.profile
    semiFinalGameOne = Game(team_one=quarterFinalGameOne.winner, team_two=quarterFinalGameTwo.winner,
                            tournament=tournament,
                            game_type='Semifinal', created_by=created_by)
    semiFinalGameTwo = Game(team_one=quarterFinalGameThree.winner, team_two=quarterFinalGameFour.winner,
                            tournament=tournament,
                            game_type='Semifinal', created_by=created_by)
    loserSemiFinalGameOne = Game(team_one=quarterFinalGameOne.loser, team_two=quarterFinalGameTwo.loser,
                                 tournament=tournament,
                                 game_type='5th-Place Semifinal', created_by=created_by)
    loserSemiFinalGameTwo = Game(team_one=quarterFinalGameThree.loser, team_two=quarterFinalGameFour.loser,
                                 tournament=tournament,
                                 game_type='5th-Place Semifinal', created_by=created_by)
    semiFinalGameOne.save()
    semiFinalGameTwo.save()
    loserSemiFinalGameOne.save()
    loserSemiFinalGameTwo.save()
    games = [semiFinalGameOne, semiFinalGameTwo, loserSemiFinalGameOne, loserSemiFinalGameTwo]
    tournament.semifinal_round_initialized = True
    tournament.semifinal_round_games.set(games)
    tournament.save()


def setup_final_round_for_eight_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    semiFinalGames = tournament.semifinal_round_games.all()
    semiFinalGameOne = semiFinalGames[0]
    semiFinalGameTwo = semiFinalGames[1]
    loserSemiFinalGameOne = semiFinalGames[2]
    loserSemiFinalGameTwo = semiFinalGames[3]
    created_by = request.user.profile
    championshipGame = Game(team_one=semiFinalGameOne.winner, team_two=semiFinalGameTwo.winner,
                            tournament=tournament,
                            game_type='Championship', created_by=created_by)
    thirdPlaceGame = Game(team_one=semiFinalGameOne.loser, team_two=semiFinalGameTwo.loser,
                          tournament=tournament,
                          game_type='3rd-Place Final', created_by=created_by)
    fifthPlaceGame = Game(team_one=loserSemiFinalGameOne.winner, team_two=loserSemiFinalGameTwo.winner,
                          tournament=tournament,
                          game_type='5th-Place Final', created_by=created_by)
    seventhPlaceGame = Game(team_one=loserSemiFinalGameOne.loser, team_two=loserSemiFinalGameTwo.loser,
                            tournament=tournament,
                            game_type='7th-Place Final', created_by=created_by)
    championshipGame.save()
    thirdPlaceGame.save()
    fifthPlaceGame.save()
    seventhPlaceGame.save()
    games = [championshipGame, thirdPlaceGame, fifthPlaceGame, seventhPlaceGame]
    tournament.final_round_initialized = True
    tournament.final_round_games.set(games)
    tournament.save()


def setup_prequarterfinal_round_for_sixteen_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_pools = TournamentPool.objects.filter(tournament=tournament)
    poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolCSortedTeams = tournament_pools[2].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolDSortedTeams = tournament_pools[3].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    teamsInWinnersBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolCSortedTeams[0], poolDSortedTeams[0],
                             poolASortedTeams[1], poolBSortedTeams[1], poolCSortedTeams[1], poolDSortedTeams[1],
                             poolASortedTeams[2], poolBSortedTeams[2], poolCSortedTeams[2], poolDSortedTeams[2]]
    winnersBracket = TournamentBracket.objects.create(tournament=tournament, number_of_teams=12,
                                                      bracket_type='Championship')
    winnersBracket.teams.set(teamsInWinnersBracket)
    winnersBracket.save()
    for i, team in enumerate(teamsInWinnersBracket, start=1):
        team.bracket_play_seed = i
        team.save()
    created_by = request.user.profile
    # Pool B2 v Pool C3
    prequarter_game_one = Game(team_one=poolBSortedTeams[1], team_two=poolCSortedTeams[2],
                               tournament=tournament,
                               game_type='Pre-Quarterfinal', created_by=created_by)
    # Pool C2 v B3
    prequarter_game_two = Game(team_one=poolCSortedTeams[1], team_two=poolBSortedTeams[2],
                               tournament=tournament,
                               game_type='Pre-Quarterfinal', created_by=created_by)
    # Pool D2 v A3
    prequarter_game_three = Game(team_one=poolDSortedTeams[1], team_two=poolASortedTeams[2],
                                 tournament=tournament,
                                 game_type='Pre-Quarterfinal', created_by=created_by)
    # Pool A2 v D3
    prequarter_game_four = Game(team_one=poolASortedTeams[1], team_two=poolDSortedTeams[2],
                                tournament=tournament,
                                game_type='Pre-Quarterfinal', created_by=created_by)
    prequarter_game_one.save()
    prequarter_game_two.save()
    prequarter_game_three.save()
    prequarter_game_four.save()
    prequarter_games = [prequarter_game_one, prequarter_game_two, prequarter_game_three, prequarter_game_four]
    tournament.pre_quarterfinal_round_initialized = True
    tournament.pre_quarterfinal_round_games.set(prequarter_games)
    tournament.save()


def setup_quarterfinal_round_for_sixteen_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    winnerPrequarterFinalGames = tournament.pre_quarterfinal_round_games.all()
    winnerPrequarterFinalGameOne = winnerPrequarterFinalGames[0]
    winnerPrequarterFinalGameTwo = winnerPrequarterFinalGames[1]
    winnerPrequarterFinalGameThree = winnerPrequarterFinalGames[2]
    winnerPrequarterFinalGameFour = winnerPrequarterFinalGames[3]
    created_by = request.user.profile
    tournament_pools = TournamentPool.objects.filter(tournament=tournament)
    poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolCSortedTeams = tournament_pools[2].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolDSortedTeams = tournament_pools[3].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    teamsInWinnersBracket = [poolASortedTeams[0], poolBSortedTeams[0], poolCSortedTeams[0], poolDSortedTeams[0],
                             winnerPrequarterFinalGameOne.winner, winnerPrequarterFinalGameTwo.winner,
                             winnerPrequarterFinalGameThree.winner, winnerPrequarterFinalGameFour.winner]
    winnersBracket = TournamentBracket.objects.create(tournament=tournament, number_of_teams=8,
                                                      bracket_type='Championship')
    winnersBracket.teams.set(teamsInWinnersBracket)
    winnersBracket.save()
    winnerQuarterFinalGameOne = Game(team_one=teamsInWinnersBracket[0],
                                     team_two=winnerPrequarterFinalGameOne.winner,
                                     tournament=tournament,
                                     game_type='Quarterfinal', created_by=created_by)
    winnerQuarterFinalGameTwo = Game(team_one=teamsInWinnersBracket[1],
                                     team_two=winnerPrequarterFinalGameTwo.winner,
                                     tournament=tournament,
                                     game_type='Quarterfinal', created_by=created_by)
    winnerQuarterFinalGameThree = Game(team_one=teamsInWinnersBracket[2],
                                       team_two=winnerPrequarterFinalGameThree.winner,
                                       tournament=tournament,
                                       game_type='Quarterfinal', created_by=created_by)
    winnerQuarterFinalGameFour = Game(team_one=teamsInWinnersBracket[3],
                                      team_two=winnerPrequarterFinalGameFour.winner,
                                      tournament=tournament,
                                      game_type='Quarterfinal', created_by=created_by)
    winnerQuarterFinalGameOne.save()
    winnerQuarterFinalGameTwo.save()
    winnerQuarterFinalGameThree.save()
    winnerQuarterFinalGameFour.save()
    for i, team in enumerate(teamsInWinnersBracket, start=1):
        team.bracket_play_seed = i
        team.save()
    winner_games = [winnerQuarterFinalGameOne, winnerQuarterFinalGameTwo, winnerQuarterFinalGameThree,
                    winnerQuarterFinalGameFour]
    tournament.quarterfinal_round_initialized = True
    tournament.quarterfinal_round_games.set(winner_games)
    tournament.save()


def setup_semifinal_round_for_sixteen_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    winnerQuarterFinalGames = tournament.quarterfinal_round_games.all()
    winnerQuarterFinalGameOne = winnerQuarterFinalGames[0]
    winnerQuarterFinalGameTwo = winnerQuarterFinalGames[1]
    winnerQuarterFinalGameThree = winnerQuarterFinalGames[2]
    winnerQuarterFinalGameFour = winnerQuarterFinalGames[3]
    created_by = request.user.profile
    winnerSemiFinalGameOne = Game(team_one=winnerQuarterFinalGameOne.winner,
                                  team_two=winnerQuarterFinalGameTwo.winner,
                                  tournament=tournament,
                                  game_type='Semifinal', created_by=created_by)
    winnerSemiFinalGameTwo = Game(team_one=winnerQuarterFinalGameThree.winner,
                                  team_two=winnerQuarterFinalGameFour.winner,
                                  tournament=tournament,
                                  game_type='Semifinal', created_by=created_by)
    fifthPlaceSemiFinalGameOne = Game(team_one=winnerQuarterFinalGameOne.loser,
                                      team_two=winnerQuarterFinalGameTwo.loser,
                                      tournament=tournament,
                                      game_type='5th-Place Semifinal', created_by=created_by)
    fifthPlaceSemiFinalGameTwo = Game(team_one=winnerQuarterFinalGameThree.loser,
                                      team_two=winnerQuarterFinalGameFour.loser,
                                      tournament=tournament,
                                      game_type='5th-Place Semifinal', created_by=created_by)
    winnerSemiFinalGameOne.save()
    winnerSemiFinalGameTwo.save()
    fifthPlaceSemiFinalGameOne.save()
    fifthPlaceSemiFinalGameTwo.save()
    winnerGames = [winnerSemiFinalGameOne, winnerSemiFinalGameTwo, fifthPlaceSemiFinalGameOne,
                   fifthPlaceSemiFinalGameTwo]
    tournament.semifinal_round_initialized = True
    tournament.semifinal_round_games.set(winnerGames)
    tournament.save()
    prequarterFinalGames = tournament.pre_quarterfinal_round_games.all()
    prequarterFinalGameOne = prequarterFinalGames[0]
    prequarterFinalGameTwo = prequarterFinalGames[1]
    prequarterFinalGameThree = prequarterFinalGames[2]
    prequarterFinalGameFour = prequarterFinalGames[3]
    ninthPlaceSemiFinalGameOne = Game(team_one=prequarterFinalGameOne.loser,
                                      team_two=prequarterFinalGameFour.loser,
                                      tournament=tournament,
                                      game_type='9th-Place Semifinal', created_by=created_by)
    ninthPlaceSemiFinalGameTwo = Game(team_one=prequarterFinalGameTwo.loser,
                                      team_two=prequarterFinalGameThree.loser,
                                      tournament=tournament,
                                      game_type='9th-Place Semifinal', created_by=created_by)
    tournament_pools = TournamentPool.objects.filter(tournament=tournament)
    poolASortedTeams = tournament_pools[0].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolBSortedTeams = tournament_pools[1].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolCSortedTeams = tournament_pools[2].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    poolDSortedTeams = tournament_pools[3].teams.order_by('-pool_play_wins', 'pool_play_point_differential')
    thirteenthPlaceSemiFinalGameOne = Game(team_one=poolASortedTeams[3],
                                           team_two=poolDSortedTeams[3],
                                           tournament=tournament,
                                           game_type='13th-Place Semifinal', created_by=created_by)
    thirteenthPlaceSemiFinalGameTwo = Game(team_one=poolBSortedTeams[3],
                                           team_two=poolCSortedTeams[3],
                                           tournament=tournament,
                                           game_type='13th-Place Semifinal', created_by=created_by)
    ninthPlaceSemiFinalGameOne.save()
    ninthPlaceSemiFinalGameTwo.save()
    thirteenthPlaceSemiFinalGameOne.save()
    thirteenthPlaceSemiFinalGameTwo.save()
    loserGames = [ninthPlaceSemiFinalGameOne, ninthPlaceSemiFinalGameTwo, thirteenthPlaceSemiFinalGameOne,
                  thirteenthPlaceSemiFinalGameTwo]
    tournament.losers_semifinal_round_initialized = True
    tournament.losers_semifinal_round_games.set(loserGames)
    tournament.save()


def setup_final_round_for_sixteen_team_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    winnerSemiFinalGames = tournament.semifinal_round_games.all()
    semiFinalGameOne = winnerSemiFinalGames[0]
    semiFinalGameTwo = winnerSemiFinalGames[1]
    fifthPlaceSemifinalGameOne = winnerSemiFinalGames[2]
    fifthPlaceSemifinalGameTwo = winnerSemiFinalGames[3]
    created_by = request.user.profile
    championshipGame = Game(team_one=semiFinalGameOne.winner, team_two=semiFinalGameTwo.winner,
                            tournament=tournament,
                            game_type='Championship', created_by=created_by)
    thirdPlaceGame = Game(team_one=semiFinalGameOne.loser, team_two=semiFinalGameTwo.loser,
                          tournament=tournament,
                          game_type='3rd-Place Final', created_by=created_by)
    fifthPlaceGame = Game(team_one=fifthPlaceSemifinalGameOne.winner, team_two=fifthPlaceSemifinalGameTwo.winner,
                          tournament=tournament,
                          game_type='5th-Place Final', created_by=created_by)
    seventhPlaceGame = Game(team_one=fifthPlaceSemifinalGameOne.loser, team_two=fifthPlaceSemifinalGameTwo.loser,
                            tournament=tournament,
                            game_type='7th-Place Final', created_by=created_by)
    championshipGame.save()
    thirdPlaceGame.save()
    fifthPlaceGame.save()
    seventhPlaceGame.save()
    winnerGames = [championshipGame, thirdPlaceGame, fifthPlaceGame, seventhPlaceGame]
    tournament.final_round_initialized = True
    tournament.final_round_games.set(winnerGames)
    tournament.save()
    loserSemiFinalGames = tournament.losers_semifinal_round_games.all()
    ninthPlaceSemiFinalGameOne = loserSemiFinalGames[0]
    ninthPlaceSemiFinalGameTwo = loserSemiFinalGames[1]
    thirteenthPlaceSemiFinalGameOne = loserSemiFinalGames[2]
    thirteenthPlaceSemiFinalGameTwo = loserSemiFinalGames[3]
    ninthPlaceGame = Game(team_one=ninthPlaceSemiFinalGameOne.winner, team_two=ninthPlaceSemiFinalGameTwo.winner,
                          tournament=tournament,
                          game_type='9th-Place Final', created_by=created_by)
    eleventhPlaceGame = Game(team_one=ninthPlaceSemiFinalGameOne.loser, team_two=ninthPlaceSemiFinalGameTwo.loser,
                             tournament=tournament,
                             game_type='11th-Place Final', created_by=created_by)
    thirteenthPlaceGame = Game(team_one=thirteenthPlaceSemiFinalGameOne.winner,
                               team_two=thirteenthPlaceSemiFinalGameTwo.winner,
                               tournament=tournament,
                               game_type='13th-Place Final', created_by=created_by)
    fifteenthPlaceGame = Game(team_one=thirteenthPlaceSemiFinalGameOne.loser,
                              team_two=thirteenthPlaceSemiFinalGameOne.loser,
                              tournament=tournament,
                              game_type='15th-Place Final', created_by=created_by)
    ninthPlaceGame.save()
    eleventhPlaceGame.save()
    thirteenthPlaceGame.save()
    fifteenthPlaceGame.save()
    loserGames = [ninthPlaceGame, eleventhPlaceGame, thirteenthPlaceGame, fifteenthPlaceGame]
    tournament.losers_final_round_initialized = True
    tournament.losers_final_round_games.set(loserGames)
    tournament.save()


def simulate_bracket_game(request, game, tournament):
    gameSimulation = GameSimulation(tournament, game)
    gameSimulation.coin_flip()
    gameSimulation.simulationType = game.tournament.simulation_type
    gameSimulation.simulate_full_game()
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
