from django.db import models
from django.conf import settings

RESULT_CHOICES = [('win', 'Win'), ('loss', 'Loss'), ('draw', 'Draw')]

class GameRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='games')
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    ai_depth = models.IntegerField()
    elo_before = models.IntegerField()
    elo_after = models.IntegerField()
    pgn = models.TextField(blank=True)
    played_at = models.DateTimeField(auto_now_add=True)
    duration_s = models.IntegerField(default=0)

    class Meta:
        ordering = ['-played_at']

    def elo_change(self):
        return self.elo_after - self.elo_before

    def duration_display(self):
        m, s = divmod(self.duration_s, 60)
        return f"{m}m {s}s"

    def __str__(self):
        return f"{self.user.username} vs AI(d{self.ai_depth}) — {self.result}"
