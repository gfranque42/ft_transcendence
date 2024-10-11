import { isValidSudoku, isBoardComplete } from './valid.js';

var numSelected = null;
var tileSelected = null;
let board = null;
let socket = null;
let currentUser = null;

export function setBoard(newboard)
{
	board = newboard;
}

export function setCurrentUser(newuser)
{
	currentUser = newuser;
}

export function setSocket(newsocket)
{
	socket = newsocket;
}

export function setGame() {
	//Digits 1-9

	const boardContainer = document.getElementById("board");
	boardContainer.innerHTML = '';

	const digitsContainer = document.getElementById("digits");
	digitsContainer.innerHTML = '';

	for (let i = 1; i<=9; i++) {
		let number = document.createElement("div");
		number.id = i;
		number.innerText = i;
		number.addEventListener("click", selectNumber);
		number.classList.add("number");
		document.getElementById("digits").appendChild(number);
	}

	for (let r = 0; r < 9; r++) {
		for (let c = 0; c < 9; c++) {
			let tile = document.createElement("div");
			tile.id = `${r}-${c}`; // Set tile ID as row-col format
			tile.classList.add("tile");

			// Set initial value if it's not 0
			if (board[r][c] != 0) {
				tile.innerText = board[r][c];
				tile.classList.add("tile-start");
			}

			tile.addEventListener("click", selectTile);
			boardContainer.appendChild(tile);
		}
	}

	document.addEventListener("keydown", handleKeyPress);

	document.addEventListener("click", (event) => {
		if (!event.target.classList.contains("tile") && !event.target.classList.contains("number")) {
			clearHighlights();
			if (tileSelected) {
				tileSelected.classList.remove("tile-selected");
				tileSelected = null;
			}
			if (numSelected) {
				numSelected.classList.remove("number-selected");
				numSelected = null;
			}
		}
	});
}

function selectNumber() {
	if (numSelected != null) {
		numSelected.classList.remove("number-selected");
	}
	numSelected = this;
	numSelected.classList.add("number-selected");
}

function selectTile() {
		if (numSelected) {
			if (this.classList.contains("tile-start")) {
				return;
			}
			this.innerText = numSelected.id;
			const [row, col] = this.id.split('-').map(Number);
			board[row][col] = Number(numSelected.id);
			numSelected.classList.remove("number-selected");
			numSelected = null;
			this.classList.remove("tile-selected");
			tileSelected = null;
			clearHighlights();
		}

		if (tileSelected != null) {
			tileSelected.classList.remove("tile-selected");
			clearHighlights();
		}
		tileSelected = this;
		tileSelected.classList.add("tile-selected");
		highlightRelatedTiles(tileSelected);
		let number = tileSelected.innerText;
		if (number != 0) {
			highlightSameNumberTiles(number);
		}

		if (!isValidSudoku(board)) {
			console.log("Grille invalide");
		}

		if (isBoardComplete(board) && isValidSudoku(board)) {
			console.log("Grille complète");
			const timeUsed = document.getElementById("timer").innerText;
			socket.send(JSON.stringify({
				'type': 'board_complete',
				'message': 'Board completed!',
				'time_used': timeUsed,
				'username': currentUser,
			}));
		}
}

function handleKeyPress(event) {
	if (tileSelected && !tileSelected.classList.contains("tile-start")) {
		let key = event.key;
		if (key >= '1' && key <= '9') {
			tileSelected.innerText = key;
            const [row, col] = tileSelected.id.split('-').map(Number);
            board[row][col] = Number(key);
			tileSelected.classList.remove("tile-selected");
			tileSelected = null;
			clearHighlights();
		}
		if (key == 'Backspace' || key == 'Delete') {
			tileSelected.innerText = '';
			const [row, col] = tileSelected.id.split('-').map(Number);
			board[row][col] = 0;
			tileSelected.classList.remove("tile-selected");
			tileSelected = null;
			clearHighlights();
		}
	}

	if (!isValidSudoku(board)) {
		console.log("Grille invalide");
	}

	if (isBoardComplete(board) && isValidSudoku(board)) {
		console.log("Grille complète");
		const timeUsed = document.getElementById("timer").innerText;
		socket.send(JSON.stringify({
			'type': 'board_complete',
			'message': 'Board completed!',
			'time_used': timeUsed,
			'username': currentUser,
		}));
	}
}

function highlightRelatedTiles(tile) {
	let [row, col] = tile.id.split("-").map(Number);

	for (let i = 0; i < 9; i++) {
		document.getElementById(row + "-" + i).classList.add("tile-highlight");
		document.getElementById(i + "-" + col).classList.add("tile-highlight");
	}

	let startRow = Math.floor(row / 3) * 3;
	let startCol = Math.floor(col / 3) * 3;
	for (let r = startRow; r < startRow + 3; r++) {
		for (let c = startCol; c < startCol + 3; c++) {
			document.getElementById(r + "-" + c).classList.add("tile-highlight");
		}
	}
}

function highlightSameNumberTiles(number) {
	let tiles = document.querySelectorAll(".tile");
	tiles.forEach(tile => {
		if (tile.innerText === number) {
			tile.classList.add("tile-highlight");
		}
	});
}

function clearHighlights() {
	let highlightedTiles = document.querySelectorAll(".tile-highlight");
	highlightedTiles.forEach(tile => {
		tile.classList.remove("tile-highlight");
	});
}
