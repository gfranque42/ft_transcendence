from django.shortcuts import render, HttpResponse
import json
import random
from .utils import generate_sudoku
from django.utils import timezone
# Create your views here.

rooms = {}

def home(request):
	return render(request, "sudokubattle/room.html")

def sudoku_board(request, room_name):
	if room_name not in rooms:
		board = generate_sudoku()
		start_time = timezone.now().isoformat()
		rooms[room_name] = {'board': board, 'start_time': start_time}
	else:
		board = rooms[room_name]['board']
		start_time = rooms[room_name]['start_time']
	
	context = {
		'board': json.dumps(board),
		'start_time': start_time
	}
	return render(request, 'sudokubattle/sudoku.html', context)
