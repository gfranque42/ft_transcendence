from django.shortcuts import render, HttpResponse
import json
import random
from .utils import generate_sudoku
from django.utils import timezone
from .models import SudokuRoom
# Create your views here.

rooms = {}

def home(request):
	return render(request, "sudokubattle/lobby.html")

def create_sudoku_room(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			room_url = data['url']
			difficulty = data['difficulty']
			
			# Generate the Sudoku board here based on difficulty
			board = generate_sudoku(difficulty)
			
			# Save the room in the database
			room = SudokuRoom.objects.create(url=room_url, difficulty=difficulty, board=board)
			
			return JsonResponse({'status': 'Room created', 'roomUrl': room_url, 'board': board}, status=201)
		except Exception as e:
			return JsonResponse({'error': str(e)}, status=400)
	else:
		return JsonResponse({'error': 'Invalid request method'}, status=405)

def sudoku_board(request, room_url):
	try:
		# Attempt to retrieve the room from the database
		room = SudokuRoom.objects.get(url=room_url)
		board = room.board  # Assuming 'board' is stored as JSON in the model
		start_time = room.created_at.isoformat()  # Or store this explicitly if needed
	except SudokuRoom.DoesNotExist:
		print(f"Room {room_url} does not exist.")
		# If the room doesn't exist, create it via the create_sudoku_room logic
		# Alternatively, you could redirect to an API endpoint that creates the room
		# But here, we'll create it directly:
		board = generate_sudoku(0)
		start_time = timezone.now().isoformat()
		room = SudokuRoom.objects.create(url=room_url, difficulty=1, board=board)  # Adjust the difficulty as needed
	
	context = {
		'board': json.dumps(board),
		'start_time': start_time,
		'room_url': room_url
	}
	return render(request, 'sudokubattle/sudoku.html', context)
