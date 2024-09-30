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

		if gRoomsManager[self.room_name].ready == True:
			#maybe send an error message to display ?
			self.close()
			return
		# Join room group
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		if gRoomsManager[self.room_name].partyType == 4:
			gRoomsManager[self.room_name].addPlayer("Player1")
			gRoomsManager[self.room_name].addPlayer("Player2")
		if gRoomsManager[self.room_name].channelLayer == None:
			gRoomsManager[self.room_name].channelLayer = self.channel_layer
			gRoomsManager[self.room_name].roomGroupName = self.room_group_name
			gRoomsManager[self.room_name].channelName = self.channel_name
		await self.accept()

	async def disconnect(self, close_code):
		gRoomsManager[self.room_name].removePlayer(self.username)
		# Leave room group
		await self.channel_layer.group_send(
						self.room_group_name, {"type": "quit", "message": "quitting"})
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		type_data = text_data_json["type"]
		if type_data == "username":
			self.username = text_data_json["username"]
			if gRoomsManager[self.room_name].partyType != 4:
				gRoomsManager[self.room_name].addPlayer(self.username)
		elif type_data == "ping":
			gRoomsManager[self.room_name].updateData(text_data_json)

	# Receive message from room group
	async def gameUpdate(self, event):
		print(self.username, ': bisous de game_update', flush=True)
		message = event["message"]
		print(self.username, ': ', message, flush=True)
		if (message == "update"):
			await self.send(event)
		elif (message == "finish"):
			await self.send(event)
			await self.close()

	async def quit(self, event):
		print(self.username, ': bisous de quit', flush=True)
		message = event["message"]
		await self.send(text_data=json.dumps({"type": "end game", "message": message}))
		await self.close()
