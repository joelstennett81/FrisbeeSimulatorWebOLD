from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    jersey_number = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    overall = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    height = models.PositiveIntegerField(validators=[MinValueValidator(48), MaxValueValidator(90)])  # In inches
    weight = models.PositiveIntegerField(validators=[MinValueValidator(50), MaxValueValidator(450)])  # In pounds
    speed = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    jumping = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    flick_distance = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    flick_accuracy = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    backhand_accuracy = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    backhand_distance = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    cutter_defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    handler_defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    agility = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    handle_cuts = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])  # Not sure how to use it
    under_cuts = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])  # Under and deep cuts determine cut ability
    deep_cuts = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    throw_ability = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    cut_ability = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    teams = models.ManyToManyField('Team', related_name='teams_players')
    seasons = models.ManyToManyField('Season', related_name='seasons_players')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Team(models.Model):
    location = models.CharField(max_length=50)
    mascot = models.CharField(max_length=50)
    players = models.ManyToManyField(Player, related_name='players_teams')


class Season(models.Model):
    SEASON_TYPE_CHOICES = [
        ('College Fall', 'College Fall'),
        ('College Spring', 'College Spring'),
        ('Club', 'Club'),
        ('AUDL', 'AUDL'),
        ('PUL', 'PUL')
    ]
    season_type = models.CharField(max_length=50, choices=SEASON_TYPE_CHOICES)
    year = models.IntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2100)])
    teams = models.ManyToManyField(Team, related_name='teams_seasons')
    players = models.ManyToManyField(Player, related_name='players_seasons')


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team, related_name='teams_tournaments')


class Game(models.Model):
    GAME_TYPE_CHOICES = [
        ('Pool Play', 'Pool Play'),
        ('Pre-Quarterfinal', 'Pre-Quarterfinal'),
        ('Quarterfinal', 'Quarterfinal'),
        ('Semifinal', 'Semifinal'),
        ('Championship', 'Championship'),
    ]
    date = models.DateTimeField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='games')
    game_type = models.CharField(max_length=50, choices=GAME_TYPE_CHOICES)


class PlayerGameStat(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='player_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='game_stats')
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    passes_thrown = models.PositiveIntegerField(default=0)
    passes_completed = models.PositiveIntegerField(default=0)
    hucks_thrown = models.PositiveIntegerField(default=0)
    hucks_completed = models.PositiveIntegerField(default=0)
    throwing_yards = models.PositiveIntegerField(default=0)
    receiving_yards = models.PositiveIntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)
    pulls = models.PositiveIntegerField(default=0)


class PlayerTournamentStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='tournament_stats')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='player_stats')
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    passes_thrown = models.PositiveIntegerField(default=0)
    passes_completed = models.PositiveIntegerField(default=0)
    hucks_thrown = models.PositiveIntegerField(default=0)
    hucks_completed = models.PositiveIntegerField(default=0)
    throwing_yards = models.PositiveIntegerField(default=0)
    receiving_yards = models.PositiveIntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)
    pulls = models.PositiveIntegerField(default=0)

class PlayerSeasonStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='season_stats')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='player_stats')


class TeamGameStat(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='team_stats')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='game_stats')
    goals_scored = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    passes_thrown = models.PositiveIntegerField(default=0)
    passes_completed = models.PositiveIntegerField(default=0)
    hucks_thrown = models.PositiveIntegerField(default=0)
    hucks_completed = models.PositiveIntegerField(default=0)
    total_throwing_yards = models.PositiveIntegerField(default=0)
    total_receiving_yards = models.PositiveIntegerField(default=0)
    turnovers = models.PositiveIntegerField(default=0)


class TeamTournamentStat(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tournament_stats')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='team_stats')
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    passing_yards_for = models.PositiveIntegerField(default=0)
    passing_yards_against = models.PositiveIntegerField(default=0)
    throwaways = models.PositiveIntegerField(default=0)
    drops = models.PositiveIntegerField(default=0)
    turnovers_forced = models.PositiveIntegerField(default=0)
    passes_thrown = models.PositiveIntegerField(default=0)
    passes_completed = models.PositiveIntegerField(default=0)
    hucks_thrown = models.PositiveIntegerField(default=0)
    hucks_completed = models.PositiveIntegerField(default=0)
    callahans = models.PositiveIntegerField(default=0)

class TeamSeasonStat(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='season_stats')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='team_season_stats')
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()





