import { setBoard, setGame } from './board.js';
import { startTimer, setStartTime } from './timer.js';
import { showModal } from './modal.js';
let sudokuSocket = null;

export function initializeWebSocket(roomName) {

	if (!roomName) {
		console.error("Room name is not provided!");
		return;
	}

	const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';

	// Initialize the WebSocket with the correct protocol
	const socket = new WebSocket(
		`${wsProtocol}://${window.location.host}/ws/sudokubattle/${roomName.value}/`
	);

	socket.onclose = function(e) {
		console.error('Sudoku socket closed unexpectedly');
	};

	return socket;
}

function handleSocketMessage(e) {
	const data = JSON.parse(e.data);
	if (data.type === 'game_start') {
		console.log('Game is starting! Setting the board...');

		// Get the board from the message and pass it to setBoard function
		const board = data.board;
		const startTime = data.time;

		setStartTime(startTime);
		startTimer();
		setBoard(board);
		setGame(sudokuSocket);
	}

	if (data.type === 'board_complete') {
		// Show the game result modal
		const timeUsed = data.time_used || "N/A";  // Assuming winner_time is sent
		const isWinner = data.is_winner || false;  // Assuming the current player won

		//TODO : Use the username to display the winner's time and the you lost / won message
		showModal(isWinner, timeUsed);  // Assuming the current player lost
	}
}

export function initialize() {
	const roomName = document.getElementById('room-name');  // Retrieve the room name from the hidden input
	if (!roomName) {
		console.error("Room name is not available in the HTML!");
		return;
	}
	console.log('Room name:', roomName);

	// Initialize WebSocket and assign to sudokuSocket
	const sudokuSocket = initializeWebSocket(roomName);
	if (sudokuSocket) {
		sudokuSocket.onmessage = handleSocketMessage;
	}
}

document.addEventListener('DOMContentLoaded', initialize);
