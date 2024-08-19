# sudoku/utils.py
import random

def is_valid(board, row, col, num):
	for x in range(9):
		if board[row][x] == num or board[x][col] == num:
			return False

	start_row, start_col = 3 * (row // 3), 3 * (col // 3)
	for i in range(3):
		for j in range(3):
			if board[i + start_row][j + start_col] == num:
				return False
	return True

def solve_sudoku(board):
	for row in range(9):
		for col in range(9):
			if board[row][col] == 0:
				for num in range(1, 10):
					if is_valid(board, row, col, num):
						board[row][col] = num
						if solve_sudoku(board):
							return True
						board[row][col] = 0
				return False
	return True

def remove_elements(board, difficulty):
	if difficulty == 0:
		removals = 1
	elif difficulty == 2:
		removals = 50
	else:
		removals = 36

	while removals > 0:
		row = random.randint(0, 8)
		col = random.randint(0, 8)
		if board[row][col] != 0:
			board[row][col] = 0
			removals -= 1
	return board

def generate_sudoku(difficulty):
	board = [[0 for _ in range(9)] for _ in range(9)]
	# Remplir aléatoirement quelques cellules pour générer des grilles différentes
	for _ in range(10):
		row = random.randint(0, 8)
		col = random.randint(0, 8)
		num = random.randint(1, 9)
		while not is_valid(board, row, col, num) or board[row][col] != 0:
			row = random.randint(0, 8)
			col = random.randint(0, 8)
			num = random.randint(1, 9)
		board[row][col] = num
	
	solve_sudoku(board)
	board = remove_elements(board, difficulty)
	return board
