# Generated by Django 4.0.6 on 2022-09-04 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsbook', '0006_line_remove_game_away_ml_remove_game_away_spread_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='line',
        ),
        migrations.AddField(
            model_name='game',
            name='away_point',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='away_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='home_point',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='home_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Line',
        ),
    ]
