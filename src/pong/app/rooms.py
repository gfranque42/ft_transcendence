from typing import List, Optional
from threading import Thread, Lock
import threading
from .pong import *
from .consumers import *
from .models import Room
import asyncio
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from concurrent.futures import ThreadPoolExecutor
import time
import random
from channels.layers import get_channel_layer

class	roomException(Exception):
	def	__init__(self, message: str, errorCode: int) -> None:
		self.errorCode: int	= errorCode
		super().__init__(message)

class	tournament:
	def __init__(self) -> None:
		self.rooms = {}
		self.waiting: bool	= False
		self.inGame: bool	= False

	def	reset(self) -> None:
		self.waiting = False
		self.inGame = False

class	roomsManager:
	def	__init__(self):
		self.rooms = {}

#party types:
# 1 - 2 - 3 ai ? 
# 0 player vs player
# 4 player vs player in local

class	room():
	def	__init__(self, roomName: str, nbPlayers: int, partyType: int) -> None:
		self.roomName: str						= roomName
		self.channelLayer						= None
		self.roomGroupName						= None
		self.channelName						= None
		self.nbPlayers: int						= nbPlayers
		self.partyType: int						= partyType
		self.paddleL: Paddle					= Paddle(Vec2(3, 32.5), Vec2(3, 35), 1.5, 0)
		self.paddleR: Paddle					= Paddle(Vec2(94, 32.5), Vec2(3, 35), 1.5, 0)
		self.ball: Ball							= Ball(Vec2(48, 48), Vec2(4, 4), 225, 2)
		self.scoreL: int						= 0
		self.scoreR: int						= 0
		self.players: List[str]					= []
		self.ready: bool						= False
		self.inGame: bool						= False
		self.finish: bool						= False
		self.lock: threading.Lock				= Lock()
		self.thread: Optional[threading.Thread]	= None
		self.looser: str						= ""
		self.urlwin: str						= "/pong/"
		self.urlloose: str						= "/"
		self.buttonwin: str						= "Next round"
		self.buttonloose: str					= "Back to the menu"
		print(self.roomName,": Je suis initialisé !",flush=True)

	def	__repr__(self):
		return repr(self.roomName)

	@database_sync_to_async
	def	addPlayer(self, player: str) -> None:
		print(self.roomName,": I have to append ",player,flush=True)
		if self.partyType < 4:
			try:
				room = Room.objects.get(url=self.roomName)
			except Room.DoesNotExist:
				print("Room Does Not Exist: ", self.roomName, flush=True)
				return
			with self.lock:
				if player not in self.players:
					self.players.append(player)
					print("playercount",room.playerCount,flush=True)
					room.addPlayer(player)
					# room.playersCount()
					room.playerCount = len(self.players)
					room.save()
					print("playercount",room.playerCount,flush=True)
				else:
					print(self.roomName,": ",player," reconnect !")
					# raise roomException(self.roomName+": Player " + player + " is already in this room!", 1001)
				print(self.roomName,": Number of players: ",len(self.players), ",number of players requested: ",self.nbPlayers,flush=True)
				if len(self.players) == self.nbPlayers:
					self.ready = True
		else:
			with self.lock:
				if player not in self.players:
					self.players.append(player)
				else:
					raise roomException(self.roomName+": Player " + player + " is already in this room!", 1001)
				if self.partyType == 4 and len(self.players) == 2:
					self.ready = True
				else:
					if len(self.players) == self.nbPlayers:
						self.ready = True

	@database_sync_to_async
	def	removePlayer(self, player: str) -> None:
		print(self.roomName,": I have to remove ",player," in partyType: ",self.partyType,flush=True)
		if self.partyType < 4:
			try:
				room = Room.objects.get(url=self.roomName)
			except Room.DoesNotExist:
				print("Room Does Not Exist: ", self.roomName, flush=True)
				return
			with self.lock:
				if player in self.players:
					print(room.players,flush=True)
					print(room.playerCount,flush=True)
					self.players.remove(player)
					print(type(room.players),flush=True)
					room.removePlayer(player)
					# room.save()
					room.playerCount = len(self.players)
					room.save()
					print(room.players,flush=True)
					print(room.playerCount,flush=True)
				else:
					raise roomException(self.roomName+": Player " + player + " isn't in this room!", 1002)
		if self.partyType == 6 or self.partyType == 5:
			if player in self.players:
				self.players.remove(player)

	async def	countDown(self) -> None:
		print(self.roomName,": countdown started",flush=True)
		if self.ready == True and self.inGame == False:
			x: int = 3
			while x > 0:
				#send to the group with the channel layer
				await self.channelLayer.group_send(
						self.roomGroupName, {"type": "gameUpdate",
							"message": "countdown",
							"number": x,})
				await asyncio.sleep(1)
				# async_to_sync(asyncio.sleep(1))
				x -= 1
			#send the end of the count down
			await self.channelLayer.group_send(
						self.roomGroupName, {"type": "gameUpdate",
							"message": "fin du compte",})
		else:
			raise roomException("Room " + self.roomName + " haven't the good amount of players or is already in game", 1003)

	async def	start(self) -> None:
		try:
			print(self.roomName,": start on our way !",flush=True)
			self.thread = Thread(target=self.gameLoop, args=())
			print(self.roomName,": thread created",flush=True)
			self.thread.start()
			if self.thread:
				print(self.roomName,": thread launched !",flush=True)
				# self.thread.join()
		except roomException as e:
					print(f"Error from start: {e}")

	def	gameLoop(self) -> None:
		print(self.roomName,": gameLoop started !",flush=True)
		try:
			async_to_sync(self.countDown)()
			print(self.roomName,": countdown done !",flush=True)
			self.inGame = True
			print(self.roomName,": in game = ",self.inGame,flush=True)
		except Exception as e:
			print(self.roomName,": error: ",e,flush=True)
			async_to_sync(self.channelLayer.group_send)(
						self.roomGroupName, {"type": "quit", "message": "quit"})
			exit()
		message: str = "update"
		while self.inGame == True:
			# with self.lock:
			self.paddleL, self.paddleR, self.ball, self.scoreL, self.scoreR = gameUpdate(self.paddleL, self.paddleR, self.ball, self.scoreL, self.scoreR)
			print(self.roomName,": scoreL = ",self.scoreL,", scoreR = ",self.scoreR,flush=True)
			if self.scoreL == 5 or self.scoreR == 5:
				self.inGame = False
				self.finish = True
				if self.scoreL == 5:
					self.looser = self.players[1]
				else:
					self.looser = self.players[0]
				print(self.roomName,": looseeeeeerrrrrr: ",self.looser,flush=True)
				message = "finish"
				print(self.roomName,": the game is finished",flush=True)
			self.sendUpdate(message)
			print(self.roomName,": bobbbbbb paddleLdir=",self.paddleL.dir,"\npaddleLkey=",self.paddleL.dir,"\npaddleRdir=",self.paddleR.dir,"\npaddleRkey=",self.paddleR.vel,flush=True)
			async_to_sync(asyncio.sleep)(1/20)
			# time.sleep(1/20)
		if self.scoreL != 5 and self.scoreR != 5:
			async_to_sync(self.channelLayer.group_send)(
						self.roomGroupName, {"type": "quit", "message": "quit"})

	def	updateData(self, data, username: str) -> None:
		# with self.lock:
		print(self.roomName,": data receive for updateData",flush=True)
		print(self.roomName,": username: ",username,flush=True)
		print(self.roomName,": player0: ",self.players[0],flush=True)
		print(self.roomName,": player1: ",self.players[1],flush=True)
		if self.partyType == 4:
			if data['w'] == True:
				self.paddleL.key -= self.paddleL.vel
			if data['s'] == True:
				self.paddleL.key += self.paddleL.vel
			if data['up'] == True:
				self.paddleR.key -= self.paddleR.vel
			if data['down'] == True:
				self.paddleR.key += self.paddleR.vel
		elif self.partyType == 0 or self.partyType == 5:
			print("here I am",flush=True)
			if username == self.players[0]:
				print("rock you",flush=True)
				if data['w'] == True:
					self.paddleL.key -= self.paddleL.vel
				if data['s'] == True:
					self.paddleL.key += self.paddleL.vel
				if data['up'] == True:
					self.paddleL.key -= self.paddleL.vel
				if data['down'] == True:
					self.paddleL.key += self.paddleL.vel
			else:
				print("like a hurricane",flush=True)
				if data['w'] == True:
					self.paddleR.key -= self.paddleR.vel
				if data['s'] == True:
					self.paddleR.key += self.paddleR.vel
				if data['up'] == True:
					self.paddleR.key -= self.paddleR.vel
				if data['down'] == True:
					self.paddleR.key += self.paddleR.vel
		else:
			if data['w'] == True:
				self.paddleL.key -= self.paddleL.vel
			if data['s'] == True:
				self.paddleL.key += self.paddleL.vel
			if data['up'] == True:
				self.paddleL.key -= self.paddleL.vel
			if data['down'] == True:
				self.paddleL.key += self.paddleL.vel
		if self.paddleL.key > 0 and self.paddleL.key > self.paddleL.vel:
			self.paddleL.key = self.paddleL.vel
		elif self.paddleL.key < 0 and self.paddleL.key < -self.paddleL.vel:
			self.paddleL.key = -self.paddleL.vel
		if self.paddleR.key > 0 and self.paddleR.key > self.paddleR.vel:
			self.paddleR.key = self.paddleR.vel
		elif self.paddleR.key < 0 and self.paddleR.key < -self.paddleR.vel:
			self.paddleR.key = -self.paddleR.vel
		print(self.roomName,": fin de updateData!",flush=True)
		print(self.roomName,": paddleLdir=",self.paddleL.dir,"\npaddleLkey=",self.paddleL.dir,"\npaddleRdir=",self.paddleR.dir,"\npaddleRkey=",self.paddleR.vel,flush=True)

	def	sendUpdate(self, message) -> None:
		print(self.roomName,": sendUpdate with message \"",message,"\"",flush=True)
		async_to_sync(self.channelLayer.group_send)(
						self.roomGroupName, {"type": "gameUpdate", "message": message,
							"ballcx": self.ball.coor.x,
							"ballcy": self.ball.coor.y,
							"ballsx": self.ball.size.x,
							"ballsy": self.ball.size.y,
							"balldx": self.ball.dir.x,
							"balldy": self.ball.dir.y,
							"balla": self.ball.angle,
							"ballv": self.ball.vel,
							"paddleLcx": self.paddleL.coor.x,
							"paddleLcy": self.paddleL.coor.y,
							"paddleLsx": self.paddleL.size.x,
							"paddleLsy": self.paddleL.size.y,
							"paddleLd": self.paddleL.dir,
							"paddleLk": self.paddleL.key,
							"paddleLv": self.paddleL.vel,
							"paddleRcx": self.paddleR.coor.x,
							"paddleRcy": self.paddleR.coor.y,
							"paddleRsx": self.paddleR.size.x,
							"paddleRsy": self.paddleR.size.y,
							"paddleRd": self.paddleR.dir,
							"paddleRk": self.paddleR.key,
							"paddleRv": self.paddleR.vel,
							"player1Name": self.players[0],
							"player2Name": self.players[1],
							"scoreL": self.scoreL,
							"scoreR": self.scoreR,
							"username": "bob",
							"id": 0,
							"partyType": self.partyType,
							"buttonwin": self.buttonwin,
							"buttonloose": self.buttonloose,
							"urlwin": self.urlwin,
							"urlloose": self.urlloose
							})

def	randomUrl() -> str:
	url:str = ""
	while len(url) != 10:
		c:str = chr(random.randint(0, 127))
		if c.isalnum():
			url += c
	return url

class	tournament():
	def	__init__(self) -> None:
		self.lobbyRoom: room				= room(randomUrl(), 2, 6)
		# lroom = Room.objects.create(url=self.lobbyRoom.roomName,difficulty=6,maxPlayers=8)
		# lroom.save()
		self.rooms							= {}
		self.players: List[str]				= []
		self.thread: Optional[threading.Thread]	= None
		self.inTour: bool					= False
		self.consumer: PongConsumer			= None

	def	shufflePlayers(self) -> None:
		playerPlaces = []
		newPlaces = []
		for player in self.players:
			playerPlaces.append(player)
		while len(newPlaces) < len(self.players):
			i = random.randint(0, len(self.players) - 1)
			if i not in newPlaces:
				newPlaces.append(i)
		self.players = [playerPlaces[i] for i in newPlaces]
		print (self.players)

	def	checkRoom(self) -> int:
		for key in self.rooms:
			if self.rooms[key].inGame == False:
				return 0
		return 1

	async def	sendRooms(self) -> None:
		print("don't forget to bring a towel !",flush=True)
		infos = {'type': 'tournamentRedirect', 'message': 'tournament'}
		infos['numberOfRooms'] = int(len(self.players) / 2)
		i = 0
		for key in self.rooms:
			print("key: ",key,flush=True)
			roomName = "Room"+str(i)
			infos[roomName] = key
			roomNamep1 = roomName+str(1)
			infos[roomNamep1] = self.players[i * 2]
			roomNamep1 = roomName+str(2)
			infos[roomNamep1] = self.players[i * 2 + 1]
			i += 1
		print("infos de sendRooms: ",infos,flush=True)
		try:
			print("channelLayer: ",self.lobbyRoom.channelLayer,", roomgroupname: ",self.lobbyRoom.roomGroupName,flush=True)
			await self.consumer.channel_layer.group_send(self.consumer.room_group_name, infos)
			print("send_group ok!",flush=True)
		except Exception as e:
			print("error with group_send: ",e,flush=True)

	def	start(self) -> None:
		print(self.lobbyRoom.roomName,": from start, thread in comming",flush=True)
		self.thread = Thread(target=self.routine, args=())
		self.inTour = True
		self.players = self.lobbyRoom.players
		self.thread.start()
		if self.thread:
			self.thread.join()

	def	routine(self) -> None:
		print(self.lobbyRoom.roomName,": bisous de la routine",flush=True)
		print(self.lobbyRoom.roomName,": liste des joueurs: ",self.players,flush=True)
		while len(self.players) > 1:
			print(self.lobbyRoom.roomName,": liste des joueurs: ",self.players,flush=True)
			self.shufflePlayers()
			print(self.lobbyRoom.roomName,": liste des joueurs: ",self.players,flush=True)
			i = 0
			while i < (len(self.players) / 2):
				url = randomUrl()
				self.rooms[url] = room(url,2,5)
				self.rooms[url].urlwin += self.lobbyRoom.roomName+"/"
				i += 1
			async_to_sync(self.sendRooms)()
			for key in self.rooms:
				if self.rooms[key].thread:
					print(self.lobbyRoom.roomName,": je join la room ",self.rooms[key].roomName,flush=True)
					self.rooms[key].thread.join()
			for key in self.rooms:
				self.players.remove(self.rooms[key].looser)
			self.lobbyRoom.players.clear()
			self.lobbyRoom.nbPlayers = len(self.players)
		self.inTour = False
		self.rooms.clear()
		self.lobbyRoom.players.clear()

