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
        exclude = ['players']

    def save(self, commit=True):
        team = super().save(commit=False)
        team.overall_rating = calculate_team_rating(team)
        if commit:
            team.save()
        return team


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'location', 'number_of_teams', 'teams']

    def __init__(self, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        self.fields['teams'] = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), required=False)
        self.fields['selection_type'] = forms.CharField(widget=forms.HiddenInput())
