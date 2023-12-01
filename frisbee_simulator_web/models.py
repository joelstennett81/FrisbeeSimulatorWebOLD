from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    jersey_number = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
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
    overall_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    teams = models.ManyToManyField('Team', related_name='teams_players')
    seasons = models.ManyToManyField('Season', related_name='seasons_players')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Team(models.Model):
    location = models.CharField(max_length=50)
    mascot = models.CharField(max_length=50)
    players = models.ManyToManyField(Player, related_name='players_teams')
    overall_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    o_line_players = models.ManyToManyField(Player, related_name='o_line_players_teams')
    d_line_players = models.ManyToManyField(Player, related_name='d_line_players_teams')
    bench_players = models.ManyToManyField(Player, related_name='bench_players_teams')


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
    NUMBER_OF_TEAMS_CHOICES = [
        (4, '4'),
        (8, '8'),
        (16, '16'),
        (20, '20'),
        (32, '32'),
    ]
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    number_of_teams = models.PositiveIntegerField(choices=NUMBER_OF_TEAMS_CHOICES, default=4)
    teams = models.ManyToManyField(Team, related_name='teams_tournaments')
    champion = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    is_complete = models.BooleanField(default=False)


class TournamentPool(models.Model):
    POOL_SIZE_CHOICES = [
        (4, '4'),
        (5, '5'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    teams = models.ManyToManyField('TournamentTeam', related_name='teams_pools')
    number_of_teams = models.PositiveIntegerField(choices=POOL_SIZE_CHOICES, default=4)


class TournamentBracket(models.Model):
    BRACKET_SIZE_CHOICES = [
        (4, '4'),
        (8, '8'),
        (12, '12')
    ]
    BRACKET_TYPE_CHOICES = [
        ('Championship', 'Championship'),
        ('Loser', 'Loser'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    teams = models.ManyToManyField('TournamentTeam', related_name='teams_brackets')
    number_of_teams = models.PositiveIntegerField(choices=BRACKET_SIZE_CHOICES, default=4)
    bracket_type = models.CharField(max_length=50, choices=BRACKET_TYPE_CHOICES)
    champion = models.ForeignKey('TournamentTeam', on_delete=models.CASCADE, null=True)


class TournamentTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    pool_play_seed = models.PositiveIntegerField()
    bracket_play_seed = models.PositiveIntegerField(blank=True)
    pool = models.ForeignKey(TournamentPool, on_delete=models.CASCADE,null=True)
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE, null=True)
    pool_play_wins = models.PositiveIntegerField(default=0)
    pool_play_losses = models.PositiveIntegerField(default=0)
    pool_play_point_differential = models.IntegerField(default=0)
    bracket_play_wins = models.PositiveIntegerField(default=0)
    bracket_play_losses = models.PositiveIntegerField(default=0)


class Game(models.Model):
    GAME_TYPE_CHOICES = [
        ('Pool Play', 'Pool Play'),
        ('Pre-Quarterfinal', 'Pre-Quarterfinal'),
        ('Quarterfinal', 'Quarterfinal'),
        ('Loser-Semifinal', 'Loser-Semifinal'),
        ('Semifinal', 'Semifinal'),
        ('Championship', 'Championship'),
        ('Third-Place-Final', 'Third-Place-Final'),
        ('Fifth-Place-Final', 'Fifth-Place-Final'),
        ('Seventh-Place-Final', 'Seventh-Place-Final')
    ]
    date = models.DateTimeField(default=timezone.now)
    team_one = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='team_one_games')
    team_two = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='team_two_games')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='games')
    game_type = models.CharField(max_length=50, choices=GAME_TYPE_CHOICES)
    winner = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='winner_games', null=True)
    loser = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE, related_name='loser_games', null=True)


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
