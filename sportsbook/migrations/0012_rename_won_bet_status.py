# Generated by Django 4.0.6 on 2022-09-05 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsbook', '0011_remove_bet_pending_bet_profit_alter_bet_won'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bet',
            old_name='won',
            new_name='status',
        ),
    ]
