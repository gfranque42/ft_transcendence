import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Room, Player

class	PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
		self.room_group_name = "pong_%s" % self.room_name
		
		try:
			room = await self.get_room(self.room_name)
			if await room_is_full(room)
				await self.close()
			else
				await self.channel_layer.group_add(self.room_group_name, self.channel_name)
				await self.accept()
		except:
			await self.close()

	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]

		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name, {"type": "chat_message", "message": message}
		)

	# Receive message from room group
	async def chat_message(self, event):
		message = event["message"]

		# Send message to WebSocket
		await self.send(text_data=json.dumps({"message": message}))

	@sync_to_async
	def get_room(self, room_name):
		return (Room.objects.get(url=room_name))

	@sync_to_async
	def room_is_full(self, room):
		return (room.players.count() >= room.maxPlayers)

	@sync_to_async
	def	add_player_to_room(self, room):
		player, created = Player.objects.get_or_create(username="current_player")
		room.players.add(player)




