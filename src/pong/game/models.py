from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class	Game(models.Model):
	name = models.CharField(max_length=255)
	difficulty = models.CharField(max_length=255)

class	Room(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	max_player = models.IntegerField()
	players = models.ManyToManyField(User, blank=True)
	status = models.CharField(max_length=50, default='waiting')

class	Player(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	current_room = models.ForeignKey(Room, on_delete=models.set_NULL, null=True, blank=True)

class	Leaderboard(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	games_played = models.IntegerField(default=0)
	games_won = models.IntegerField(default=0)
	class	Meta:
		unique_together = ('user', 'game')
	def	__str__(self):
		return (f'{self.user.username} - {self.game.name}')
