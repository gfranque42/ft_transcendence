import { setGame } from './board.js';
import { startTimer } from './timer.js';

function initializeWebSocket(roomName) {
	const socket = new WebSocket(
		'ws://' + window.location.host + '/ws/sudoku/' + roomName + '/'
	);

	socket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		if (data.type === 'board_complete') {
			alert(data.message);  // Notify players
			// Stop the game logic
			document.querySelectorAll('.cell').forEach(cell => {
				cell.disabled = true;  // Disable further input
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
