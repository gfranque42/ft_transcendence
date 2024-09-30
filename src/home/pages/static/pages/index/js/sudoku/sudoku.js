import { setBoard, setCurrentUser, setGame, setSocket } from './board.js';
import { startTimer, setStartTime } from './timer.js';
import { showModal } from './modal.js';
import { getUser } from '../getUser.js';
import { sendGameResults } from './sendGameResults.js';

let sudokuSocket = null;
let currentUser = null;

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

		console.log("data: ", data);
		console.log("users are before set: ", currentUser);

		setStartTime(startTime);
		startTimer();
		setBoard(board);
		setSocket(sudokuSocket);
		setCurrentUser(currentUser);
		setGame();
	}

	if (data.type === 'board_complete') {
		// Show the game result modal
		const timeUsed = data.time_used || "N/A";
		const winningUser = data.winner || "N/A";
		const losingUser = data.loser || "N/A";
		//const winningTime = data.winner_time || "N/A";
		console.log("users are: ", winningUser, losingUser);

		showModal(timeUsed, winningUser, currentUser);  // Assuming the current player lost
		sendGameResults(winningUser, losingUser, 1, 0);
	}
}

export async function initialize() {
	const roomName = document.getElementById('room-name');
	const userInfo = await getUser();

	if (!roomName) {
		console.error("Room name is not available in the HTML!");
		return;
	}

	currentUser = userInfo.Username;
	console.log('Current user:', currentUser);
	// Initialize WebSocket and assign to sudokuSocket
	sudokuSocket = initializeWebSocket(roomName);
	if (sudokuSocket) {
		sudokuSocket.onmessage = handleSocketMessage;
	}
}

document.addEventListener('DOMContentLoaded', initialize);
