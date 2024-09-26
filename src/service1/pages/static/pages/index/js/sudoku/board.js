import { isValidSudoku, isBoardComplete } from './valid.js';
import { showModal } from './modal.js';

var numSelected = null;
var tileSelected = null;
let board = null;

export function setBoard(newboard)
{
	board = newboard;
}

export function setGame(socket) {
	//Digits 1-9

	for (let i = 1; i<=9; i++) {
		let number = document.createElement("div");
		number.id = i;
		number.innerText = i;
		number.addEventListener("click", selectNumber);
		number.classList.add("number");
		document.getElementById("digits").appendChild(number);
	}
	
	//console.log()
	// Board 9x9
	for (let r = 0; r < 9; r++) {
		for (let c = 0; c < 9; c++) {
			let tile = document.createElement("div");
			tile.id = r.toString() + "-" + c.toString();
			if (board[r][c] != 0)
			{
				tile.innerText = board[r][c];
				tile.classList.add("tile-start");
			}
			if (r == 0 && c == 0) {
				tile.classList.add("corner-top-left");
			}
			if (r == 0 && c == 8) {
				tile.classList.add("corner-top-right");
			}
			if (r == 8 && c == 0) {
				tile.classList.add("corner-bottom-left");
			}
			if (r == 8 && c == 8) {
				tile.classList.add("corner-bottom-right");
			}
			if (r == 2 || r == 5) {
				tile.classList.add("horizontal-line");
			}
			if (c == 2 || c == 5) {
				tile.classList.add("vertical-line");
			}
			if (r == 0) {
				tile.classList.add("horizontal-top-line");
			}
			if (r == 8) {
				tile.classList.add("horizontal-bottom-line");
			}
			if (c == 0) {
				tile.classList.add("vertical-left-line");
			}
			if (c == 8) {
				tile.classList.add("vertical-right-line");
			}
			if (r == 0 || r == 8) {
				tile.classList.add("outer-line");
			}
			if (c == 0 || c == 8) {
				tile.classList.add("outer-line");
			}
			tile.addEventListener("click", function () {
				selectTile.call(this, socket);  // `this` refers to the clicked tile
			});
			tile.classList.add("tile");
			document.getElementById("board").appendChild(tile);
		}
	}
	document.addEventListener("keydown", handleKeyPress);
}

function selectNumber() {
	if (numSelected != null) {
		numSelected.classList.remove("number-selected");
	}
	numSelected = this;
	numSelected.classList.add("number-selected");
}

function selectTile(socket) {
		if (numSelected) {
			if (this.classList.contains("tile-start")) {
				return;
			}
			this.innerText = numSelected.id;
			// Mettre à jour la grille de jeu
			const [row, col] = this.id.split('-').map(Number);
			board[row][col] = Number(numSelected.id); // Met à jour le tableau board
			numSelected.classList.remove("number-selected");
			numSelected = null;
			this.classList.remove("tile-selected");
			tileSelected = null;
			clearHighlights();
		}

		// Vérifier la validité de la grille
		if (!isValidSudoku(board)) {
			console.log("Grille invalide");
		}

		// Vérifier si le jeu est terminé
		if (isBoardComplete(board) && isValidSudoku(board)) {
			const timeUsed = document.getElementById("timer").innerText;
			socket.send(JSON.stringify({
				'type': 'board_complete',
				'message': 'Board completed!',
				'time_used': timeUsed,
				"is_winner": true
			}));
			showModal(true, timeUsed);
		}

		if (tileSelected != null) {
			tileSelected.classList.remove("tile-selected");
			clearHighlights();
		}
		tileSelected = this;
		tileSelected.classList.add("tile-selected");
		highlightRelatedTiles(tileSelected); // Mettre en évidence les cases liées
		let number = tileSelected.innerText;
		if (number != 0) {
			highlightSameNumberTiles(number); // Mettre en évidence les chiffres similaires
		}
}

function handleKeyPress(event) {
	if (tileSelected && !tileSelected.classList.contains("tile-start")) {
		let key = event.key;
		if (key >= '1' && key <= '9') {
			tileSelected.innerText = key;
			// Mettre à jour la grille de jeu
            const [row, col] = tileSelected.id.split('-').map(Number);
            board[row][col] = Number(key); // Met à jour le tableau board
			tileSelected.classList.remove("tile-selected"); // Retirer la couleur temporaire lors de la saisie
			tileSelected = null;
			clearHighlights();
		}
	}
}

function highlightRelatedTiles(tile) {
	let [row, col] = tile.id.split("-").map(Number);

	// Highlight row and column
	for (let i = 0; i < 9; i++) {
		document.getElementById(row + "-" + i).classList.add("tile-highlight");
		document.getElementById(i + "-" + col).classList.add("tile-highlight");
	}

	// Highlight 3x3 square
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
