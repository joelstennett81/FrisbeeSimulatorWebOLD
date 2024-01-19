from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from frisbee_simulator_web.models import Tournament, PlayerTournamentStat
from frisbee_simulator_web.forms import TournamentForm
from frisbee_simulator_web.views.simulate_tournament_functions import TournamentSimulation
from frisbee_simulator_web.views.teams import create_random_team


class TournamentCreateView(CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournaments/create_tournament.html'
    success_url = '/tournaments/list/'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_public = form.cleaned_data['is_public']
        self.object.created_by = self.request.user

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


def list_tournaments(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournaments/list_tournaments.html', {'tournaments': tournaments})


def simulate_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    tournamentSimulation = TournamentSimulation(tournament)
    tournamentSimulation.simulate_tournament(request, tournament_id)
    return render(request, 'tournaments/tournament_results.html', {'tournament': tournament})


def tournament_results(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    top_assists = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('assists').desc())[:3]
    top_goals = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('goals').desc())[:3]
    top_throwaways = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(F('throwaways').desc())[:3]
    top_throwing_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('throwing_yards').desc())[:3]
    top_receiving_yards = PlayerTournamentStat.objects.filter(tournament=tournament).order_by(
        F('receiving_yards').desc())[:3]
    return render(request, 'tournaments/tournament_results.html',
                  {'tournament': tournament, 'top_assists': top_assists, 'top_goals': top_goals,
                   'top_throwaways': top_throwaways, 'top_throwing_yards': top_throwing_yards,
                   'top_receiving_yards': top_receiving_yards})


def detail_tournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    return render(request, 'tournaments/detail_tournament.html', {'tournament': tournament})
