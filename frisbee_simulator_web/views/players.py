from django.shortcuts import render, redirect
from django.views.generic import CreateView

from frisbee_simulator_web.forms import PlayerForm
from frisbee_simulator_web.models import Player
from frisbee_simulator_web.views.misc import create_random_player


class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'players/create_player.html'
    success_url = '/players/list/'


def random_player(request):
    player = create_random_player(request)
    player.save()
    return redirect('list_players')


def list_players(request):
    players = Player.objects.all()
    return render(request, 'players/list_players.html', {'players': players})
