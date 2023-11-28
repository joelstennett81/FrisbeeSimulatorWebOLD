from django.shortcuts import render, redirect
from frisbee_simulator_web.forms import TeamForm
from frisbee_simulator_web.models import Team, Player
from frisbee_simulator_web.views.misc import create_random_player, calculate_player_rating, \
    generate_random_city, generate_random_mascot


def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_teams')
    else:
        form = TeamForm()
    return render(request, 'teams/create_team.html', {'form': form})


def create_team_of_random_players(request):
    team = Team(
        location=generate_random_city(50),
        mascot=generate_random_mascot()
    )
    team.save()
    for _ in range(20):
        player = create_random_player(request)
        player.overall = calculate_player_rating(player)
        player.save()
        team.players.add(player)
        team.save()
    return redirect('list_teams')


def list_teams(request):
    teams = Team.objects.all()
    return render(request, 'teams/list_teams.html', {'teams': teams})