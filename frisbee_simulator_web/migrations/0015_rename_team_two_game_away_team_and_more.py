# Generated by Django 4.2.7 on 2024-01-15 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frisbee_simulator_web', '0014_alter_playergamestat_tournament_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='team_two',
            new_name='away_team',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='team_one',
            new_name='home_team',
        ),
    ]