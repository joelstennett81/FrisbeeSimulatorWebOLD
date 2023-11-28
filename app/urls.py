from django.contrib import admin
from django.urls import path
from frisbee_simulator_web.views import players

urlpatterns = [
    path('admin/', admin.site.urls),
    path('players/new/', players.create_player, name='create_player'),
    path('players/random/', players.random_player, name='random_player'),
    path('players/list/', players.list_players, name='list_players'),
]
