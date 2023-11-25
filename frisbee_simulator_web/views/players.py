from django.shortcuts import render, redirect
from frisbee_simulator_web.forms import PlayerForm
from frisbee_simulator_web.models import Player
import random


def create_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm()
    return render(request, 'players/create_player.html', {'form': form})


def random_player(request):
    player = Player(
        first_name='Random',
        last_name='Player',
        jersey_number=random.randint(0, 99),
        height=random.randint(60, 90),
        weight=random.randint(60, 90),
        speed=random.randint(60, 90),
        jumping=random.randint(60, 90),
        flick_distance=random.randint(60, 90),
        flick_accuracy=random.randint(60, 90),
        backhand_accuracy=random.randint(60, 90),
        backhand_distance=random.randint(60, 90),
        cutter_defense=random.randint(60, 90),
        handler_defense=random.randint(60, 90),
        agility=random.randint(60, 90),
        handle_cuts=random.randint(60, 90),
        under_cuts=random.randint(60, 90),
        deep_cuts=random.randint(60, 90),
        throw_ability=random.randint(60, 90),
        cut_ability=random.randint(60, 90)
    )
    player.overall = calculate_player_rating(player)
    player.save()
    return redirect('player_list')


def calculate_player_rating(player):
    rating_sum = (
                player.speed + player.jumping + player.flick_distance + player.flick_accuracy + player.backhand_accuracy + player.backhand_distance + player.cutter_defense +
                player.handler_defense + player.agility + player.handle_cuts + player.under_cuts + player.deep_cuts + player.throw_ability + player.throw_ability)
    overall_rating = rating_sum / 14
    return overall_rating
