from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse

from frisbee_simulator_web.forms import GameForm
from frisbee_simulator_web.models import Game, TournamentTeam
from frisbee_simulator_web.views.simulate_game_functions import GameSimulation


@login_required(login_url='/login/')
def create_individual_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            # Set the created_by field to the current user's profile
            form.instance.created_by = request.user.profile
            form.save()
            return redirect('games_list') # Redirect to a page that lists all games
    else:
        form = GameForm()
    return render(request, 'games/create_individual_game.html', {'form': form})


def simulate_individual_game(request, game_id):
    game = Game.objects.get(id=game_id)
    gameSimulation = GameSimulation(tournament=None, game=game)
    gameSimulation.coin_flip()
    gameSimulation.simulate_full_game()
    if gameSimulation.winner == gameSimulation.teamInGameSimulationOne:
        game.winner = gameSimulation.teamInGameSimulationOne.tournamentTeam
        game.loser = gameSimulation.teamInGameSimulationTwo.tournamentTeam
        point_differential = abs(
            gameSimulation.teamInGameSimulationOne.score - gameSimulation.teamInGameSimulationTwo.score)
    else:
        game.winner = gameSimulation.teamInGameSimulationTwo.tournamentTeam
        game.loser = gameSimulation.teamInGameSimulationOne.tournamentTeam
        point_differential = abs(
            gameSimulation.teamInGameSimulationTwo.score - gameSimulation.teamInGameSimulationOne.score)
    if game.game_type == 'Pool Play':
        TournamentTeam.objects.filter(pk=game.winner.pk).update(pool_play_wins=F('pool_play_wins') + 1,
                                                                pool_play_point_differential=F(
                                                                    'pool_play_point_differential') + point_differential)
        TournamentTeam.objects.filter(pk=game.loser.pk).update(pool_play_losses=F('pool_play_losses') + 1,
                                                               pool_play_point_differential=F(
                                                                   'pool_play_point_differential') - point_differential)
    else:
        game.winner.bracket_play_wins += 1
        game.loser.bracket_play_losses += 1
    game.created_by = request.user.profile
    game.is_completed = True
    game.save()
    return redirect(reverse('detail_game', kwargs={'pk': game.id}))


@login_required(login_url='/login/')
def games_list(request):
    games = Game.objects.filter(game_type='Exhibition', created_by=request.user.profile)
    return render(request, 'games/games_list.html', {'games': games})
