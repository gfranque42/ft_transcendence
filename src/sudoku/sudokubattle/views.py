from django.shortcuts import render, HttpResponse, get_object_or_404
import json
import random
from .utils import generate_sudoku, generate_random_url
from django.utils import timezone
from .models import SudokuRoom
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
	try:
		data = json.loads(request.body)
		difficulty = data.get('difficulty')

		current_user = request.user

		available_room = SudokuRoom.objects.filter(
			difficulty=difficulty,
			is_full=False,
		).exclude(player1=current_user).first()

		if available_room:
			available_room.add_player(current_user)

			return JsonResponse({
				'status': 'Joined existing room',
				'roomUrl': f'/sudoku/game/{available_room.url}/'
			}, status=200)
		else:
			room_url = generate_random_url()
			
			board = generate_sudoku(difficulty)
			
			room = SudokuRoom.objects.create(
				url=room_url,
				difficulty=difficulty,
				board=board,
				player1=current_user
			)
			return JsonResponse({'status': 'Room created', 'roomUrl': room_url, 'board': board}, status=201)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=400)


def sudoku_board(request, room_url):
	if request.method == 'GET':
		room = get_object_or_404(SudokuRoom, url=room_url)
		if room.is_full:
			context = {
				'board': room.board,
				'room_url': room.url,
				'player1': room.player1,
				'player2': room.player2,
			}
			return render(request, 'sudokubattle/game_room.html', context)
		else:
			context = {
				'room_url': room.url,
				'message': 'Waiting for another player to join...'
			}
			return render(request, 'sudokubattle/waiting.html', context)
	else:
		return HttpResponse(status=405)
