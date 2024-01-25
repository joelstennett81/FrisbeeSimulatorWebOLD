from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Player, Team, Tournament, Profile
from .views.misc import calculate_overall_team_rating, calculate_overall_player_rating, calculate_handle_offense_rating, \
    calculate_handle_defense_rating, calculate_cutter_offense_rating, calculate_cutter_defense_rating, \
    create_random_player


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
        exclude = ['teams', 'seasons', 'overall_rating', 'overall_handle_offense_rating',
                   'overall_handle_defense_rating', 'overall_cutter_offense_rating', 'overall_cutter_defense_rating',
                   'created_by']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        player = super().save(commit=False)
        player.overall_rating = calculate_overall_player_rating(player)
        player.overall_handle_offense_rating = calculate_handle_offense_rating(player)
        player.overall_handle_defense_rating = calculate_handle_defense_rating(player)
        player.overall_cutter_offense_rating = calculate_cutter_offense_rating(player)
        player.overall_cutter_defense_rating = calculate_cutter_defense_rating(player)
        player.created_by = self.request.user.profile
        if commit:
            player.save()
        return player


class TeamForm(forms.ModelForm):
    o_line_players = forms.ModelMultipleChoiceField(queryset=Player.objects.none(), required=False)
    d_line_players = forms.ModelMultipleChoiceField(queryset=Player.objects.none(), required=False)
    bench_players = forms.ModelMultipleChoiceField(queryset=Player.objects.none(), required=False)

    class Meta:
        model = Team
        exclude = ['players', 'created_by', 'overall_rating']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['o_line_players'].queryset = Player.objects.filter(primary_line='OFFENSE',
                                                                       created_by=self.request.user.profile)
        self.fields['d_line_players'].queryset = Player.objects.filter(primary_line='DEFENSE',
                                                                       created_by=self.request.user.profile)
        self.fields['bench_players'].queryset = Player.objects.filter(primary_line='BENCH',
                                                                      created_by=self.request.user.profile)

    def clean(self):
        cleaned_data = super().clean()
        o_line_players = cleaned_data.get('o_line_players')
        d_line_players = cleaned_data.get('d_line_players')
        bench_players = cleaned_data.get('bench_players')
        if o_line_players and len(o_line_players) > 7:
            raise ValidationError("You cannot choose more than 7 O Line players")
        if d_line_players and len(d_line_players) > 7:
            raise ValidationError("You cannot choose more than 7 D line players")
        if bench_players and len(bench_players) > 7:
            raise ValidationError("You cannot choose more than 7 Bench players")

        return cleaned_data

    def save(self, commit=True):
        team = super().save(commit=False)
        team.created_by = self.request.user.profile

        if commit:
            team.save()
            o_line_players = list(self.cleaned_data['o_line_players'])
            d_line_players = list(self.cleaned_data['d_line_players'])
            bench_players = list(self.cleaned_data['bench_players'])

            # Calculate the number of players needed for each line
            o_line_needed = max(0, 7 - len(o_line_players))
            d_line_needed = max(0, 7 - len(d_line_players))
            bench_needed = max(0, 7 - len(bench_players))

            # Create random players for the lines that need them
            if o_line_needed > 0:
                o_line_players += [create_random_player(self.request, "OLINE") for _ in range(o_line_needed)]
            if d_line_needed > 0:
                d_line_players += [create_random_player(self.request, "DLINE") for _ in range(d_line_needed)]
            if bench_needed > 0:
                bench_players += [create_random_player(self.request, 'BENCH') for _ in range(bench_needed)]

            # Assign the players to the lines
            team.o_line_players.set(o_line_players)
            team.d_line_players.set(d_line_players)
            team.bench_players.set(bench_players)
            players = o_line_players + d_line_players + bench_players
            for player in players:
                player.is_public = team.is_public
            team.players.set(players)
            team.save()
            team.overall_rating = calculate_overall_team_rating(team)
            team.save()
        return team


class TournamentForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.none(),
                                           required=False)

    class Meta:
        model = Tournament
        fields = ['name', 'location', 'number_of_teams', 'simulation_type', 'is_public']
        exclude = ['created_by', 'pool_play_completed', 'bracket_play_completed']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['teams'].queryset = Team.objects.filter(created_by=self.request.user.profile)

    def save(self, commit=True):
        tournament = super().save(commit=False)
        tournament.created_by = self.request.user.profile

        if commit:
            tournament.save()
        return tournament
