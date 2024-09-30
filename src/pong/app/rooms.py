from typing import List, Optional
from threading import Thread
import threading
from .pong import *
from .models import Room, Player
import asyncio
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async

class	roomException(Exception):
	def	__init__(self, message: str, errorCode: int) -> None:
		self.errorCode: int	= errorCode
		super().__init__(message)

class	roomsManager:
	def	__init__(self):
		self.rooms = {}
	
	def	__setitem__(self, key, value):
		self.rooms[key] = value

	def	__getitem__(self, key):
		return self.rooms[key]

	def	__contains__(self, key):
		return key in self.rooms

	def	__len__(self):
		return len(self.rooms)

	def	erase(self, key):
		if key in self.rooms:
			del self.rooms[key]

	def clear(self):
		self.rooms.clear()

	def keys(self):
		return self.data.keys()
	
	def	__repr__(self):
		return repr(self.data)

#party types:
# 1 - 2 - 3 ai ? 
# 0 player vs player
# 4 player vs player in local

class	room:
	def	__init__(self, roomName: str, nbPlayers: int, partyType: int) -> None:
		self.roomName: str						= roomName
		self.channelLayer						= None
		self.roomGroupName						= None
		self.channelName						= None
		self.nbPlayers: int						= nbPlayers
		self.partyType: int						= partyType
		self.paddleL: Paddle					= Paddle(Vec2(3, 32.5), Vec2(3, 35), 1.5, 0)
		self.paddleR: Paddle					= Paddle(Vec2(94, 32.5), Vec2(3, 35), 1.5, 0)
		self.ball: Ball							= Ball(Vec2(48, 48), Vec2(4, 4), 45, 2)
		self.scoreL: int						= 0
		self.scoreR: int						= 0
		self.players: List[str]
		self.ready: bool						= False
		self.inGame: bool						= False
		self.lock: threading.Lock				= threading.lock()
		self.thread: Optional[threading.Thread]	= None

	def	__repr__(self):
		return repr(self.roomName)

	@database_sync_to_async
	async def	addPlayer(self, player: str) -> None:
		if self.partyType != 4:
			try:
				user = Player.objects.get(username=player)
			except Player.DoesNotExist:
				user = Player.objects.create(username=player)
			try:
				room = Room.objects.get(url=self.roomName)
			except Room.DoesNotExist:
				print("Room Does Not Exist: ", self.roomName, flush=True)
				return
			with self.lock:
				if player not in self.players:
					self.players.append(player)
				else:
					raise roomException("Player ", player, " is already in this room!", 1001)
				if len(self.players) == self.nbPlayers:
					self.ready = True

	#prevoir le cas ou c'est un tournois et c'est un forfait
	#juste faire un you win !
	  		# try:
			# 		user = Player.objects.get(username=self.username)
			# except Player.DoesNotExist:
			# 	user = Player.objects.create(username=self.username)
			# 	user.stanid = self.id
			# try:
			# 	room = Room.objects.get(url=self.room_name)
			# 	room.players.add(user)
			# 	print(self.username, ": player added to ", self.room_name, flush=True)
			# 	if (room.players.count() == room.maxPlayers):
			# 		return 1
	@database_sync_to_async
	async def	removePlayer(self, player: str) -> None:
		with self.lock:
			if self.inGame == True:
				await self.channel_layer.group_send(
						self.room_group_name, {"type": "quit", "message": "quitting"})
			if player in self.players:
				self.players.remove(player)
			else:
				raise roomException("Player ", player, " isn't in this room!", 1002)

	async def	countDown(self) -> None:
		if self.ready == True and self.inGame == False:
			x: int = 3
			while x > 0:
				#send to the group with the channel layer
				asyncio.sleep(1)
				x -= 1
			#send the end of the count down
		else:
			raise roomException("Room ", self.roomName, " haven't te good amount of players or is already in game", 1003)
	
	async def	start(self) -> None:
		try:
			await self.countDown()
			self.inGame = True
			self.thread = threading.Thread(target=self.gameLoop)
			self.thread.start()
			if self.thread:
				self.thread.join()
		except roomException as e:
					print(f"Error from start: {e}")
	
	async def	sendUpdate(self, message) -> None:
		await self.channel_layer.group_send(
						self.room_group_name, {"type": "gameUpdate", "message": message,
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
							"scoreR": self.scoreR
							})

	async def	gameLoop(self) -> None:
		message: str = "update"
		while self.inGame == True:
			with self.lock:
				self.PaddleL, self.PaddleR, self.Ball, self.ScoreL, self.ScoreR = gameUpdate(self.PaddleL, self.PaddleR, self.Ball, self.ScoreL, self.ScoreR)
				if self.scoreL == 5 or self.scoreR == 5:
					self.inGame = False
					message = "finish"
				await self.sendUpdate(message)
			await asyncio.sleep(1/20)

	def	updateData(self, data) -> None:
		with self.lock:
			if self.partyType == 4:
				if data['w'] == True:
					self.paddleL.key += self.paddleL.vel
				if data['s'] == True:
					self.paddleL.key -= self.paddleL.vel
				if data['up'] == True:
					self.paddleR.key += self.paddleR.vel
				if data['down'] == True:
					self.paddleR.key -= self.paddleR.vel
			elif self.partyType == 0:
				if data["username"] == self.players[0]:
					if data['w'] == True:
						self.paddleL.key += self.paddleL.vel
					if data['s'] == True:
						self.paddleL.key -= self.paddleL.vel
					if data['up'] == True:
						self.paddleL.key += self.paddleL.vel
					if data['down'] == True:
						self.paddleL.key -= self.paddleL.vel
				else:
					if data['w'] == True:
						self.paddleR.key += self.paddleR.vel
					if data['s'] == True:
						self.paddleR.key -= self.paddleR.vel
					if data['up'] == True:
						self.paddleR.key += self.paddleR.vel
					if data['down'] == True:
						self.paddleR.key -= self.paddleR.vel
			else:
				if data['w'] == True:
					self.paddleL.key += self.paddleL.vel
				if data['s'] == True:
					self.paddleL.key -= self.paddleL.vel
				if data['up'] == True:
					self.paddleL.key += self.paddleL.vel
				if data['down'] == True:
					self.paddleL.key -= self.paddleL.vel
			if self.paddleL.key > 0 and self.paddleL.key > self.paddleL.vel:
				self.paddleL.key = self.paddleL.vel
			elif self.paddleL.key < 0 and self.paddleL.key < -self.paddleL.vel:
				self.paddleL.key = -self.paddleL.vel
			if self.paddleR.key > 0 and self.paddleR.key > self.paddleR.vel:
				self.paddleR.key = self.paddleR.vel
			elif self.paddleR.key < 0 and self.paddleR.key < -self.paddleR.vel:
				self.paddleR.key = -self.paddleR.vel
