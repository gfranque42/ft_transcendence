from django.db import models
import json
from django.http import JsonResponse

# Create your models here.

# class	Player(models.Model):
# 	username = models.CharField(max_length=255)
# 	stanid = models.IntegerField(default=0)
# 	gamePlayed = models.IntegerField(default=0)
# 	gameWon = models.IntegerField(default=0)

# 	def	__str__(self):
# 		return (self.username)

class	Room(models.Model):
	url = models.CharField(max_length=255)
	difficulty = models.IntegerField(default=-1)
	players = models.TextField(default=[])
	maxPlayers = models.IntegerField(default=1)
	playerCount = models.IntegerField(default = 0)

	def __str__(self):
		return (self.url)

	def	getPlayers(self):
		return (json.loads(self.players))
	
	def	setPlayers(self, playersList):
		self.players = json.dumps(playersList)
		self.save()

	def addPlayer(self, player):
		playersList = self.getPlayers()
		if player not in playersList:
			playersList.append(player)
			self.setPlayers(playersList)

	def removePlayer(self, player):
		playersList = self.getPlayers()
		if player in playersList:
			playersList.remove(player)
			self.players = playersList
			self.save()

	# def playersCount(self):
	# 	self.playerCount = len(self.getPlayers())
	# 	self.save()
	# 	return self.playerCount
