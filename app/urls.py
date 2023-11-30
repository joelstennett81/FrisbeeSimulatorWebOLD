from django.contrib import admin
from django.urls import path
from frisbee_simulator_web.views import players, teams, tournaments, home

urlpatterns = [
    path('', home.home, name='home'),
    path('admin/', admin.site.urls),
    path('players/new/', players.PlayerCreateView.as_view(), name='create_player'),
    path('players/random/', players.random_player, name='random_player'),
    path('players/list/', players.list_players, name='list_players'),
    path('teams/new/', teams.TeamCreateView.as_view(), name='create_team'),
    path('teams/random/', teams.create_random_team, name='random_team'),
    path('teams/list/', teams.list_teams, name='list_teams'),
    path('tournaments/new/', tournaments.TournamentCreateView.as_view(), name='create_tournament'),
    path('tournaments/list/', tournaments.list_tournaments, name='list_teams'),
    path('tournaments/simulate/<int:tournament_id>/', tournaments.simulate_tournament, name='simulate_tournament'),

]
