from .pong import *

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

class	room:
	def	__init__(self, roomName: str, nbPlayers: int, partyType: int) -> None:
		self.roomName: str		= roomName
		self.nbPlayers: int		= nbPlayers
		self.partyType: int		= partyType
		self.paddleL: Paddle	= Paddle(Vec2(3, 32.5), Vec2(3, 35), 1.5, 0)
		self.paddleR: Paddle	= Paddle(Vec2(94, 32.5), Vec2(3, 35), 1.5, 0)
		self.ball: Ball			= Ball(Vec2(48, 48), Vec2(4, 4), 45, 2)
		self.scoreL: int		= 0
		self.scoreR: int		= 0
		self.players: List[str]
		self.ready: bool		= False
		self.inGame: bool		= False
	
	def	addPlayer(self, player: str) -> None:
		if player not in self.players:
			self.players.append(player)
		else
			raise roomException("Player is already in this room!", 1001)
		if len(self.players) == self.nbPlayers
			self.ready = True

	def	removePlayer(self, player: str) -> None:

