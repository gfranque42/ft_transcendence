import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .pong import *
import asyncio
from .rooms import *
from channels.layers import get_channel_layer


gRoomsManager: roomsManager = roomsManager()

gTournament: tournament = tournament()

class	PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = "pong_%s" % self.room_name
		self.username = None

		print(self.room_name,": connection en cours",flush=True)

		try:
			# if gRoomsManager.rooms[self.room_name].ready == True:
			# 	#maybe send an error message to display ?
			# 	self.close()
			# 	return
			# Join room group
			await self.channel_layer.group_add(self.room_group_name, self.channel_name)
			print(self.room_name,": partyType = [",type(gRoomsManager.rooms[self.room_name].partyType),"]",flush=True)
			if int(gRoomsManager.rooms[self.room_name].partyType) == 4:
				await gRoomsManager.rooms[self.room_name].addPlayer("Player1")
				await gRoomsManager.rooms[self.room_name].addPlayer("Player2")
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
		if gRoomsManager.rooms[self.room_name].partyType != 4 and gRoomsManager.rooms[self.room_name].inGame == False:
			try:
				await gRoomsManager.rooms[self.room_name].removePlayer(self.username)
			except Exception as e:
				print(self.room_name,": error: ",e,flush=True)
		# Leave room group
		if gRoomsManager.rooms[self.room_name].thread and self.username and gRoomsManager.rooms[self.room_name].players[0] == self.username and gRoomsManager.rooms[self.room_name].finish == True:
			gRoomsManager.rooms[self.room_name].thread.join()
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
			self.id = text_data_json["id"]
			if gRoomsManager.rooms[self.room_name].partyType != 4:
				try:
					await gRoomsManager.rooms[self.room_name].addPlayer(self.username)
					if gRoomsManager.rooms[self.room_name].partyType > 0 and gRoomsManager.rooms[self.room_name].partyType < 4:
						await gRoomsManager.rooms[self.room_name].addPlayer("AI")
						gRoomsManager.rooms[self.room_name].paddleR.ai = gRoomsManager.rooms[self.room_name].partyType
				except Exception as e:
					print(self.username,": error: ",e,flush=True)
					self.close()
					# say to the front goodbye
				if gRoomsManager.rooms[self.room_name].ready == True:
					await self.channel_layer.group_send(
					self.room_group_name, {"type": "gameUpdate", "message": "ready for playing"})
					await gRoomsManager.rooms[self.room_name].start()
					print(self.username,": start lanceeeeeeee", "on room: ",self.room_name,flush=True)
			else:
				await self.channel_layer.group_send(
					self.room_group_name, {"type": "gameUpdate", "message": "ready for playing"})
				await gRoomsManager.rooms[self.room_name].start()
				print(self.username,": start lanceeeeeeee", "on room: ",self.room_name,flush=True)
		elif type_data == "ping":
			print('ping recu !:',text_data,flush=True)
			print('ping recu !:',text_data_json,flush=True)
			gRoomsManager.rooms[self.room_name].updateData(text_data_json, self.username)

	# Receive message from room group
	async def gameUpdate(self, event):
		print(self.username,': bisous de game_update',flush=True)
		message = event["message"]
		event["username"] = self.username
		event["id"] = self.id
		print(self.username,': ',message,flush=True)
		if (message == "update"):
			print(self.username,': valeur de paddledir:', event["paddleLd"],flush=True)
			await self.send(text_data=json.dumps(event))
		elif (message == "finish"):
			print(self.username,': the game is finished !\nBye bye !',flush=True)
			await self.send(text_data=json.dumps(event))
			await asyncio.sleep(1)
			await self.close()
		elif (message == "countdown"):
			await self.send(text_data=json.dumps({"type": "compte a rebour",
					"message": "compte a rebour",
					"number": event["number"]}))
		elif (message == "fin du compte"):
			await self.send(text_data=json.dumps({"type": "fin du compte",
										 "message": "fin du compte",
			}))
		elif (message == "ready for playing"):
			await self.send(text_data=json.dumps({"type": "ready for playing", "message": "ready for playing",
										"player1Name": gRoomsManager.rooms[self.room_name].players[0],
										"player2Name": gRoomsManager.rooms[self.room_name].players[1],}))

	async def quit(self, event):
		print(self.username, ': bisous de quit', flush=True)
		message = event["message"]
		await self.send(text_data=json.dumps({"type": "end game", "message": message}))
		await self.close()
