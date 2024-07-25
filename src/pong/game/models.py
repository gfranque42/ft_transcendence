from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class	Game(models.Model):
# 	name = models.CharField(max_length=255)
# 	difficulty = models.CharField(max_length=255)

# class	Room(models.Model):
# 	game = models.ForeignKey(Game, on_delete=models.CASCADE)
# 	name = models.CharField(max_length=255)
# 	max_player = models.IntegerField()
# 	players = models.ManyToManyField(User, blank=True)
# 	status = models.CharField(max_length=50, default='waiting')

# class	Player(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	current_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

# class	Leaderboard(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	game = models.ForeignKey(Game, on_delete=models.CASCADE)
# 	games_played = models.IntegerField(default=0)
# 	games_won = models.IntegerField(default=0)
# 	class	Meta:
# 		unique_together = ('user', 'game')
# 	def	__str__(self):
# 		return (f'{self.user.username} - {self.game.name}')

# --------------------------my new models--------------------------

# class	Player(models.Model):
# 	username = models.CharField(max_length=255)

# class	Game(models.Model):
# 	difficulty = models.IntegerField(default=-1)

# class	Vector(models.Model):
# 	x = models.IntegerField()
# 	y = models.IntegerField()

# class	Ball(models.Model):
# 	coor = models.ForeignKey(Vector, on_delete=models.CASCADE)
# 	size = models.ForeignKey(Vector, on_delete=models.CASCADE)
# 	dire = models.ForeignKey(Vector, on_delete=models.CASCADE)
# 	vel = models.ForeignKey(Vector, on_delete=models.CASCADE)
# 	ai = models.IntegerField()

# class	Paddle(models.Model):
# 	coor = models.ForeignKey(Vector, on_delete=models.CASCADE)
# 	size = models.ForeignKey(Vector, on_delete=models.CASCADE)

# class	Stats(models.Model):
# 	paddle_left = models.ForeignKey(Paddle, on_delete=models.CASCADE)
# 	paddle_right = models.ForeignKey(Paddle, on_delete=models.CASCADE)
# 	ball = models.ForeignKey(Ball, on_delete=models.CASCADE)
# 	score_left = models.IntegerField(default=0)
# 	score_right = models.IntegerField(default=0)

# class	Room(models.Model):
# 	name = models.CharField(max_length=255)
# 	party = models.ForeignKey(Game, on_delete=models.CASCADE)
# 	max_players = models.IntegerField()
# 	players = models.ManyToManyField(Player, blank=True)

class	Bob(models.Model):
	name = models.CharField(max_length=255)
	refreshtime = models.IntegerField(default = 0)
