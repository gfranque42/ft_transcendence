# sudokubattle/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import SudokuRoom, myUser
from django.utils import timezone

def get_player1(room):
    return room.player1

def get_player2(room):
    return room.player2

# make a global variable username
myusername = ""
room_closed = False

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

        if room.is_full and not room.is_completed:
            user = await sync_to_async(get_player2)(room)
            myusername = user.username
            await self.send_start_game(room)
        else:
            user = await sync_to_async(get_player1)(room)
            myusername = user.username

    async def disconnect(self, close_code):
        # Leave room group

        room = await sync_to_async(SudokuRoom.objects.get)(url=self.room_name)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        print(message_type)
        room = await sync_to_async(SudokuRoom.objects.get)(url=self.room_name)
        player1 = await sync_to_async(get_player1)(room)
        player2 = await sync_to_async(get_player2)(room)

        if message_type == 'board_complete':
            room.is_completed = True
            room_closed = true
            time_used = data.get('time_used')
            username = data.get('username')


            if player1.username == username and player2:
                loser = player2.username
                loserId = player2.id
                winnerId = player1.id
            else:
                loser = player1.username
                loserId = player1.id
                winnerId = player2.id

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'board_complete',
                    'message': data['message'],
                    'time_used': time_used,
                    'winner': username,
                    'loser': loser,
                    'loser_id': loserId,
                    'winner_id': winnerId
                }
            )
        if message_type == 'user_left':
            room.is_completed = True
            room_closed = true
            loserUsername = data.get('user')
            winnerUsername = data.get('adversary')

            if player1.username == loserUsername and player2:
                loserId = player1.id
                winnerId = player2.id
            elif player2:
                loserId = player2.id
                winnerId = player1.id

            if player2:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'board_complete',
                        'message': 'Your opponent has left the game. You win by disconnection!',
                        'time_used': 'N/A',
                        'winner': winnerUsername,
                        'loser': loserUsername,
                        'loser_id': loserId,
                        'winner_id': winnerId
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'close_room',
                        'user': loserUsername
                    }
                )

    async def board_complete(self, event):
        message = event['message']
        time_used = event.get('time_used')
        winner = event.get('winner')
        loser = event.get('loser')
        winner_id = event.get('winner_id')
        loser_id = event.get('loser_id')

        # Broadcast the board complete message to both players with the winner details
        await self.send(text_data=json.dumps({
            'type': 'board_complete',
            'message': message,
            'time_used': time_used,
            'winner': winner,
            'loser': loser,
            'winner_id': winner_id,
            'loser_id': loser_id
        }))

    async def close_room(self, event):
        user = event.get('user')

        # Broadcast the board complete message to both players with the winner details
        await self.send(text_data=json.dumps({
            'type': 'close_room',
            'user': user
        }))

    async def send_start_game(self, room):
        board = room.board

        user = await sync_to_async(get_player1)(room)
        other_user = await sync_to_async(get_player2)(room)

        start_time = timezone.now()
        await sync_to_async(setattr)(room, 'start_time', start_time)
        await sync_to_async(room.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_start',
                'message': 'Both players are connected. The game is starting!',
                'board': board,
                'time': start_time.isoformat(),
                'username': user.username,
                'adversary': other_user.username
            }
        )
    
    async def game_start(self, event):
        message = event['message']
        board = event['board']
        start_time = event['time']
        username = event['username']
        adversary = event['adversary']

        # Send the "game start" message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_start',
            'message': message,
            'board': board,
            'time': start_time,
            'username': username,
            'adversary': adversary
        }))
