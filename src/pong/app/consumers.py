import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .models import Room, Player
from .pong import *
import asyncio
from .rooms import *

gRoomsManager: roomsManager = roomsManager()

class	PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = "pong_%s" % self.room_name

		# Join room group
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)

		await self.accept()

	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_send(
						self.room_group_name, {"type": "quit", "message": "quitting"})
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		type_data = text_data_json["type"]

	# Receive message from room group
	async def update(self, event):
		print(self.username, ': bisous de update', flush=True)
		message = event["message"]
		print(self.username, ":", message, flush=True)
		if (message == "ready for playing"):
			print(self.username, ': update ready', flush=True)
			self.player1Name = event["player1Name"]
			self.player2Name = event["player2Name"]
			self.player1id = event["player1id"]
			self.player2id = event["player2id"]
			await self.send(text_data=json.dumps({"type": message, "player1Name": self.player1Name, "player2Name": self.player2Name}))
			await self.set_game()
			await self.send_updated_game(message)
			await self.count_down()

	async def game_update(self, event):
		print(self.username, ': bisous de game_update', flush=True)
		message = event["message"]
		print(self.username, ': ', message, flush=True)
		if (message == "in playing"):
			self.ball.coor.x = event["ballcx"]
			self.ball.coor. y = event["ballcy"]
			self.ball.size.x = event["ballsx"]
			self.ball.size.y = event["ballsy"]
			self.ball.dir.x = event["balldx"]
			self.ball.dir.y = event["balldy"]
			self.ball.angle = event["balla"]
			self.ball.vel = event["ballv"]
			self.paddleL.coor.x = event["paddleLcx"]
			self.paddleL.coor. y = event["paddleLcy"]
			self.paddleL.size.x = event["paddleLsx"]
			self.paddleL.size.y = event["paddleLsy"]
			self.paddleL.dir = event["paddleLd"]
			self.paddleL.key = event["paddleLk"]
			self.paddleL.vel = event["paddleLv"]
			self.paddleR.coor.x = event["paddleRcx"]
			self.paddleR.coor. y = event["paddleRcy"]
			self.paddleR.size.x = event["paddleRsx"]
			self.paddleR.size.y = event["paddleRsy"]
			self.paddleR.dir = event["paddleRd"]
			self.paddleR.key = event["paddleRk"]
			self.paddleR.vel = event["paddleRv"]
			self.scoreL = event["scoreL"]
			self.scoreR = event["scoreR"]
		elif (message == "game is finished"):
			self.scoreL = event["scoreL"]
			self.scoreR = event["scoreR"]
		await self.send_updated_game(message)

	async def quit(self, event):
		print(self.username, ': bisous de quit', flush=True)
		message = event["message"]
		await self.send(text_data=json.dumps({"type": "end game", "message": message}))
		await self.close()
