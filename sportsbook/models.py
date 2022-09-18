from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

# Models
class User(AbstractUser):
    balance = models.FloatField(default=500)
    pending = models.FloatField(default=0)


class League(models.Model):
    league = models.CharField(max_length=3)

    def clean(self):
        if League.objects.exists() and not self.pk:
            raise ValidationError("League already exists.")

    def __str__(self):
        return f"{self.league}"
    

class Market(models.Model):
    market = models.CharField(max_length=32)

    def __str__(self):
        if self.market == "ml":
            return "Money Line"
        elif self.market == "spread":
            return "Spread"
        else:
            return f"{self.market}"


class Game(models.Model):
    api_id = models.CharField(max_length=128, default="no-id")
    league = models.ForeignKey(League, on_delete=models.CASCADE, blank=True, null=True, related_name="game_league")
    commence_time = models.DateTimeField(blank=True, null=True)
    home_team = models.CharField(max_length=64)
    away_team = models.CharField(max_length=64)
    home_ml = models.IntegerField(blank=True, null=True)
    away_ml = models.IntegerField(blank=True, null=True)
    home_price = models.IntegerField(blank=True, null=True)
    away_price = models.IntegerField(blank=True, null=True)
    home_point = models.FloatField(blank=True, null=True)
    away_point = models.FloatField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.away_team} at {self.home_team}"


class Bet(models.Model):
    bettor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bet")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game_bet")
    wager = models.FloatField(default=0)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, blank=True, null=True, related_name="market_bet")
    home_bet = models.BooleanField(default=True)
    status = models.CharField(max_length=8, default="Pending")
    profit = models.FloatField(blank=True, null=True)

    def __str__(self):
        if self.home_bet:
            return f"{self.wager} on {self.game.home_team} {self.market}"
        else:
            return f"{self.wager} on {self.game.away_team} {self.market}"


class Update(models.Model):
    update_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.update_time}"

    def clean(self):
        if Update.objects.exists() and not self.pk:
            raise ValidationError("Only one update time permitted.")