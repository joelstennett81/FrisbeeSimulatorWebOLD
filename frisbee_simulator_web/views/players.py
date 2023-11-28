from django.shortcuts import render, redirect
from frisbee_simulator_web.forms import PlayerForm
from frisbee_simulator_web.models import Player
from frisbee_simulator_web.views.misc import create_random_player


def create_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_players')
    else:
        form = PlayerForm()
    return render(request, 'players/create_player.html', {'form': form})


def random_player(request):
    player = create_random_player(request)
    player.save()
    return redirect('list_players')


def list_players(request):
    players = Player.objects.all()
    return render(request, 'players/list_players.html', {'players': players})

