from django.db import models

# Create your models here.

class Player(models.Model):
	identification = models.IntegerField()
	username = models.CharField(max_length=200)
	gamePlayed = models.IntegerField()
	gameWin = models.IntegerField()
	gameLoose = models.IntegerField()
