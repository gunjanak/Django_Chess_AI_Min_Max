from django.contrib.auth.models import AbstractUser
from django.db import models

class ChessUser(AbstractUser):
    elo = models.IntegerField(default=1200)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)

    def win_rate(self):
        if self.games_played == 0:
            return 0
        return round((self.wins / self.games_played) * 100, 1)

    def __str__(self):
        return self.username
