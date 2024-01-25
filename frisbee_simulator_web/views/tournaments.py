from django.contrib.auth.decorators import login_required
from django.db.models import F, Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from frisbee_simulator_web.models import Tournament, PlayerTournamentStat, TournamentTeam, Game, Point
from frisbee_simulator_web.forms import TournamentForm
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
        simulate_pool_play(request, tournamentSimulation, tournament_id, number_of_teams)
    elif tournament.pool_play_completed and not tournament.bracket_play_completed:
        simulate_bracket(request, tournamentSimulation, tournament_id, number_of_teams)
    return redirect(reverse('tournament_results', kwargs={'tournament_id': tournament_id}))


def simulate_pool_play(request, tournamentSimulation, tournament_id, number_of_teams):
    tournament = Tournament.objects.get(id=tournament_id)
    tournamentSimulation.rank_teams_for_pool_play()
    if number_of_teams == 4:
        tournamentSimulation.simulate_four_team_pool(request)
    elif number_of_teams == 8:
        tournamentSimulation.simulate_eight_team_pool(request)
    elif number_of_teams == 16:
        tournamentSimulation.simulate_sixteen_team_pool(request)
    else:
        return render(request, 'tournaments/tournament_error.html')
    tournament.pool_play_completed = True
    tournament.bracket_play_completed = False
    tournament.save()
    return redirect(reverse('tournament_results', kwargs={'tournament_id': tournament_id}))


def simulate_bracket(request, tournamentSimulation, tournament_id, number_of_teams):
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
