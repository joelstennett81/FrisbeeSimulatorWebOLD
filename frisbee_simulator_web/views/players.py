from django.shortcuts import render, redirect, get_object_or_404
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
    player = create_random_player()
    player.save()
    return redirect('list_players')


def list_players(request):
    players = Player.objects.all()
    return render(request, 'players/list_players.html', {'players': players})


def detail_player(request, pk):
   player = get_object_or_404(Player, pk=pk)
   return render(request, 'players/detail_player.html', {'player': player})