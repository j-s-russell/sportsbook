# Generated by Django 4.0.6 on 2022-09-04 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsbook', '0007_remove_game_line_game_away_point_game_away_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='away_ml',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='home_ml',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]