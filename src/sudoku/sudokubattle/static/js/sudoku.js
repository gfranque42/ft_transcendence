import { setGame } from './board.js';
import { startTimer } from './timer.js';
let sudokuSocket = null;

export function initializeWebSocket(roomName) {

	if (!roomName) {
		console.error("Room name is not provided!");
		return;
	}

	const socket = new WebSocket(
		'ws://' + window.location.host + '/ws/sudokubattle/' + roomName + '/'
	);

	socket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		if (data.type === 'board_complete') {
			alert(data.message);  // Notify players
			// Stop the game logic by disabling all tiles
			document.querySelectorAll('.tile').forEach(tile => {
				tile.removeEventListener("click", selectTile);  // Remove the event listener
				tile.classList.add("tile-disabled");  // Optionally, add a disabled class for styling
			});
		}
	};

	socket.onclose = function(e) {
		console.error('Sudoku socket closed unexpectedly');
	};

	return socket;
}

function initialize() {
	const roomName = document.getElementById('room-name').value;  // Retrieve the room name from the hidden input
	if (!roomName) {
		console.error("Room name is not available in the HTML!");
		return;
	}
	console.log('Room name:', roomName);

	// Initialize WebSocket and assign to sudokuSocket
	sudokuSocket = initializeWebSocket(roomName);
	if (sudokuSocket) {
		setGame(sudokuSocket);
		startTimer();
	}
}

export {sudokuSocket};

document.addEventListener('DOMContentLoaded', initialize);
