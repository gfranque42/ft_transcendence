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
		print(self.username, ': quitting', flush=True)
		await self.channel_layer.group_send(
						self.room_group_name, {"type": "quit", "message": "quitting"})
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		type_data = text_data_json["type"]

		if (type_data == "username"):
			username = text_data_json["username"]
			self.username = username
			self.id = text_data_json["id"]
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
						self.room_group_name, {"type": "update", "message": "ready for playing", "player1Name": self.player1Name, "player2Name": self.player2Name,
												"player1id": self.player1id, "player2id": self.player2id})
			except Exception as e:
				print(f"Exception from receive: {e}", flush=True)
		elif (type_data == "ping"):
			if (self.username == self.player1Name):
				try:
					if ("move" in text_data_json):
						self.paddleL.key = 0
						if (text_data_json["move"] == "up"):
							self.paddleL.key = -self.paddleL.vel
							# self.paddleL.coor. y = self.paddleL.coor.y - self.paddleL.vel
						elif (text_data_json["move"] == "down"):
							self.paddleL.key = self.paddleL.vel
							# self.paddleL.coor. y = self.paddleL.coor.y + self.paddleL.vel
				except KeyError as e:
					print(f"KeyError: {e}")
				except Exception as e:
					print(f"Exception from receive: {e}")
			else:
				try:
					if ("move" in text_data_json):
						self.paddleR.key = 0
						if (text_data_json["move"] == "up"):
							self.paddleR.key = -self.paddleR.vel
							# self.paddleR.coor. y = self.paddleR.coor.y - self.paddleR.vel
						elif (text_data_json["move"] == "down"):
							self.paddleR.key = self.paddleR.vel
							# self.paddleR.coor. y = self.paddleR.coor.y + self.paddleR.vel
				except KeyError as e:
					print(f"KeyError: {e}")
				except Exception as e:
					print(f"Exception from receive: {e}")
			# self.paddleL, self.paddleR, self.ball = gameUpdate(self.paddleL, self.paddleR, self.ball)
			if (self.scoreL == 5 or self.scoreR == 5):
				await self.channel_layer.group_send(
							self.room_group_name, {"type": "game_update", "message": "game is finished",
							  			"scoreL": self.scoreL,
										"scoreR": self.scoreR})
			else:
				await self.channel_layer.group_send(
							self.room_group_name, {"type": "game_update", "message": "in playing",
										"ballcx": self.ball.coor.x,
										"ballcy": self.ball.coor.y,
										"ballsx": self.ball.size.x,
										"ballsy": self.ball.size.y,
										"balldx": self.ball.dir.x,
										"balldy": self.ball.dir.y,
										"balla": self.ball.angle,
										"ballv": self.ball.vel,
										"paddleLcx": self.paddleL.coor.x,
										"paddleLcy": self.paddleL.coor.y,
										"paddleLsx": self.paddleL.size.x,
										"paddleLsy": self.paddleL.size.y,
										"paddleLd": self.paddleL.dir,
										"paddleLk": self.paddleL.key,
										"paddleLv": self.paddleL.vel,
										"paddleRcx": self.paddleR.coor.x,
										"paddleRcy": self.paddleR.coor.y,
										"paddleRsx": self.paddleR.size.x,
										"paddleRsy": self.paddleR.size.y,
										"paddleRd": self.paddleR.dir,
										"paddleRk": self.paddleR.key,
										"paddleRv": self.paddleR.vel,
										"scoreL": self.scoreL,
										"scoreR": self.scoreR})

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

	@database_sync_to_async
	def add_player(self):
		print(self.username, ': bisous de add_player', flush=True)
		if (self.username):
			try:
				user = Player.objects.get(username=self.username)
			except Player.DoesNotExist:
				user = Player.objects.create(username=self.username)
				user.stanid = self.id
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
				self.player1id = players[0].stanid
				print(self.username, ': add_player_names: ', players[0].username, ", ", players[1].username, flush=True)
				self.player2Name = players[1].username
				self.player2id = players[1].stanid
			elif room.maxPlayers == 2:
				self.player1Name = players[1].username
				self.player1id = players[1].stanid
				print(self.username, ': add_player_names: ', players[1].username, ", ", players[0].username, flush=True)
				self.player2Name = players[0].username
				self.player2id = players[0].stanid
			else:
				self.player1Name = players[0].username
				self.player1id = players[0].stanid
				print(self.username, ': add_player_names: ', players[0].username, ", AI", flush=True)
				self.player2Name = "AI"
				self.player2id = -1
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
			self.ball = Ball(Vec2(48, 48), Vec2(4, 4), 45, 2)
			self.paddleL = Paddle(Vec2(3, 32.5), Vec2(3, 35), 1.5, 0)
			self.paddleR = Paddle(Vec2(94, 32.5), Vec2(3, 35), 1.5, room.difficulty)
			self.scoreL = 0
			self.scoreR = 0
		except Exception as e:
			print(f"Exception form set_game: {e}", flush=True)

	async def send_updated_game(self, message):
		print(self.username, ': bisous de send_updated_game', flush=True)
		if (message == "in playing"):
			await self.send(text_data=json.dumps({"type": "game update",
										 	"message": message,
											"ballcx": self.ball.coor.x,
											"ballcy": self.ball.coor.y,
											"ballsx": self.ball.size.x,
											"ballsy": self.ball.size.y,
											"balldx": self.ball.dir.x,
											"balldy": self.ball.dir.y,
											"paddleLcx": self.paddleL.coor.x,
											"paddleLcy": self.paddleL.coor.y,
											"paddleLsx": self.paddleL.size.x,
											"paddleLsy": self.paddleL.size.y,
											"paddleLdy": self.paddleL.dir,
											"paddleRcx": self.paddleR.coor.x,
											"paddleRcy": self.paddleR.coor.y,
											"paddleRsx": self.paddleR.size.x,
											"paddleRsy": self.paddleR.size.y,
											"paddleRdy": self.paddleR.dir,
											"scoreL": self.scoreL,
											"scoreR": self.scoreR}))
			self.paddleL, self.paddleR, self.ball, self.scoreL, self.scoreR = gameUpdate(self.paddleL, self.paddleR, self.ball, self.scoreL, self.scoreR)
			print(self.username, ': paddleLdir = ', self.paddleL.dir, flush=True)
			# FPS choix a tester, pour l'instant sleep(0.2)
			await asyncio.sleep(1 / 20)			
		elif (message == "game is finished"):
			await self.send(text_data=json.dumps({"type": "game update",
										 	"message": message,
											"player1id": self.player1id,
											"player2id": self.player2id,
											"player1Name": self.player1Name,
											"player2Name": self.player2Name,
											"scoreL": self.scoreL,
											"scoreR": self.scoreR}))

	async def quit(self, event):
		print(self.username, ': bisous de quit', flush=True)
		message = event["message"]
		await self.send(text_data=json.dumps({"type": "end game", "message": message}))
		await self.close()
