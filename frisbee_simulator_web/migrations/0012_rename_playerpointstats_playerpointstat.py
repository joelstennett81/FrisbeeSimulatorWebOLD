# Generated by Django 4.2.7 on 2023-12-14 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frisbee_simulator_web', '0011_point_point_number_in_game'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlayerPointStats',
            new_name='PlayerPointStat',
        ),
    ]