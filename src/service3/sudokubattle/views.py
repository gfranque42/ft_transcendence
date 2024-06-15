from django.shortcuts import render, HttpResponse
import json
import random
from .utils import generate_sudoku
from django.utils import timezone
# Create your views here.

def home(request):
	return render(request, "sudoku.html")

def sudoku_board(request):
	board = generate_sudoku()
	start_time = timezone.now().isoformat()
	context = {
		'board': json.dumps(board),
		'start_time': start_time
	}
	return render(request, 'sudoku.html', context)
