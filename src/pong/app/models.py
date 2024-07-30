from django.db import models

# Create your models here.

class	Player(models.Model):
	username = models.CharField(max_length=255)
	gamePlay = models.IntegerField(default=0)
	gameWin = models.IntegerField(default=0)

	def	__str__(self):
		return (self.username)

class	Game(models.Model):
	scoreLeft = models.IntegerField(default=0)
	scoreRight = models.IntegerField(default=0)

class	Room(models.Model):
	url = models.CharField(max_length=255)
	difficulty = models.IntegerField(default=-1)
	players = models.ManyToManyField(Player, blank=True)
	stats = models.ForeignKey(Game, blank=True, null=True, on_delete=models.CASCADE)
	maxPlayers = models.IntegerField(default=1) 

	# def save(self, *args, **kwargs):
	# 	if not self.stats_id:
	# 		self.stats = Game.objects.first()
	# 	super(Room, self).save(*args, **kwargs)

	def __str__(self):
		return (self.url)

