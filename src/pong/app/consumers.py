import json
# from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer

# class	PongConsumer(AsyncWebsocketConsumer):
# 	async def connect(self):
# 		self.room_name = self.scope["url_route"]["kwargs"]["uri"]
# 		self.room_group_name = f"chat_{self.room_name}"
# 		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		
# 		await self.accept()
	
# 	async def disconnect(self, close_code):
# 		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

# 	# je recois un message par la websocket
# 	async def receive(self, text_data):
# 		text_data_json = json.loads(text_data)
# 		message = text_data_json["message"]
# 		# je l'envoie au group / aux personnes presentes dans la room
# 		await self.channel_layer.group_send(self.send(text_data=json.dumps({"message": message})))

# 	# je recois le message du groupe
# 	async def chat_message(self, event):
# 		message = event["message"]
# 		# j'envoie par la websocket le message recu par le groupe
# 		await self.send(text_data=json.dumps({"message": message}))

class	ChatConsumer(WebsocketConsumer):
	def connect(self):
		self.accept()

	def disconnect(self, close_code):
		pass

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]

		self.send(text_data=json.dumps({"message": message}))
