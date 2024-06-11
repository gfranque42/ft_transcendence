from django.shortcuts import render, HttpResponse
import json
import random
from .utils import generate_sudoku
# Create your views here.

def home(request):
	return render(request, "sudoku.html")

def sudoku_board(request):
	board = generate_sudoku()
	context = {
		'board': json.dumps(board)
	}
	return render(request, 'sudoku.html', context)
