from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_created")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    designer = models.CharField(max_length=200)
    year_released = models.IntegerField()
    num_players = models.IntegerField()
    estimated_playtime = models.IntegerField()
    age_recommendation = models.IntegerField()
    categories = models.ManyToManyField(
        "Category",
        through='GameCategory',
        related_name="games"
    )
