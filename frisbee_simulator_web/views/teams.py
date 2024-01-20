from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required(login_url='/login/')
def random_team(request):
    team = create_random_team(request)
    team.save()
    return redirect('list_teams')


def create_random_team(request):
    team = Team(
        location=generate_random_city(50),
        mascot=generate_random_mascot()
    )
    team.save()
    o_line_players = [create_random_player(request, "OLINE") for _ in range(7)]
    d_line_players = [create_random_player(request, "DLINE") for _ in range(7)]
    bench_players = [create_random_player(request, "BENCH") for _ in range(7)]
    players = o_line_players + d_line_players + bench_players
    for player in players:
        player.is_public = team.is_public
    team.players.set(players)
    team.o_line_players.set(o_line_players)
    team.d_line_players.set(d_line_players)
    team.bench_players.set(bench_players)
    team.created_by = request.user.profile
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
