from django.shortcuts import render, redirect
from django.views.generic import CreateView
from frisbee_simulator_web.forms import TeamForm
from frisbee_simulator_web.models import Team
from frisbee_simulator_web.views.misc import create_random_player, calculate_player_rating, \
    generate_random_city, generate_random_mascot


class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/create_team.html'
    success_url = '/teams/list/'


def create_random_team(request):
    team = Team(
        location=generate_random_city(50),
        mascot=generate_random_mascot()
    )
    team.save()
    return team


def list_teams(request):
    teams = Team.objects.all()
    return render(request, 'teams/list_teams.html', {'teams': teams})