import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .models import Room, Player
from .pong import *
import asyncio

class	PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = "pong_%s" % self.room_name

		# Join room group
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)

		await self.accept()

	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		type_data = text_data_json["type"]

		if (type_data == "username"):
			username = text_data_json["username"]
			self.username = username
			try:
				print(self.username, ': bisous de receive', flush=True)
				ready = await self.add_player()
				await self.send(text_data=json.dumps({
					"type": "connected"
				}))
				if (ready == 1):
					print(self.username, ': ready and before add_player_names', flush=True)
					await self.add_player_names()
					await self.channel_layer.group_send(
						self.room_group_name, {"type": "update", "message": "ready for playing", "player1Name": self.player1Name, "player2Name": self.player2Name})
			except Exception as e:
				print(f"Exception from receive: {e}", flush=True)
		elif (type_data == "ping"):
			await self.channel_layer.group_send(
						self.room_group_name, {"type": "game_update", "message": "in playing"})

	# Receive message from room group
	async def update(self, event):
		print(self.username, ': bisous de update', flush=True)
		message = event["message"]
		print(self.username, ":", message, flush=True)
		if (message == "ready for playing"):
			print(self.username, ': update ready', flush=True)
			self.player1Name = event["player1Name"]
			self.player2Name = event["player2Name"]
			await self.send(text_data=json.dumps({"type": message, "player1Name": self.player1Name, "player2Name": self.player2Name}))
			await self.set_game()
			await self.send_updated_game()
			await self.count_down()

	async def game_update(self, event):
		print(self.username, ': bisous de game_update', flush=True)
		message = event["message"]
		print(self.username, ': ', message, flush=True)
		await self.send_updated_game()

	@database_sync_to_async
	def add_player(self):
		print(self.username, ': bisous de add_player', flush=True)
		if (self.username):
			try:
				user = Player.objects.get(username=self.username)
			except Player.DoesNotExist:
				user = Player.objects.create(username=self.username)
			try:
				room = Room.objects.get(url=self.room_name)
				room.players.add(user)
				print(self.username, ": player added to ", self.room_name, flush=True)
				if (room.players.count() == room.maxPlayers):
					return 1
			except Exception as e:
				print(f"Exception form add_player: {e}", flush=True)
		return 0

	@database_sync_to_async
	def add_player_names(self):
		print(self.username, ': bisous de add_player_names', flush=True)
		try:
			room = Room.objects.get(url=self.room_name)
			players = list(room.players.all())
			if room.maxPlayers == 2 and self.username == players[1].username:
				self.player1Name = players[0].username
				print(self.username, ': add_player_names: ', players[0].username, ", ", players[1].username, flush=True)
				self.player2Name = players[1].username
			elif room.maxPlayers == 2:
				self.player1Name = players[1].username
				print(self.username, ': add_player_names: ', players[1].username, ", ", players[0].username, flush=True)
				self.player2Name = players[0].username
			else:
				self.player1Name = players[0].username
				print(self.username, ': add_player_names: ', players[0].username, ", AI", flush=True)
				self.player2Name = "AI"
		except Exception as e:
			print(f"Exception form add_player_names: {e}", flush=True)

	async def count_down(self):
		sec = 3
		while sec > 0:
			await self.send(text_data=json.dumps({"type": "compte a rebour", "number": sec}))
			await asyncio.sleep(1)
			sec -= 1
		await self.send(text_data=json.dumps({"type": "fin du compte"}))

	@database_sync_to_async
	def set_game(self):
		try:
			print(self.username, ': bisous de set_game', flush=True)
			room = Room.objects.get(url=self.room_name)
			self.ball = Ball(Vec2(48, 48), Vec2(4, 4), Vec2(1, 0), 1)
			self.paddleL = Paddle(Vec2(3, 30), Vec2(3, 40), 0)
			self.paddleR = Paddle(Vec2(94, 30), Vec2(3, 40), room.difficulty)
			self.scoreL = 0
			self.scoreR = 0
		except Exception as e:
			print(f"Exception form set_game: {e}", flush=True)

	async def send_updated_game(self):
		await self.send(text_data=json.dumps({"type": "game update",
										"ballcx": self.ball.getXMin(),
										"ballcy": self.ball.getYMin(),
										"ballsx": self.ball.getSizeX(),
										"ballsy": self.ball.getSizeY(),
										"paddleLcx": self.paddleL.getXMin(),
										"paddleLcy": self.paddleL.getYMin(),
										"paddleLsx": self.paddleL.getSizeX(),
										"paddleLsy": self.paddleL.getSizeY(),
										"paddleRcx": self.paddleR.getXMin(),
										"paddleRcy": self.paddleR.getYMin(),
										"paddleRsx": self.paddleR.getSizeX(),
										"paddleRsy": self.paddleR.getSizeY(),
										"scoreL": 4,
										"scoreR": 3}))
										# "scoreL": self.scoreL,
