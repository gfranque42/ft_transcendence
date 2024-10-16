import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .pong import *
import asyncio
from .rooms import gTournament, gRoomsManager
from channels.layers import get_channel_layer

class	PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = "pong_%s" % self.room_name
		self.username = None
		self.tournament = False


		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		try:
			if int(gRoomsManager.rooms[self.room_name].partyType) == 4:
				await gRoomsManager.rooms[self.room_name].addPlayer("Player1", 0)
				await gRoomsManager.rooms[self.room_name].addPlayer("Player2", 0)
			if gRoomsManager.rooms[self.room_name].channelLayer == None:
				gRoomsManager.rooms[self.room_name].channelLayer = get_channel_layer()
				gRoomsManager.rooms[self.room_name].roomGroupName = self.room_group_name
				gRoomsManager.rooms[self.room_name].channelName = self.channel_name
			await self.accept()
			await self.send(text_data=json.dumps({"type": "connected"}))
		except Exception as e:
			print(self.room_name,": error: ",e,flush=True)
			self.close()

	async def disconnect(self, close_code):
		if gRoomsManager.rooms[self.room_name].partyType != 4 and gRoomsManager.rooms[self.room_name].ready == False:
			try:
				await gRoomsManager.rooms[self.room_name].removePlayer(self.username, self.id)
			except Exception as e:
				print(self.room_name,": error: ",e,flush=True)
		# Leave room group
		await self.channel_layer.group_send(
						self.room_group_name, {"type": "quit", "message": "quitting", "left": self.username})
		if gRoomsManager.rooms[self.room_name].thread and self.username and gRoomsManager.rooms[self.room_name].players[0] == self.username and gRoomsManager.rooms[self.room_name].finish == True:
			gRoomsManager.rooms[self.room_name].thread.join()
				
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		type_data = text_data_json["type"]
		if type_data == "username":
			self.username = text_data_json["username"]
			self.id = text_data_json["id"]
			if gRoomsManager.rooms[self.room_name].partyType != 4:
				try:
					await gRoomsManager.rooms[self.room_name].addPlayer(self.username, self.id)
					if gRoomsManager.rooms[self.room_name].partyType > 0 and gRoomsManager.rooms[self.room_name].partyType < 4:
						await gRoomsManager.rooms[self.room_name].addPlayer("AI", 0)
						gRoomsManager.rooms[self.room_name].paddleR.ai = gRoomsManager.rooms[self.room_name].partyType
				except Exception as e:
					print(self.username,": error: ",e,flush=True)
					await self.close()
					# say to the front goodbye
				if gRoomsManager.rooms[self.room_name].ready == True:
					if gRoomsManager.rooms[self.room_name].partyType == 5 and self.room_name != "SbDaMcGf24":
						await gRoomsManager.rooms[self.room_name].waitForTournament()
					else:
						await self.channel_layer.group_send(
						self.room_group_name, {"type": "gameUpdate", "message": "ready for playing"})
						await gRoomsManager.rooms[self.room_name].start()
			else:
				await self.channel_layer.group_send(
					self.room_group_name, {"type": "gameUpdate", "message": "ready for playing"})
				await gRoomsManager.rooms[self.room_name].start()
		elif type_data == "ping":
			gRoomsManager.rooms[self.room_name].updateData(text_data_json, self.username)

	# Receive message from room group
	async def gameUpdate(self, event):
		message = event["message"]
		event["username"] = self.username
		if (message == "update"):
			await self.send(text_data=json.dumps(event))
		elif (message == "finish"):
			event["id"] = self.id
			await self.send(text_data=json.dumps(event))
			event["button"] = "Back to the menu"
			event["redir"] = "/"
			await asyncio.sleep(1)
			await self.close()
		elif (message == "countdown"):
			await self.send(text_data=json.dumps({"type": "compte a rebour",
					"message": "compte a rebour",
					"number": event["number"]}))
		elif (message == "matchmaking"):
			await self.send(text_data=json.dumps({"type": message, "message": message,
										"player1": event["player1"],
										"player2": event["player2"]}))
		elif (message == "fin du compte"):
			await self.send(text_data=json.dumps({"type": "fin du compte",
										 "message": "fin du compte",
			}))
		elif (message == "tournament start") and self.username == gRoomsManager.rooms[self.room_name].players[0]:
			await self.channel_layer.group_send(
					self.room_group_name, {"type": "gameUpdate", "message": "ready for playing"})
			await gRoomsManager.rooms[self.room_name].start()
		elif (message == "ready for playing"):
			await self.send(text_data=json.dumps({"type": "ready for playing", "message": "ready for playing",
										"player1Name": gRoomsManager.rooms[self.room_name].players[0],
										"player2Name": gRoomsManager.rooms[self.room_name].players[1],}))
