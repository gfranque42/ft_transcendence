# sudokubattle/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import SudokuRoom
from django.utils import timezone

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

        room = await sync_to_async(SudokuRoom.objects.get)(url=self.room_name)

        if room.is_full:
            await self.send_start_game(room)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            # maybe leave the SudokuRoom too
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
        
    async def send_start_game(self, room):
        board = room.board
        
        start_time = timezone.now().isoformat()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_start',
                'message': 'Both players are connected. The game is starting!',
                'board': board,
                'time': start_time
            }
        )
    
    async def game_start(self, event):
        message = event['message']
        board = event['board']
        start_time = event['time']

        # Send the "game start" message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_start',
            'message': message,
            'board': board,
            'time': start_time
        }))
