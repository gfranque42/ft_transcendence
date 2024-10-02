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

gTournament: tournament = tournament()

class	PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = "pong_%s" % self.room_name

		print(self.room_name,": connection en cours",flush=True)

		if gRoomsManager.rooms[self.room_name].ready == True:
			#maybe send an error message to display ?
			self.close()
			return
		# Join room group
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		print(self.room_name,": partyType = [",type(gRoomsManager.rooms[self.room_name].partyType),"]",flush=True)
		if int(gRoomsManager.rooms[self.room_name].partyType) == 4:
			print(self.room_name,": coucou @@@@@@@",flush=True)
			await gRoomsManager.rooms[self.room_name].addPlayer("Player1")
			await gRoomsManager.rooms[self.room_name].addPlayer("Player2")
		if gRoomsManager.rooms[self.room_name].channelLayer == None:
			gRoomsManager.rooms[self.room_name].channelLayer = self.channel_layer
			gRoomsManager.rooms[self.room_name].roomGroupName = self.room_group_name
			gRoomsManager.rooms[self.room_name].channelName = self.channel_name
		await self.accept()
		await self.send(text_data=json.dumps({"type": "connected"}))

	async def disconnect(self, close_code):
		if int(gRoomsManager.rooms[self.room_name].partyType) != 4:
			await gRoomsManager.rooms[self.room_name].removePlayer(self.username)
		# Leave room group
		await self.channel_layer.group_send(
						self.room_group_name, {"type": "quit", "message": "quitting"})
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		type_data = text_data_json["type"]
		print('coucou de receive, type: ',text_data_json["type"], flush=True)
		if type_data == "username":
			self.username = text_data_json["username"]
			if gRoomsManager.rooms[self.room_name].partyType != 4:
				await gRoomsManager.rooms[self.room_name].addPlayer(self.username)
			else:
				await gRoomsManager.rooms[self.room_name].start()
		elif type_data == "ping":
			gRoomsManager.rooms[self.room_name].updateData(text_data_json)

	# Receive message from room group
	async def gameUpdate(self, event):
		print(self.username, ': bisous de game_update', flush=True)
		message = event["message"]
		print(self.username, ': ', message, flush=True)
		if (message == "update"):
			await self.send(text_data=json.dumps(event))
		elif (message == "finish"):
			await self.send(text_data=json.dumps(event))
			await self.close()
		elif (message == "countdown"):
			await self.send(text_data=json.dumps({"type": "compte a rebour",
					"message": "compte a rebour",
					"number": event["number"]}))
		elif (message == "fin du compte"):
			await self.send(text_data=json.dumps({"type": "fin du compte",
										 "message": "fin du compte",
			}))

	async def quit(self, event):
		print(self.username, ': bisous de quit', flush=True)
		message = event["message"]
		await self.send(text_data=json.dumps({"type": "end game", "message": message}))
		await self.close()
