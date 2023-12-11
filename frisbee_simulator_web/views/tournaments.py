import random
from itertools import chain

from django.shortcuts import render
from django.views.generic.edit import CreateView
from frisbee_simulator_web.models import Tournament, TournamentTeam, Game, TournamentPool, TournamentBracket
from frisbee_simulator_web.forms import TournamentForm
from frisbee_simulator_web.views.simulate_game_functions import GameSimulation
from frisbee_simulator_web.views.teams import create_random_team


class TournamentCreateView(CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournaments/create_tournament.html'
    success_url = '/tournaments/list/'

    def form_valid(self, form):
        response = super().form_valid(form)
        number_of_teams = int(form.cleaned_data['number_of_teams'])
        for _ in range(number_of_teams):
            team = create_random_team(self.request)
            self.object.teams.add(team)
        self.object.save()
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)


def list_tournaments(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournaments/list_tournaments.html', {'tournaments': tournaments})


def rank_teams_for_pool_play(tournament):
    teams = list(tournament.teams.all())
    teams.sort(key=lambda team: (-team.overall_rating, team.location))
    for i, team in enumerate(teams):
        pool_play_seed = i = 1
        tournament_team = TournamentTeam.objects.create(team=team, tournament=tournament, pool_play_seed=pool_play_seed,
                                                        bracket_play_seed=pool_play_seed, pool_play_wins=0)
        tournament_team.save()


def simulate_four_team_pool(tournament):
    tournament_teams = TournamentTeam.objects.filter(tournament=tournament)
    pool = TournamentPool.objects.create(tournament=tournament, number_of_teams=4)
    pool.teams.set(tournament_teams)
    pool.save()
    teams_in_pool = pool.teams.all()
    game_one = Game(team_one=teams_in_pool[0], team_two=teams_in_pool[1],
                    tournament=tournament,
                    game_type='Pool Play')
    game_two = Game(team_one=teams_in_pool[0], team_two=teams_in_pool[2],
                    tournament=tournament,
                    game_type='Pool Play')
    game_three = Game(team_one=teams_in_pool[0], team_two=teams_in_pool[3],
                      tournament=tournament,
                      game_type='Pool Play')
    game_four = Game(team_one=teams_in_pool[1], team_two=teams_in_pool[2],
                     tournament=tournament,
                     game_type='Pool Play')
    game_five = Game(team_one=teams_in_pool[1], team_two=teams_in_pool[3],
                     tournament=tournament,
                     game_type='Pool Play')
    game_six = Game(team_one=teams_in_pool[2], team_two=teams_in_pool[3],
                    tournament=tournament,
                    game_type='Pool Play')
    simulate_pool_play_game(game_one)
    simulate_pool_play_game(game_two)
    simulate_pool_play_game(game_three)
    simulate_pool_play_game(game_four)
    simulate_pool_play_game(game_five)
    simulate_pool_play_game(game_six)


def simulate_eight_team_pool(tournament):
    tournament_teams = TournamentTeam.objects.filter(tournament=tournament)
    poolOne = TournamentPool.objects.create(tournament=tournament, number_of_teams=4)
    poolTwo = TournamentPool.objects.create(tournament=tournament, number_of_teams=4)
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
                         tournament=tournament, game_type='Pool Play')
            game2 = Game(home_team=poolTwo.teams.all()[j], away_team=poolTwo.teams.all()[3 - j],
                         tournament=tournament, game_type='Pool Play')
            game1.save()
            game2.save()
            simulate_pool_play_game(game1)
            simulate_pool_play_game(game2)
            game1.save()
            game2.save()


def simulate_pool_play_game(game):
    gameSimulation = GameSimulation(game)
    gameSimulation.coin_flip()
    gameSimulation.simulationType = game.tournament.simulation_type
    gameSimulation.simulate_full_game()
    if gameSimulation.winner == gameSimulation.teamOne:
        game.winner = gameSimulation.teamOne.tournamentTeam
        game.loser = gameSimulation.teamTwo.tournamentTeam
        point_differential = gameSimulation.teamOne.score - gameSimulation.teamTwo.score
    else:
        game.winner = gameSimulation.teamTwo.tournamentTeam
        game.loser = gameSimulation.teamOne.tournamentTeam
        point_differential = gameSimulation.teamTwo.score - gameSimulation.teamOne.score
    game.save()
    game.winner.pool_play_wins += 1
    game.loser.pool_play_losses += 1
    game.loser.pool_play_point_differential = point_differential
    game.loser.pool_play_point_differential = point_differential * (-1)
    game.save()
    return game


def simulate_bracket_game(game):
    gameSimulation = GameSimulation(game)
    gameSimulation.coin_flip()
    gameSimulation.simulate_full_game()
    if gameSimulation.winner == gameSimulation.teamOne:
        game.winner = gameSimulation.teamOne.tournamentTeam
        game.loser = gameSimulation.teamTwo.tournamentTeam
    else:
        game.winner = gameSimulation.teamTwo.tournamentTeam
        game.loser = gameSimulation.teamOne.tournamentTeam
    game.save()
    game.winner.bracket_play_wins += 1
    game.loser.bracket_play_losses += 1
    game.save()
    return game


def simulate_four_team_bracket(tournament):
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
    game_one = Game(team_one=teams_in_bracket[0], team_two=teams_in_bracket[3],
                    tournament=tournament_bracket.tournament,
                    game_type='Semifinal')
    simulate_bracket_game(game_one)
    game_two = Game(team_one=teams_in_bracket[1], team_two=teams_in_bracket[2],
                    tournament=tournament_bracket.tournament,
                    game_type='Semifinal')
    simulate_bracket_game(game_two)
    game_three = Game(team_one=game_one.loser, team_two=game_two.loser, tournament=tournament_bracket.tournament,
                      game_type='Third-Place')
    simulate_bracket_game(game_three)
    game_four = Game(team_one=game_one.winner, team_two=game_two.winner, tournament=tournament_bracket.tournament,
                     game_type='Championship')
    simulate_bracket_game(game_four)
    tournament_bracket.champion = game_four.winner
    tournament_bracket.save()
    return tournament_bracket


def simulate_eight_team_bracket(tournament):
    tournament_pools = TournamentPool.objects.filter(tournament=tournament)
    teams_list = list(chain.from_iterable(pool.teams.all() for pool in tournament_pools))
    sorted_teams = sorted(
        teams_list,
        key=lambda team: (team.pool_play_wins, team.pool_play_point_differential),
        reverse=True
    )
    tournament_bracket = TournamentBracket.objects.create(tournament=tournament, number_of_teams=8,
                                                          bracket_type='Championship')
    tournament_bracket.teams.set(sorted_teams)
    tournament_bracket.save()
    for i, team in enumerate(sorted_teams, start=1):
        team.bracket_play_seed = i
        team.save()
    teams_in_bracket = tournament_bracket.teams.all()
    game_one = Game.objects.create(team_one=teams_in_bracket[0], team_two=teams_in_bracket[7], tournament=tournament,
                                   game_type='Quarterfinal')
    simulate_bracket_game(game_one)
    game_two = Game.objects.create(team_one=teams_in_bracket[1], team_two=teams_in_bracket[6], tournament=tournament,
                                   game_type='Quarterfinal')
    simulate_bracket_game(game_two)
    game_three = Game.objects.create(team_one=teams_in_bracket[2], team_two=teams_in_bracket[5], tournament=tournament,
                                     game_type='Quarterfinal')
    simulate_bracket_game(game_three)
    game_four = Game.objects.create(team_one=teams_in_bracket[3], team_two=teams_in_bracket[4], tournament=tournament,
                                    game_type='Quarterfinal')
    simulate_bracket_game(game_four)
    # Loser's Bracket
    game_five = Game.objects.create(team_one=game_one.loser, team_two=game_two.loser, tournament=tournament,
                                    game_type='Loser-Semifinal')
    simulate_bracket_game(game_five)
    game_six = Game.objects.create(team_one=game_three.loser, team_two=game_four.loser, tournament=tournament,
                                   game_type='Loser-Semifinal')
    simulate_bracket_game(game_six)
    game_seven = Game.objects.create(team_one=game_five.winner, team_two=game_six.winner, tournament=tournament,
                                     game_type='Fifth-Place-Final')
    simulate_bracket_game(game_seven)
    game_eight = Game.objects.create(team_one=game_five.loser, team_two=game_six.loser, tournament=tournament,
                                     game_type='Seventh-Place-Final')
    simulate_bracket_game(game_eight)
    # Winner's Bracket
    game_nine = Game.objects.create(team_one=game_one.winner, team_two=game_two.winner, tournament=tournament,
                                    game_type='Semifinal')
    simulate_bracket_game(game_nine)
    game_ten = Game.objects.create(team_one=game_three.winner, team_two=game_four.winner, tournament=tournament,
                                   game_type='Semifinal')
    simulate_bracket_game(game_ten)
    game_eleven = Game.objects.create(team_one=game_nine.loser, team_two=game_ten.loser, tournament=tournament,
                                      game_type='Third-Place')
    simulate_bracket_game(game_eleven)
    game_twelve = Game.objects.create(team_one=game_nine.winner, team_two=game_ten.winner, tournament=tournament,
                                      game_type='Championship')
    simulate_bracket_game(game_twelve)
    tournament_bracket.champion = game_twelve.winner
    tournament_bracket.save()
    return tournament_bracket


def simulate_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    number_of_teams = tournament.number_of_teams
    rank_teams_for_pool_play(tournament)
    simulate_four_team_pool(tournament)
    if number_of_teams == 4:
        tournament_bracket = simulate_four_team_bracket(tournament)
    elif number_of_teams == 8:
        tournament_bracket = simulate_eight_team_bracket(tournament)
    else:
        return render(request, 'tournaments/tournament_error.html')
    tournament.champion = tournament_bracket.champion.team
    tournament.is_complete = True
    tournament.save()
    return render(request, 'tournaments/tournament_results.html', {'tournament': tournament})


def tournament_results(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    return render(request, 'tournaments/tournament_results.html', {'tournament': tournament})
