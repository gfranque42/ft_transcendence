from typing import List, Optional
from threading import Thread, Lock
import threading
from .pong import *
from .models import Room, Player
import asyncio
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from concurrent.futures import ThreadPoolExecutor
# from pydantic import BaseModel
import time

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
		self.ball: Ball							= Ball(Vec2(48, 48), Vec2(4, 4), 45, 2)
		self.scoreL: int						= 0
		self.scoreR: int						= 0
		self.players: List[str]					= []
		self.ready: bool						= False
		self.inGame: bool						= False
		self.lock: threading.Lock				= Lock()
		self.thread: Optional[threading.Thread]	= None
		print(self.roomName,": Je suis initialisé !",flush=True)

	def	__repr__(self):
		return repr(self.roomName)

	@database_sync_to_async
	def	addPlayer(self, player: str) -> None:
		print(self.roomName,": I have to append ",player,flush=True)
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
					room.players.add(user)
				else:
					raise roomException("Player ", player, " is already in this room!", 1001)
				if len(self.players) == self.nbPlayers:
					self.ready = True
		else:
			with self.lock:
				if player not in self.players:
					self.players.append(player)
				else:
					raise roomException("Player ", player, " is already in this room!", 1001)
				if len(self.players) == 2:
					self.ready = True

	@database_sync_to_async
	def	removePlayer(self, player: str) -> None:
		print(self.roomName,": I have to remove ",player,flush=True)
		if self.partyType != 4:
			try:
				room = Room.objects.get(url=self.roomName)
			except Room.DoesNotExist:
				print("Room Does Not Exist: ", self.roomName, flush=True)
				return
			with self.lock:
				if self.inGame == True:
					async_to_sync(self.channelLayer.group_send)(
							self.roomGroupName, {"type": "quit", "message": "quitting"})
				if player in self.players:
					self.players.remove(player)
					room.players.delete(username=player)
				else:
					raise roomException("Player ", player, " isn't in this room!", 1002)

	def	countDown(self) -> None:
		print(self.roomName,": countdown started",flush=True)
		if self.ready == True and self.inGame == False:
			x: int = 3
			while x > 0:
				#send to the group with the channel layer
				async_to_sync(self.channelLayer.group_send(
						self.roomGroupName, {"type": "gameUpdate",
							"message": "countdown",
							"number": x,}))
				time.sleep(1)
				x -= 1
			#send the end of the count down
			async_to_sync(self.channelLayer.group_send(
						self.roomGroupName, {"type": "gameUpdate",
							"message": "fin du compte",}))
		else:
			raise roomException("Room ", self.roomName, " haven't the good amount of players or is already in game", 1003)

	async def	start(self) -> None:
		try:
			print(self.roomName,": start on our way !",flush=True)
			self.countDown()
			print(self.roomName,": countdown done !",flush=True)
			self.inGame = True
			print(self.roomName,": in game = ",self.inGame,flush=True)
			self.thread = Thread(target=self.gameLoop, args=())
			print(self.roomName,": thread created",flush=True)
			self.thread.start()
			if self.thread:
				print(self.roomName,": thread launched !",flush=True)
				self.thread.join()
		except roomException as e:
					print(f"Error from start: {e}")

	async def	sendUpdate(self, message) -> None:
		print(self.roomName,": sendUpdate with message \"",message,"\"",flush=True)
		await self.channelLayer.group_send(
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
							"scoreR": self.scoreR
							})

	def	gameLoop(self) -> None:
		print(self.roomName,": gameLoop started !",flush=True)
		message: str = "update"
		while self.inGame == True:
			# with self.lock:
			self.paddleL, self.paddleR, self.ball, self.scoreL, self.scoreR = gameUpdate(self.paddleL, self.paddleR, self.ball, self.scoreL, self.scoreR)
			if self.scoreL == 5 or self.scoreR == 5:
				self.inGame = False
				message = "finish"
				print(self.roomName,": the game is finished",flush=True)
			async_to_sync(self.sendUpdate(message))
			async_to_sync(asyncio.sleep(1/20))

	def	updateData(self, data, username: str) -> None:
		# with self.lock:
		print(self.roomName,": data receive for updateData",flush=True)
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
			if username == self.players[0]:
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
		print(self.roomName,": fin de updateData!",flush=True)
