import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .models import Room, Player
from .pong import *

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
		# if (type_data == "message"):
		# 	text_data_json["message"]
		# 	message = text_data_json["message"]

		# 	# Send message to room group
		# 	await self.channel_layer.group_send(
		# 		self.room_group_name, {"type": "chat_message", "message": message}
		# 	)
		if (type_data == "username"):
			username = text_data_json["username"]
			self.username = username
			try:
				print('bisous de receive', flush=True)
				ready = await self.add_player()
				await self.send(text_data=json.dumps({
					"type": "connected"
				}))
				if (ready == 1):
					await self.channel_layer.group_send(
						self.room_group_name, {"type": "update", "message": "ready for playing"}
					)
			except Exception as e:
				print(f"Exception from receive: {e}", flush=True)

	# Receive message from room group
	async def update(self, event):
		print('bisous de update', flush=True)
		message = event["message"]
		print(message, flush=True)
		if (message == "ready for playing"):
			await self.send(text_data=json.dumps({"type": message}))
		# message = event["message"]

		# # Send message to WebSocket
		# await self.send(text_data=json.dumps({"message": message}))

	@database_sync_to_async
	def add_player(self):
		print('bisous de add_player', flush=True)
		if (self.username):
			try:
				user = Player.objects.get(username=self.username)
			except Player.DoesNotExist:
				user = Player.objects.create(username=self.username)
			try:
				room = Room.objects.get(url=self.room_name)
				room.players.add(user)
				print("player added to ", self.room_name)
				if (room.players.count() == room.maxPlayers):
					return 1
			except Exception as e:
				print(f"Exception form add_player: {e}", flush=True)
		return 0
