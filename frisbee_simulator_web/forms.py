from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Player, Team, Tournament, Profile
from .views.misc import calculate_overall_team_rating, calculate_overall_player_rating, calculate_handle_offense_rating, \
    calculate_handle_defense_rating, calculate_cutter_offense_rating, calculate_cutter_defense_rating


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'date_of_birth']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['teams', 'seasons', 'overall', 'created_by']

    def save(self, commit=True):
        player = super().save(commit=False)
        player.overall_rating = calculate_overall_player_rating(player)
        player.overall_handle_offense_rating = calculate_handle_offense_rating(player)
        player.overall_handle_defense_rating = calculate_handle_defense_rating(player)
        player.overall_cutter_offense_rating = calculate_cutter_offense_rating(player)
        player.overall_cutter_defense_rating = calculate_cutter_defense_rating(player)
        if commit:
            player.save()
        return player


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['players', 'o_line_players', 'd_line_players', 'bench_players', 'created_by']

    def save(self, commit=True):
        team = super().save(commit=False)
        team.overall_rating = calculate_overall_team_rating(team)
        if commit:
            team.save()
        return team


class TournamentForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), required=False)

    class Meta:
        model = Tournament
        fields = ['name', 'location', 'number_of_teams', 'simulation_type', 'is_public']
        exclude = ['created_by']

    def save(self, commit=True):
        tournament = super().save(commit=False)
        if commit:
            tournament.save()
        return tournament
