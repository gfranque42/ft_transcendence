import { setGame } from './board.js';
import { startTimer } from './timer.js';

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

const roomName = document.getElementById('room-name').value;  // Assume you have an element with the room name
const sudokuSocket = initializeWebSocket(roomName);

window.onload = function() {
	setGame(sudokuSocket);
	startTimer();
}
