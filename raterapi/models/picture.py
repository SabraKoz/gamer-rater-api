from django.db import models
from django.contrib.auth.models import User
from .game import Game

class Picture(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
