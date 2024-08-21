# sudokubattle/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SudokuConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'sudoku_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        print(message_type)
        if message_type == 'board_complete':
            time_used = data.get('time_used')
            is_winner = data.get('is_winner')
            # Broadcast the completion message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'board_complete',
                    'message': data['message'],
                    'time_used': time_used,
                    'is_winner': is_winner
                }
            )

    async def board_complete(self, event):
        message = event['message']
        time_used = event.get('time_used')
        is_winner = event.get('is_winner')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'board_complete',
            'message': message,
            'time_used': time_used,
            'is_winner': event.get('is_winner')
        }))