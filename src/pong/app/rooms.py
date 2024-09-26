from typing import List, Optional
from threading import Thread
import threading
from .pong import *
import asyncio

class	roomException(Exception):
	def	__init__(self, message: str, errorCode: int):
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

	def	addPlayer(self, player: str) -> None:
		if player not in self.players:
			self.players.append(player)
		else:
			raise roomException("Player ", player, " is already in this room!", 1001)
		if len(self.players) == self.nbPlayers:
			self.ready = True

	def	removePlayer(self, player: str) -> None:
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
	
	def	gameLoop(self) -> None:
		while self.inGame == True:
			with self.lock:
				gameUpdate(self.PaddleL, self.PaddleR, self.Ball, self.ScoreL, self.ScoreR)
				if self.scoreL == 5 or self.scoreR == 5:
					# self.inGame = False
					finish = True
					#send the finish group
			#send to the group with the channel layer

	def	updateData(self, data) -> None:
		with self.lock:
			self.ball.coor.x = data["ballcx"]
			self.ball.coor. y = data["ballcy"]
			self.ball.size.x = data["ballsx"]
			self.ball.size.y = data["ballsy"]
			self.ball.dir.x = data["balldx"]
			self.ball.dir.y = data["balldy"]
			self.ball.angle = data["balla"]
			self.ball.vel = data["ballv"]
			self.paddleL.coor.x = data["paddleLcx"]
			self.paddleL.coor. y = data["paddleLcy"]
			self.paddleL.size.x = data["paddleLsx"]
			self.paddleL.size.y = data["paddleLsy"]
			self.paddleL.dir = data["paddleLd"]
			self.paddleL.key = data["paddleLk"]
			self.paddleL.vel = data["paddleLv"]
			self.paddleR.coor.x = data["paddleRcx"]
			self.paddleR.coor. y = data["paddleRcy"]
			self.paddleR.size.x = data["paddleRsx"]
			self.paddleR.size.y = data["paddleRsy"]
			self.paddleR.dir = data["paddleRd"]
			self.paddleR.key = data["paddleRk"]
			self.paddleR.vel = data["paddleRv"]
			self.scoreL = data["scoreL"]
			self.scoreR = data["scoreR"]
