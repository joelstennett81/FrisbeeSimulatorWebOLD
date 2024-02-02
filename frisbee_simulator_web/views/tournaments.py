from itertools import count

from django.contrib.auth.decorators import login_required
from django.db.models import F, Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from frisbee_simulator_web.models import Tournament, PlayerTournamentStat, TournamentTeam, Game, Point
from frisbee_simulator_web.forms import TournamentForm
from frisbee_simulator_web.views.simulate_game_functions import GameSimulation
from frisbee_simulator_web.views.simulate_tournament_functions import TournamentSimulation
from frisbee_simulator_web.views.teams import create_random_team


class TournamentCreateView(CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournaments/create_tournament.html'
    success_url = '/tournaments/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_public = form.cleaned_data['is_public']
        self.object.created_by = self.request.user.profile

        # Check if teams were selected in the form
        teams = form.cleaned_data['teams']
        number_of_selected_teams = len(teams)

        # Subtract the number of selected teams from the total number of teams required for the tournament
        number_of_teams_to_create = int(form.cleaned_data['number_of_teams']) - number_of_selected_teams

        # Create the required number of random teams
        for _ in range(number_of_teams_to_create):
            team = create_random_team(self.request)
            team.is_public = form.cleaned_data['is_public']
            self.object.teams.add(team)

        # Add the selected teams to the tournament
        for team in teams:
            self.object.teams.add(team)

        self.object.save()
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)


class TournamentDeleteView(DeleteView):
    model = Tournament
    success_url = '/tournaments/'
    template_name = 'tournaments/tournament_confirm_delete.html'  # Replace with your template name


@login_required(login_url='/login/')
def list_tournaments(request, is_public=None):
    if is_public is None:
        tournaments = Tournament.objects.filter(created_by=request.user.profile)
    elif is_public:
        tournaments = Tournament.objects.filter(is_public=True).order_by('created_by')
    else:
        tournaments = Tournament.objects.filter(created_by=request.user.profile)
    return render(request, 'tournaments/list_tournaments.html', {'tournaments': tournaments})


def simulate_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournamentSimulation = TournamentSimulation(tournament)
    number_of_teams = tournament.number_of_teams
    if not tournament.pool_play_completed and not tournament.bracket_play_completed:
        return redirect(reverse('pool_play_overview', kwargs={'tournament_id': tournament_id}))
    elif tournament.pool_play_completed and not tournament.bracket_play_completed:
        return redirect(reverse('bracket_overview', kwargs={'tournament_id': tournament_id}))
    return redirect(reverse('tournament_results', kwargs={'tournament_id': tournament_id}))


def pool_play_overview(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournamentSimulation = TournamentSimulation(tournament=tournament)
    if not tournament.pool_play_initialized:
        tournamentSimulation.setup_pool_play_games_for_simulation(tournamentSimulation.numberOfTeams)
    return render(request, 'pool_play/pool_play_overview.html',
                  {'pool_play_games': tournament.pool_play_games, 'tournament': tournament})


def bracket_overview(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    if tournament.number_of_teams == 4:
        return render(request, 'bracket/four_team_bracket_overview.html', {'tournament': tournament})
    elif tournament.number_of_teams == 8:
        return render(request, 'bracket/eight_team_bracket_overview.html', {'tournament': tournament})
    elif tournament.number_of_teams == 16:
        return render(request, 'bracket/sixteen_team_bracket_overview.html', {'tournament': tournament})


def simulate_game(request, game_id, tournament_id):
    game = Game.objects.get(id=game_id)
    tournament = Tournament.objects.get(id=tournament_id)
    tournamentSimulation = TournamentSimulation(tournament=tournament)
    gameSimulation = GameSimulation(tournament, game)
    gameSimulation.coin_flip()
    gameSimulation.simulationType = game.tournament.simulation_type
    gameSimulation.simulate_full_game()
    tournamentSimulation.gameSimulationsList.append(gameSimulation)
    if gameSimulation.winner == gameSimulation.teamInGameSimulationOne:
        game.winner = gameSimulation.teamInGameSimulationOne.tournamentTeam
        game.loser = gameSimulation.teamInGameSimulationTwo.tournamentTeam
        point_differential = abs(
            gameSimulation.teamInGameSimulationOne.score - gameSimulation.teamInGameSimulationTwo.score)
    else:
        game.winner = gameSimulation.teamInGameSimulationTwo.tournamentTeam
        game.loser = gameSimulation.teamInGameSimulationOne.tournamentTeam
        point_differential = abs(
            gameSimulation.teamInGameSimulationTwo.score - gameSimulation.teamInGameSimulationOne.score)
    if game.game_type == 'Pool Play':
        TournamentTeam.objects.filter(pk=game.winner.pk).update(pool_play_wins=F('pool_play_wins') + 1,
                                                                pool_play_point_differential=F(
                                                                    'pool_play_point_differential') + point_differential)
        TournamentTeam.objects.filter(pk=game.loser.pk).update(pool_play_losses=F('pool_play_losses') + 1,
                                                               pool_play_point_differential=F(
                                                                   'pool_play_point_differential') - point_differential)
        tournamentSimulation.poolPlayGamesDoneSimulating += 1
        if tournamentSimulation.poolPlayGamesDoneSimulating == tournamentSimulation.poolPlayTotalGamesCount:
            tournament.pool_play_completed = True
            tournament.save()
    else:
        game.winner.bracket_play_wins += 1
        game.loser.bracket_play_losses += 1
    game.created_by = request.user.profile
    game.is_completed = True
    game.save()
    if game.game_type == 'Pool Play':
        return redirect(reverse('pool_play_overview', kwargs={'tournament_id': tournament_id}))
    else:
        return redirect(reverse('list_tournaments'))


def check_pool_play_simulation_status(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    incomplete_games = Game.objects.filter(tournament=tournament, game_type='Pool Play', is_completed=False)
    return JsonResponse({'simulations_complete': not incomplete_games.exists()})


def check_bracket_simulation_status(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    incomplete_games = Game.objects.filter(tournament=tournament, is_completed=False)
    return JsonResponse({'simulations_complete': not incomplete_games.exists()})


def fetch_latest_games_data(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    games = Game.objects.filter(tournament=tournament).values('id', 'is_completed', 'winner__team', 'loser__team',
                                                              'winner_score', 'loser_score', 'tournament_id')
    return JsonResponse({'games': list(games)})


def simulate_full_pool_play(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    for game in tournament.pool_play_games.all():
        if not game.is_completed:
            simulate_game(request, game.id, tournament.id)
    tournament.pool_play_completed = True
    tournament.save()
    return redirect(reverse('pool_play_results', kwargs={'tournament_id': tournament_id}))


def simulate_bracket(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournamentSimulation = TournamentSimulation(tournament)
    number_of_teams = tournament.number_of_teams
    if number_of_teams == 4:
        tournamentSimulation.simulate_four_team_bracket(request)
    elif number_of_teams == 8:
        tournamentSimulation.simulate_eight_team_winners_bracket(request, number_of_teams)
    elif number_of_teams == 16:
        tournamentSimulation.simulate_eight_team_winners_bracket(request, number_of_teams)
        tournamentSimulation.simulate_eight_team_losers_bracket(request)
    else:
        return render(request, 'tournaments/tournament_error.html')

    tournament.champion = tournamentSimulation.champion
    tournament.is_complete = True
    tournament.bracket_play_completed = True
    tournament.save()
    tournamentSimulation.save_tournament_player_stats_from_game_player_stats()
    return redirect(reverse('tournament_results', kwargs={'tournament_id': tournament_id}))


@login_required(login_url='/login/')
def game_results(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return JsonResponse(game)


@login_required(login_url='/login/')
def pool_play_results(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    number_of_teams = tournament.number_of_teams
    teams = TournamentTeam.objects.filter(tournament=tournament)
    teams_stats = []
    for team in teams:
        team_stats = {
            'team': team,
            'pool_play_wins': team.pool_play_wins,
            'pool_play_losses': team.pool_play_losses,
            'pool_play_point_differential': team.pool_play_point_differential
        }
        teams_stats.append(team_stats)
    top_assists = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('assists').desc())[:3]
    top_goals = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('goals').desc())[:3]
    top_throwaways = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('throwaways').desc())[:3]
    top_throwing_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('throwing_yards').desc())[:3]
    top_receiving_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('receiving_yards').desc())[:3]
    context = {'tournament': tournament, 'teams_stats': teams_stats, 'top_assists': top_assists,
               'top_goals': top_goals,
               'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
               'top_receiving_yards': top_receiving_yards}
    return render(request, 'tournaments/pool_play_results.html', context)


@login_required(login_url='/login/')
def tournament_results(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    number_of_teams = tournament.number_of_teams
    teams = TournamentTeam.objects.filter(tournament=tournament)
    teams_stats = []
    for team in teams:
        team_stats = {
            'team': team,
            'pool_play_wins': team.pool_play_wins,
            'pool_play_losses': team.pool_play_losses,
            'pool_play_point_differential': team.pool_play_point_differential
        }
        teams_stats.append(team_stats)
    top_assists = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('assists').desc())[:3]
    top_goals = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('goals').desc())[:3]
    top_throwaways = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('throwaways').desc())[:3]
    top_throwing_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('throwing_yards').desc())[:3]
    top_receiving_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('receiving_yards').desc())[:3]
    context = {'tournament': tournament, 'teams_stats': teams_stats, 'top_assists': top_assists,
               'top_goals': top_goals,
               'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
               'top_receiving_yards': top_receiving_yards}
    if tournament.pool_play_completed and not tournament.bracket_play_completed:
        return redirect(reverse('pool_play_results', kwargs={'tournament_id': tournament_id}))
    elif tournament.pool_play_completed and tournament.bracket_play_completed:
        if number_of_teams == 4:
            return render(request, 'tournaments/four_team_tournament_results.html', context)
        elif number_of_teams == 8:
            return render(request, 'tournaments/eight_team_tournament_results.html', context)
        elif number_of_teams == 16:
            return render(request, 'tournaments/eight_team_tournament_results.html', context)
        else:
            return render(request, 'tournaments/tournament_error.html')
    else:
        return render(request, 'tournaments/tournament_error.html')


@login_required(login_url='/login/')
def detail_tournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    return render(request, 'tournaments/detail_tournament.html', {'tournament': tournament})


@login_required(login_url='/login/')
def detail_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game = Game.objects.prefetch_related(Prefetch('game_points', queryset=Point.objects.order_by('id'))).get(pk=pk)
    return render(request, 'tournaments/detail_game.html', {'game': game})


@login_required(login_url='/login/')
def detail_point(request, pk):
    point = get_object_or_404(Point, pk=pk)
    return render(request, 'tournaments/detail_point.html', {'point': point})
