from django.shortcuts import render, HttpResponse, get_object_or_404
import json
import random
from .utils import generate_sudoku, generate_random_url
from django.utils import timezone
from .models import SudokuRoom, myUser
from urllib.parse import quote
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.

rooms = {}

def home(request):
	if request.method == 'GET':
		return render(request, "sudokubattle/lobby.html")

@api_view(['POST'])
def check_or_create_sudoku_room(request):
	# try:
	data = json.loads(request.body)
	difficulty = data.get('difficulty')
	multiplayer = data.get('multiplayer')

	username = data.get('user')
	user_id = data.get('id')
	print(f"Received user_id: {user_id}, username: {username}", flush=True)

	print(f"Received myUser: {myUser.objects.get_or_create(username=username,user_id=user_id)}", flush=True)
	current_user, created = myUser.objects.get_or_create(
		username=username,
		user_id=user_id
	)

	if multiplayer == True:
		available_room = SudokuRoom.objects.filter(
			difficulty=difficulty,
			is_full=False,
			is_completed=False,
		).exclude(player1=current_user).first()

		if available_room:
			available_room.add_player(current_user)

			return JsonResponse({
				'status': 'Joined existing room',
				'roomUrl': available_room.url,
			}, status=200)
		else:
			room_url = generate_random_url()
			
			board = generate_sudoku(difficulty)
			
			room = SudokuRoom.objects.create(
				url=room_url,
				difficulty=difficulty,
				board=board,
				player1=current_user,
				multiplayer=True,
			)
			return JsonResponse({'status': 'Room created', 'roomUrl': room_url, 'board': board, 'username': username, 'multiplayer': 'true'}, status=201)
	else:
		room_url = generate_random_url()
		board = generate_sudoku(difficulty)
		
		room = SudokuRoom.objects.create(
			url=room_url,
			difficulty=difficulty,
			board=board,
			player1=current_user,
			multiplayer=False,
		)
		return JsonResponse({'status': 'Room created', 'roomUrl': room_url, 'board': board, 'username': username, 'multiplayer': 'false'}, status=201)
	# except Exception as e:
	# 	return JsonResponse({'error': str(e)}, status=400)


def sudoku_board(request, room_url):
	if request.method == 'GET':
		# Fetch the room data (no need to check is_full here)
		try:
			# room = get_object_or_404(SudokuRoom, url=room_url)
			print(f"room_url: {room_url}", flush=True)
			room = SudokuRoom.objects.get(url=room_url)
			if room.is_completed:
				return render(request, 'sudokubattle/noRoom.html')
			print(f"room: {room}", flush=True)
			print(f"room is completed: {room.is_completed}", flush=True)
			# Render a template for both players, WebSocket will manage the game state
			context = { 'room_url': room.url, }
			return render(request, 'sudokubattle/sudoku.html', context)
		except SudokuRoom.DoesNotExist:
			return render(request, 'sudokubattle/noRoom.html')
	else:
		return HttpResponse(status=405)
