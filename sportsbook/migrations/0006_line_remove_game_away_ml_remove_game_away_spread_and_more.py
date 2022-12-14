# Generated by Django 4.0.6 on 2022-09-04 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sportsbook', '0005_bet_pending_bet_won'),
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_price', models.IntegerField(blank=True, null=True)),
                ('away_price', models.IntegerField(blank=True, null=True)),
                ('home_point', models.FloatField(blank=True, null=True)),
                ('away_point', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='game',
            name='away_ml',
        ),
        migrations.RemoveField(
            model_name='game',
            name='away_spread',
        ),
        migrations.RemoveField(
            model_name='game',
            name='home_ml',
        ),
        migrations.RemoveField(
            model_name='game',
            name='home_spread',
        ),
        migrations.AddField(
            model_name='game',
            name='line',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_line', to='sportsbook.line'),
        ),
    ]
