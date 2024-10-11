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
		self.tournament = False
		self.tournamentRoom = False

		print(self.room_name,": connection en cours",flush=True)

		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		try:
			# if gRoomsManager.rooms[self.room_name].ready == True:
			# 	#maybe send an error message to display ?
			# 	self.close()
			# 	return
			# Join room group
			tournamentroom = []
			if len(gTournament.rooms) != 0:
				for key in gTournament.rooms:
					tournamentroom.append(key)
				if self.room_name in tournamentroom:
					self.tournamentRoom = True
					gTournament.rooms[self.room_name].channelLayer = get_channel_layer()
					gTournament.rooms[self.room_name].roomGroupName = self.room_group_name
					gTournament.rooms[self.room_name].channelName = self.channel_name
					await self.accept()
					return
			if self.room_name == gTournament.lobbyRoom.roomName:
				self.tournament = True
				if gTournament.lobbyRoom.channelLayer == None:
					gTournament.lobbyRoom.channelLayer = get_channel_layer()
					print(self.room_name,": channel layer type: ",gTournament.lobbyRoom.channelLayer,flush=True)
					gTournament.lobbyRoom.roomGroupName = self.room_group_name
					print(self.room_name,": groupname: ",self.room_group_name,flush=True)
					gTournament.lobbyRoom.channelName = self.channel_name
					gTournament.consumer = self
				await self.accept()
			else:
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
		if self.tournament == True:
			if self.username:
				await gTournament.lobbyRoom.removePlayer(self.username)
		elif self.tournamentRoom == True:
			if self.username:
				await gTournament.rooms[self.room_name].removePlayer(self.username)
				await self.channel_layer.group_send(
								self.room_group_name, {"type": "quit", "message": "quitting", "left": self.username})
		else:
			if gRoomsManager.rooms[self.room_name].partyType != 4 and gRoomsManager.rooms[self.room_name].ready == False:
				try:
					await gRoomsManager.rooms[self.room_name].removePlayer(self.username)
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
		print('coucou de receive, type: ',text_data_json["type"], flush=True)
		if type_data == "username":
			self.username = text_data_json["username"]
			self.id = text_data_json["id"]
			if self.tournament == True:
				try:
					await gTournament.lobbyRoom.addPlayer(self.username)
				except Exception as e:
					print(self.username,": error: ",e,flush=True)
					await self.close()
				if gTournament.lobbyRoom.ready == True:
					# await self.channel_layer.group_send(
					# self.room_group_name, {"type": "gameUpdate", "message": "ready for playing"})
					print(self.username,": start lanceeeeeeee", "on room: ",self.room_name,flush=True)
					gTournament.start()
			elif self.tournamentRoom == True:
				try:
					await gTournament.rooms[self.room_name].addPlayer(self.username)
				except Exception as e:
					print(self.username,": error: ",e,flush=True)
					await self.close()
				if gTournament.rooms[self.room_name].ready == True:
					await self.channel_layer.group_send(
					self.room_group_name, {"type": "gameUpdate", "message": "ready for playing"})
					await gTournament.rooms[self.room_name].start()
					print(self.username,": start lanceeeeeeee", "on room: ",self.room_name,flush=True)
			else:
				if gRoomsManager.rooms[self.room_name].partyType != 4:
					try:
						await gRoomsManager.rooms[self.room_name].addPlayer(self.username)
						if gRoomsManager.rooms[self.room_name].partyType > 0 and gRoomsManager.rooms[self.room_name].partyType < 4:
							await gRoomsManager.rooms[self.room_name].addPlayer("AI")
							gRoomsManager.rooms[self.room_name].paddleR.ai = gRoomsManager.rooms[self.room_name].partyType
					except Exception as e:
						print(self.username,": error: ",e,flush=True)
						await self.close()
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
			if self.tournamentRoom == True:
				gTournament.rooms[self.room_name].updateData(text_data_json, self.username)
			else:
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
			if self.tournament == False and self.tournamentRoom == False:
				await self.send(text_data=json.dumps({"type": "ready for playing", "message": "ready for playing",
										"player1Name": gRoomsManager.rooms[self.room_name].players[0],
										"player2Name": gRoomsManager.rooms[self.room_name].players[1],}))
			elif self.tournamentRoom == True:
				await self.send(text_data=json.dumps({"type": "ready for playing", "message": "ready for playing",
										"player1Name": gTournament.rooms[self.room_name].players[0],
										"player2Name": gTournament.rooms[self.room_name].players[1],}))

	async def tournamentRedirect(self, event):
		print("Event received in tournament: ", event, flush=True)
		print("From Tournament: ",event["numberOfRooms"]," number of rooms",flush=True)
		roomKey = ""
		for key, value in event.items():
			if value == self.username:
				roomKey = key
				break
		roomKey = roomKey[:-1]
		print("roomKey: ",roomKey,flush=True)
		await self.send(text_data=json.dumps({
			"type": "tournament",
			"message": "redirect",
			"url": event[roomKey]+'/'
		}))

	async def quit(self, event):
		print(self.username, ': bisous de quit', flush=True)
		message = event["message"]
		if self.tournamentRoom == True and gTournament.rooms[self.room_name].inGame == True:
			if gTournament.rooms[self.room_name].players[0] == event["left"]:
				gTournament.rooms[self.room_name].scoreR = 5
			else:
				gTournament.rooms[self.room_name].scoreL = 5
		else:
			if gRoomsManager.rooms[self.room_name].players[0] == event["left"]:
				gRoomsManager.rooms[self.room_name].scoreR = 5
			else:
				gRoomsManager.rooms[self.room_name].scoreL = 5
		# await self.send(text_data=json.dumps({"type": "end game", "message": message}))
		await self.close()

class	TournoisConsumer(AsyncWebsocketConsumer):
	async def	connect(self):
		self.accept()
