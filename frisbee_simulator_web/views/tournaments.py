import random

from django.shortcuts import render
from django.views.generic.edit import CreateView
from frisbee_simulator_web.models import Tournament, TournamentTeam, Game, TournamentPool, TournamentBracket
from frisbee_simulator_web.forms import TournamentForm
from frisbee_simulator_web.views.teams import create_random_team


class TournamentCreateView(CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournaments/create_tournament.html'
    success_url = '/tournaments/list/'

    def form_valid(self, form):
        response = super().form_valid(form)
        number_of_teams = int(form.cleaned_data['number_of_teams'])
        selected_teams = form.cleaned_data['teams']
        selection_type = form.cleaned_data['selection_type']
        if selection_type == 'manual':
            if len(selected_teams) != number_of_teams:
                form.add_error('teams', 'You must select the exact number of teams as specified.')
                return self.form_invalid(form)
            for team in selected_teams:
                self.object.teams.add(team)
        else:
            for _ in range(number_of_teams):
                team = create_random_team(self.request)
                self.object.teams.add(team)
        self.object.save()
        assign_pool_seeds(self.object)
        simulate_pool_play_games_for_tournament(self.object)

        return response


def list_tournaments(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournaments/list_tournaments.html', {'tournaments': tournaments})


def assign_pool_seeds(tournament):
    teams = list(tournament.teams.all())
    teams.sort(key=lambda team: (-team.overall_rating, team.location))
    for i, team in enumerate(teams):
        team_tournament = TournamentTeam(team=team, tournament=tournament, seed=i + 1)
        team_tournament.save()


def simulate_pool_play_games_for_tournament(tournament):
    tournament_teams = TournamentTeam.objects.filter(tournament=tournament)
    number_of_tournament_teams = len(tournament_teams)
    if number_of_tournament_teams == 4:
        for i in range(number_of_tournament_teams):
            for j in range(i + 1, number_of_tournament_teams):
                game = Game(home_team=tournament_teams[i], away_team=tournament_teams[j], tournament=tournament,
                            game_type='Pool Play')
                game.save()
                simulate_pool_play_game(game)
                game.save()
    if number_of_tournament_teams == 8:
        pool1 = TournamentPool.objects.create(tournament=tournament)
        pool2 = TournamentPool.objects.create(tournament=tournament)
        for tournament_team in tournament_teams:
            if tournament_team.pool_play_seed in [1, 4, 5, 8]:
                pool1.teams.add(tournament_team.team)
            else:
                pool2.teams.add(tournament_team.team)
        for i in range(3):  # 3 rounds for 4 teams each
            for j in range(2):  # 2 matches per round
                game1 = Game(home_team=pool1.teams.all()[j], away_team=pool1.teams.all()[3 - j],
                             tournament=tournament, game_type='Pool Play')
                game2 = Game(home_team=pool2.teams.all()[j], away_team=pool2.teams.all()[3 - j],
                             tournament=tournament, game_type='Pool Play')
                game1.save()
                game2.save()
                simulate_pool_play_game(game1)
                simulate_pool_play_game(game2)
                game1.save()
                game2.save()


def simulate_pool_play_game(game):
    team_one = game.team_one
    team_two = game.team_two
    game.winner = team_one
    team_one.pool_play_wins += 1
    pool_play_point_differential = random.randint(1, 15)
    team_one.pool_play_point_differential = pool_play_point_differential
    game.loser = team_two
    team_two.pool_play_losses += 1
    team_two.pool_play_point_differential = pool_play_point_differential * -1
    game.save()
    team_one.save()
    team_two.save()


def create_four_team_bracket(tournament_pool):
    teams = tournament_pool.teams.all()
    sorted_teams = teams.order_by('-pool_play_wins')
    tournament_bracket = TournamentBracket(tournament=tournament_pool.tournament, number_of_teams=4, teams=sorted_teams,
                                           bracket_type='Championship')
    tournament_bracket.save()
    for i, team in enumerate(sorted_teams, start=1):
        team.bracket_play_seed = i
        team.save()
    teams_in_bracket = tournament_bracket.teams
    team_one = teams_in_bracket.objects.get(bracket_play_seed=1)
    team_two = teams_in_bracket.objects.get(bracket_play_seed=2)
    team_three = teams_in_bracket.objects.get(bracket_play_seed=3)
    team_four = teams_in_bracket.objects.get(bracket_play_seed=4)
    game_one = Game(team_one=team_one, team_two=team_four, tournament=tournament_bracket.tournament,
                    game_type='Semifinal')
    game_one.winner = team_one
    game_one.loser = team_two
    game_one.save()
    team_one.bracket_play_wins += 1
    team_four.bracket_play_losses += 1
    team_one.save()
    team_four.save()
    game_two = Game(team_one=team_two, team_two=team_three, tournament=tournament_bracket.tournament,
                    game_type='Semifinal')
    game_two.winner = team_two
    game_two.loser = team_three
    game_two.save()
    team_two.bracket_play_wins += 1
    team_three.bracket_play_losses += 1
    team_two.save()
    team_three.save()
    team_five = game_one.loser
    team_six = game_two.loser
    game_three = Game(team_one=team_five, team_two=team_six, tournament=tournament_bracket.tournament,
                      game_type='Third-Place')
    game_three.winner = team_five
    game_three.loser = team_six
    game_three.save()
    team_five.bracket_play_wins += 1
    team_six.bracket_play_losses += 1
    team_five.save()
    team_six.save()
    team_seven = game_one.winner
    team_eight = game_two.winner
    game_four = Game(team_one=team_seven, team_two=team_eight, tournament=tournament_bracket.tournament,
                     game_type='Championship')
    game_four.winner = team_seven
    game_four.loser = team_eight
    game_four.save()
    team_seven.bracket_play_wins += 1
    team_eight.bracket_play_losses += 1
    team_seven.save()
    team_eight.save()
    tournament_bracket.winner = team_seven
