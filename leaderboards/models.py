from django.db import models
from django.conf import settings

class HighScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game_key = models.CharField(max_length=50)
    score = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game_key"],
                name="unique_high_score_per_user_game",
            ),
        ]
        indexes = [
            models.Index(fields=["game_key", "-score", "id"]),
        ]

    @classmethod
    def record_score(cls, user, game_key, score, *, higher_is_better = True):
        best, created = cls.objects.get_or_create(
            user = user,
            game_key = game_key,
            defaults={"score":score},
        )

        if created:
            return True

        saved_score = cls.objects.filter(pk=best.pk)

        if higher_is_better:
            saved_score = saved_score.filter(score__lt=score)   #to determine when to save based on lower score better or higher score better
        else:
            saved_score = saved_score.filter(score__gt=score)   

        return saved_score.update(score=score) == 1