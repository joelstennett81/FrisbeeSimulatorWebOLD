from django.contrib import admin
from django.urls import path
from frisbee_simulator_web.views import players, teams

urlpatterns = [
    path('admin/', admin.site.urls),
    path('players/new/', players.create_player, name='create_player'),
    path('players/random/', players.random_player, name='random_player'),
    path('players/list/', players.list_players, name='list_players'),
    path('teams/new/', teams.create_team, name='create_team'),
    path('teams/random/', teams.create_team_of_random_players, name='random_team'),
    path('teams/list/', teams.list_teams, name='list_teams'),
]
