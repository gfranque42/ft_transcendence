from django.db import models

# Create your models here.

class	Player(models.Model):
	username = models.CharField(max_length=255)
	gamePlay = models.IntegerField(default=0)
	gameWin = models.IntegerField(default=0)

	def	__str__(self):
		return (self.username)
