from django import forms
from .models import Player, Team
from .views.misc import calculate_player_rating


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['teams', 'seasons', 'overall']

    def save(self, commit=True):
        player = super().save(commit=False)
        player.overall = calculate_player_rating(player)
        if commit:
            player.save()
        return player


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
