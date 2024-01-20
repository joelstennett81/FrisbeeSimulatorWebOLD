from django.contrib import admin
from django.urls import path
from frisbee_simulator_web.views import players, teams, tournaments, home, stats, users

urlpatterns = [
    path('', home.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', users.user_login, name='login'),
    path('register/', users.user_register, name='register'),
    path('profile/view/', users.ProfileDetailView.as_view(), name='view_profile'),
    path('profile/edit/', users.ProfileEditView.as_view(), name='edit_profile'),
    path('logout/', users.user_logout, name='logout'),
    path('players/new/', players.PlayerCreateView.as_view(), name='create_player'),
    path('players/', players.list_players, name='list_players'),
    path('players/public/', players.list_players, kwargs={'is_public': True}, name='list_public_players'),
    path('players/detail/<int:pk>/', players.detail_player, name='detail_player'),
    path('teams/new/', teams.TeamCreateView.as_view(), name='create_team'),
    path('teams/random/', teams.random_team, name='random_team'),
    path('teams/', teams.list_teams, name='list_teams'),
    path('teams/public/', teams.list_teams, kwargs={'is_public': True}, name='list_public_teams'),
    path('teams/detail/<int:pk>/', teams.detail_team, name='detail_team'),
    path('tournaments/new/', tournaments.TournamentCreateView.as_view(), name='create_tournament'),
    path('tournaments/', tournaments.list_tournaments, name='list_tournaments'),
    path('tournaments/public/', tournaments.list_tournaments, kwargs={'is_public': True}, name='list_public_tournaments'),
    path('tournaments/detail/<int:pk>/', tournaments.detail_tournament, name='detail_tournament'),
    path('tournaments/simulate/<int:tournament_id>/', tournaments.simulate_tournament, name='simulate_tournament'),
    path('tournaments/results/<int:tournament_id>/', tournaments.tournament_results, name='tournament_results'),
    path('stats/list_player_tournament_stats/<int:tournament_id>/', stats.list_player_tournament_stats,
         name='list_player_tournament_stats'),
    path('stats/detail_player_tournament_stats/<int:tournament_id>/<int:player_id>/',
         stats.detail_player_tournament_stats, name='detail_player_tournament_stats'),
]
