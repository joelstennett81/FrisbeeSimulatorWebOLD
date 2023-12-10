from django import forms
from .models import Player, Team, Tournament
from .views.misc import calculate_player_rating, calculate_team_rating


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['teams', 'seasons', 'overall']

    def save(self, commit=True):
        player = super().save(commit=False)
        player.overall_rating = calculate_player_rating(player)
        if commit:
            player.save()
        return player


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['players', 'o_line_players', 'd_line_players', 'bench_players']

    def save(self, commit=True):
        team = super().save(commit=False)
        team.overall_rating = calculate_team_rating(team)
        if commit:
            team.save()
        return team


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'location', 'number_of_teams', 'simulation_type']
