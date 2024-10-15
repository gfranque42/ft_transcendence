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
		# try:
		# 	room = Room.objects.get(url="SbDaMcGf24")
		# except Room.DoesNotExist:
		# 	room = Room.objects.create(url="SbDaMcGf24", maxPlayers=2)
		self.rooms["SbDaMcGf24"] = room("SbDaMcGf24", 2, 5)
		self.rooms["SbDaMcGf24"].channelLayer = get_channel_layer()
		self.rooms["SbDaMcGf24"].roomGroupName = "pong_%s" % "SbDaMcGf24"
		print("mydict:",self.rooms,flush=True)
		


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
		self.paddleL: Paddle					= Paddle(Vec2(3, 32.5), Vec2(3, 35), 2.1, 0)
		self.paddleR: Paddle					= Paddle(Vec2(94, 32.5), Vec2(3, 35), 2.1, 0)
		self.ball: Ball							= Ball(Vec2(48, 48), Vec2(3, 3), 35, 2)
		self.scoreL: int						= 0
		self.scoreR: int						= 0
		self.players: List[str]					= []
		self.id: List[int]						= []
		self.ready: bool						= False
		self.inGame: bool						= False
		self.finish: bool						= False
		self.lock: threading.Lock				= Lock()
		self.thread: Optional[threading.Thread]	= None
		self.looser: str						= "/"
		self.urlwin: str						= "Next round"
		self.urlloose: str						= "/"
		self.buttonwin: str						= "Back to the menu"
		self.buttonloose: str					= "Back to the menu"
		if self.roomName == "SbDaMcGf24":
			self.buttonwin = "You won the tournament !"
			self.urlwin = "/"
		print(self.roomName,": Je suis initialisé !",flush=True)

	def	__repr__(self):
		return repr(self.roomName)

	@database_sync_to_async
	def	addPlayer(self, player: str, id: int) -> None:
		print(self.roomName,": I have to append ",player,flush=True)
		if self.partyType != 4 and self.roomName != "SbDaMcGf24":
			try:
				room = Room.objects.get(url=self.roomName)
			except Room.DoesNotExist:
				print("Room Does Not Exist: ", self.roomName, flush=True)
				return
			with self.lock:
				if player not in self.players:
					self.players.append(player)
					self.id.append(id)
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
					self.id.append(id)
				# else:
				# 	raise roomException(self.roomName+": Player " + player + " is already in this room!", 1001)
				if self.partyType == 4 and len(self.players) == 2:
					self.ready = True
				else:
					if len(self.players) == self.nbPlayers:
						self.ready = True

	@database_sync_to_async
	def	removePlayer(self, player: str, id: int) -> None:
		print(self.roomName,": I have to remove ",player," in partyType: ",self.partyType,flush=True)
		if self.partyType != 4 and self.roomName != "SbDaMcGf24":
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
					self.id.remove(id)
					print(type(room.players),flush=True)
					room.removePlayer(player)
					# room.save()
					room.playerCount = len(self.players)
					room.save()
					print(room.players,flush=True)
					print(room.playerCount,flush=True)
				# else:
				# 	raise roomException(self.roomName+": Player " + player + " isn't in this room!", 1002)

	@database_sync_to_async
	def	waitForTournament(self) -> None:
		gRoomsManager.rooms["SbDaMcGf24"].players.clear()
		gRoomsManager.rooms["SbDaMcGf24"].scoreL = 0
		gRoomsManager.rooms["SbDaMcGf24"].scoreR = 0
		gRoomsManager.rooms["SbDaMcGf24"].ready = False
		gRoomsManager.rooms["SbDaMcGf24"].inGame = False
		gRoomsManager.rooms["SbDaMcGf24"].finish = False
		gRoomsManager.rooms["SbDaMcGf24"].paddleL = Paddle(Vec2(3, 32.5), Vec2(3, 35), 2.1, 0)
		gRoomsManager.rooms["SbDaMcGf24"].paddleR = Paddle(Vec2(94, 32.5), Vec2(3, 35), 2.1, 0)
		gRoomsManager.rooms["SbDaMcGf24"].ball = Ball(Vec2(48, 48), Vec2(3, 3), 35, 2)
		room = Room.objects.filter(difficulty=5)
		i = 0
		groupName = []
		print("waitfortournament: gtournament players: ",gTournament.players,flush=True)
		for rom in room:
			if rom.url in gRoomsManager.rooms:
				groupName.append("pong_%s" % rom.url)
				print(groupName,rom.url,": ",rom.playerCount,flush=True)
				if rom.playerCount == 2 and gRoomsManager.rooms[rom.url].finish == False:
					i += 1
		if i == gTournament.players // 2:
			channelLayer = get_channel_layer()
			for gn in groupName:
				print(gn,": send",flush=True)
				async_to_sync(channelLayer.group_send)(gn, {"type": "gameUpdate", "message": "tournament start"})
				print(gn,": sent",flush=True)
			# gTournament.players //= 2
		self.buttonwin = "Next round"
		self.urlwin = "pong/SbDaMcGf24/"
		# if gTournament.players < 2:
		# 	self.buttonwin = "You win the tournament !"
		# 	self.urlwin = "/"

	def	endOfParty(self) -> None:
		print(self.roomName,": End of the party",flush=True)
		try:
			room = Room.objects.get(url=self.roomName)
			room.delete()
		except Room.DoesNotExist:
			print("Room Does Not Exist: ", self.roomName, flush=True)
			return

	async def	countDown(self) -> None:
		print(self.roomName,": countdown started",flush=True)
		await self.channelLayer.group_send(
						self.roomGroupName, {"type": "gameUpdate",
							"message": "matchmaking",
							"player1": self.players[0],
							"player2": self.players[1]})
		await asyncio.sleep(2)
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
			print(self.roomName,": scoreL = ",self.scoreL,", scoreR = ",self.scoreR, ", ball vel = ",self.ball.vel,flush=True)
			if self.scoreL == 3 or self.scoreR == 3:
				self.inGame = False
				self.finish = True
				if self.scoreL == 3:
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
		# if self.scoreL != 5 and self.scoreR != 5:
		# 	async_to_sync(self.channelLayer.group_send)(
		# 				self.roomGroupName, {"type": "quit", "message": "quit"})

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
							"player1Id": self.id[0],
							"player2Id": self.id[1],
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

class	tournament():
	def	__init__(self, players: int) -> None:
		self.maxplayers: int	= players
		self.players: int		= 0
		self.inTour: bool		= False

gRoomsManager: roomsManager = roomsManager()

gTournament: tournament = tournament(4)
