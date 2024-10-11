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

        if room.is_full and not room.is_completed and room.multiplayer:
            user = await sync_to_async(get_player2)(room)
            await self.send_start_game(room)
        elif not room.multiplayer:
            print("Solo game")
            user = await sync_to_async(get_player1)(room)
            await self.send_solo_start_game(room)
        else:
            user = await sync_to_async(get_player1)(room)

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
        
        # Fetch the room and players
        room = await sync_to_async(SudokuRoom.objects.get)(url=self.room_name)
        multiplayer = room.multiplayer
        player1 = await sync_to_async(get_player1)(room)
        player2 = await sync_to_async(get_player2)(room) if multiplayer and room.is_full else None
        
        # Mark room as completed
        room.is_completed = True
        await sync_to_async(room.save)()
        
        if message_type == 'board_complete':
            await self.handle_board_complete(data, player1, player2, multiplayer)
        elif message_type == 'user_left':
            await self.handle_user_left(data, player1, player2, multiplayer)

    async def handle_board_complete(self, data, player1, player2, multiplayer):
        time_used = data.get('time_used')
        username = data.get('username')
        message = data.get('message')
        
        if not multiplayer:
            # Single-player game
            winner = player1
            message_data = {
                'type': 'board_complete',
                'message': message,
                'time_used': time_used,
                'winner': winner.username,
                'winner_id': winner.id,
                'multiplayer': multiplayer
            }
        else:
            # Multi-player game
            if player1.username == username:
                winner, loser = player1, player2
            else:
                winner, loser = player2, player1
            message_data = {
                'type': 'board_complete',
                'message': message,
                'time_used': time_used,
                'winner': winner.username,
                'winner_id': winner.id,
                'loser': loser.username,
                'loser_id': loser.id,
                'multiplayer': multiplayer
            }
        
        await self.channel_layer.group_send(self.room_group_name, message_data)

    async def handle_user_left(self, data, player1, player2, multiplayer):
        loser_username = data.get('username')
        winner_username = data.get('adversary')
        
        if not multiplayer or not player2:
            # Not a multi-player game or no opponent; close the room
            message_data = {
                'type': 'close_room',
                'user': loser_username,
                'multiplayer': multiplayer
            }
        else:
            # Determine winner and loser based on usernames
            if player1.username == loser_username:
                loser, winner = player1, player2
            else:
                loser, winner = player2, player1
            
            message_data = {
                'type': 'board_complete',
                'message': 'Your opponent has left the game. You win by disconnection!',
                'time_used': 'N/A',
                'winner': winner.username,
                'winner_id': winner.id,
                'loser': loser.username,
                'loser_id': loser.id,
                'multiplayer': multiplayer
            }
        
        await self.channel_layer.group_send(self.room_group_name, message_data)

    async def board_complete(self, event):
        message = event['message']
        time_used = event.get('time_used')
        winner = event.get('winner')
        winner_id = event.get('winner_id')
        multiplayer = event.get('multiplayer')

        if multiplayer:
            print("I AM IN THE MULTIPLAYER BOARD_COMPLETE")
            loser = event.get('loser')
            loser_id = event.get('loser_id')

            await self.send(text_data=json.dumps({
                'type': 'board_complete',
                'message': message,
                'time_used': time_used,
                'winner': winner,
                'winner_id': winner_id,
                'loser': loser,
                'loser_id': loser_id
            }))
        else:
            print("I AM IN THE SOLO BOARD_COMPLETE")
            await self.send(text_data=json.dumps({
                'type': 'board_complete',
                'message': message,
                'time_used': time_used,
                'winner': winner,
                'winner_id': winner_id,
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
        room.start_time = start_time
        await sync_to_async(room.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_start',
                'message': 'Both players are connected. The game is starting!',
                'board': board,
                'time': start_time.isoformat(),
                'username': user.username,
                'multiplayer': True,
                'adversary': other_user.username
            }
        )

    async def send_solo_start_game(self, room):
        board = room.board

        user = await sync_to_async(get_player1)(room)
        start_time = timezone.now()
        # await sync_to_async(setattr)(room, 'start_time', start_time)
        # await sync_to_async(setattr)(room, 'is_full', True)
        room.start_time = start_time
        room.is_full = True
        await sync_to_async(room.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_start',
                'message': 'The game is starting!',
                'board': board,
                'time': start_time.isoformat(),
                'username': user.username,
                'multiplayer': False
            }
        )

    async def game_start(self, event):
        message = event['message']
        board = event['board']
        start_time = event['time']
        username = event['username']
        multiplayer = event['multiplayer']
        if multiplayer:
            adversary = event['adversary']
            await self.send(text_data=json.dumps({
                'type': 'game_start',
                'message': message,
                'board': board,
                'time': start_time,
                'username': username,
                'multiplayer': multiplayer,
                'adversary': adversary
            }))
        else:
            await self.send(text_data=json.dumps({
                'type': 'game_start',
                'message': message,
                'board': board,
                'time': start_time,
                'username': username,
                'multiplayer': multiplayer
            }))
