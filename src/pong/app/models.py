from django.db import models

# Create your models here.

class	Player(models.Model):
	username = models.CharField(max_length=255)
	gamePlayed = models.IntegerField(default=0)
	gameWon = models.IntegerField(default=0)

	def	__str__(self):
		return (self.username)

class	Room(models.Model):
	url = models.CharField(max_length=255)
	difficulty = models.IntegerField(default=-1)
	players = models.ManyToManyField(Player, blank=True)
	# stats = models.ForeignKey(Game, blank=True, null=True, on_delete=models.CASCADE)
	maxPlayers = models.IntegerField(default=1) 

	def __str__(self):
		return (self.url)

