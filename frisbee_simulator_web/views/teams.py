from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from frisbee_simulator_web.forms import TeamForm
from frisbee_simulator_web.models import Team
from frisbee_simulator_web.views.misc import create_random_player, generate_random_city, generate_random_mascot, \
    calculate_overall_team_rating


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
    players = [create_random_player(request) for _ in range(21)]
    for player in players:
        player.is_public = team.is_public
    team.players.set(players)
    team.o_line_players.set([player.id for player in players[:7]])
    team.d_line_players.set([player.id for player in players[7:14]])
    team.bench_players.set([player.id for player in players[14:]])
    team.created_by = request.user
    team.save()
    team.overall_rating = calculate_overall_team_rating(team)
    team.save()
    return team


def list_teams(request):
    teams = Team.objects.all()
    return render(request, 'teams/list_teams.html', {'teams': teams})


def detail_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'teams/detail_team.html', {'team': team})
