from django.db import models
from django.contrib.auth.models import User
from .game import Game

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_created")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="games_reviewed")
    content = models.CharField(max_length=500)
    rating = models.IntegerField()
