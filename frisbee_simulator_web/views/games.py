from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse

from frisbee_simulator_web.forms import GameForm
from frisbee_simulator_web.models import Game, TournamentTeam, Tournament
from frisbee_simulator_web.views.simulate_game_functions import GameSimulation


@login_required(login_url='/login/')
def create_individual_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request=request)
        if form.is_valid():
            game = form.save(commit=False)
            game.created_by = request.user.profile
            game.save()

            # Assuming you want to create TournamentTeam instances for the selected teams
            # within a specific tournament. You might need to adjust this part based on your actual requirements.
            tournament, created = Tournament.objects.get_or_create(name='Fake Tournament')
            TournamentTeam.objects.create(team=game.t1, tournament=tournament, pool_play_seed=1,
                                          bracket_play_seed=1)
            TournamentTeam.objects.create(team=game.t2, tournament=tournament, pool_play_seed=2,
                                          bracket_play_seed=2)
            return redirect('games_list')
    else:
        form = GameForm(request=request)
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
