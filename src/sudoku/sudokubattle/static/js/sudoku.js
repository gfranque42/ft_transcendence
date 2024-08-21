import { setGame } from './board.js';
import { startTimer } from './timer.js';
import { showModal } from './modal.js';
let sudokuSocket = null;

export function initializeWebSocket(roomName) {

	if (!roomName) {
		console.error("Room name is not provided!");
		return;
	}

	const socket = new WebSocket(
		'ws://' + window.location.host + '/ws/sudokubattle/' + roomName + '/'
	);

	socket.onclose = function(e) {
		console.error('Sudoku socket closed unexpectedly');
	};

	return socket;
}

function handleSocketMessage(e) {
	const data = JSON.parse(e.data);
	if (data.type === 'board_complete') {
		// Show the game result modal
		const timeUsed = data.time_used || "N/A";  // Assuming winner_time is sent
		const isWinner = data.is_winner || false;  // Assuming the current player won

		//TODO : Use the username to display the winner's time and the you lost / won message
		showModal(isWinner, timeUsed);  // Assuming the current player lost
	}
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
		sudokuSocket.onmessage = handleSocketMessage;
		setGame(sudokuSocket);
		startTimer();
	}
}

export {sudokuSocket};

document.addEventListener('DOMContentLoaded', initialize);
