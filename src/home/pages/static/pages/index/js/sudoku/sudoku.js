import { setBoard, setCurrentUser, setGame, setSocket } from './board.js';
import { startTimer, setStartTime, stopTimer } from './timer.js';
import { showModal } from './modal.js';
import { getUser } from '../getUser.js';
import { sendGameResults } from './sendGameResults.js';

let currentUser = null;
let gameended = false;

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
		console.log('entered the close function');
		if (gameended === false) {
			const link = document.createElement('a');
			link.href = '/sudoku/';
			link.setAttribute('data-link', '');
			document.body.appendChild(link);
			console.log(link);
			link.click();
			document.body.removeChild(link);
		}
	};

	return socket;
}

function handleSocketMessage(e) {
	const data = JSON.parse(e.data);
	console.log('Received message:', data);
	if (data.type === 'game_start') {
		console.log('Game is starting! Setting the board...');

		// Get the board from the message and pass it to setBoard function
		const board = data.board;
		const startTime = data.time;

		console.log("data: ", data);

		setStartTime(startTime);
		startTimer();
		setBoard(board);
		setCurrentUser(currentUser);
		setGame();
	}

	if (data.type === 'board_complete') {
		// Show the game result modal
		gameended = true;
		const timeUsed = data.time_used || "N/A";
		const winningUser = data.winner || "N/A";
		//const winningTime = data.winner_time || "N/A";

		const winningId = data.winner_id;
		const losingId = data.loser_id;
		console.log(data);

		showModal(timeUsed, winningUser, currentUser);
		console.log(winningId, losingId);
		if (currentUser === winningUser)
			sendGameResults(winningId, losingId, 1, 0);
		stopTimer();
	}
}

export async function initialize(sudokuSocket) {
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
		setSocket(sudokuSocket);
		sudokuSocket.onmessage = handleSocketMessage;
	}
}

document.addEventListener('DOMContentLoaded', initialize);
