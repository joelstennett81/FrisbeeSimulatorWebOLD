from itertools import chain
from django.shortcuts import render
from django.views.generic.edit import CreateView
from frisbee_simulator_web.models import Tournament
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
        number_of_teams = int(form.cleaned_data['number_of_teams'])
        for _ in range(number_of_teams):
            team = create_random_team()
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
    tournament = Tournament.objects.get(id=tournament_id)
    return render(request, 'tournaments/tournament_results.html', {'tournament': tournament})
