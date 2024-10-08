import { setBoard, setCurrentUser, setGame, setSocket } from './board.js';
import { startTimer, setStartTime, stopTimer } from './timer.js';
import { showModal } from './modal.js';
import { getUser } from '../getUser.js';
import { sendGameResults } from './sendGameResults.js';
import { navigateTo } from '../index.js';
import sudoku from '../../views/sudoku.js';

let currentUser = null;
let gameended = false;
let sudokuSocket = null;
let adversary = null;

export function initializeWebSocket(roomName) {

	if (!roomName) {
		console.error("Room name is not provided!");
		return;
	}

	if (sudokuSocket !== null) {
		console.log("WebSocket is already initialized!");
		sudokuSocket.close();
		sudokuSocket = null;
	}

	const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';

	// Initialize the WebSocket with the correct protocol
	const socket = new WebSocket(
		`${wsProtocol}://${window.location.host}/ws/sudokubattle/${roomName.value}/`
	);

	socket.onclose = function(e) {
		console.log('entered the close function');
		sudokuSocket = null;
		gameended = false;
		currentUser = null;
		adversary = null;
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
		adversary = data.adversary;

		console.log("data: ", data);

		setStartTime(startTime);
		startTimer();
		setBoard(board);
		setSocket(sudokuSocket);
		setCurrentUser(currentUser);
		setGame();
	}

	if (data.type === 'board_complete') {
		// Show the game result modal
		if (gameended !== true) {
			gameended = true;
			const timeUsed = data.time_used || "N/A";
			const winningUser = data.winner || "N/A";
			//const winningTime = data.winner_time || "N/A";

			const winningId = data.winner_id;
			const losingId = data.loser_id;

			showModal(timeUsed, winningUser, currentUser);
			if (currentUser === winningUser)
				sendGameResults(winningId, losingId, 1, 0);
			stopTimer();
			if (sudokuSocket) {
				sudokuSocket.close();
			}
		}
	}

	if (data.type === 'close_room') {
		console.log('Room is closing! Redirecting to home page...');
		gameended = true;
		navigateTo('/sudoku/');
		if (sudokuSocket) {
			sudokuSocket.close();
		}
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
	
	sudokuSocket = initializeWebSocket(roomName);
	if (sudokuSocket) {
		sudokuSocket.onmessage = handleSocketMessage;
	}

	window.addEventListener('popstate', function (event) {
		if (roomName && window.location.pathname !== `/sudoku/${roomName.value}/`) {

			if (sudokuSocket) {
				sudokuSocket.send(JSON.stringify({
					'type': 'user_left',
					'username': currentUser,
					'adversary': adversary
				}));
			}
		}
	});

	window.addEventListener('beforeunload', function (event) {
		if (roomName) {
			if (sudokuSocket) {
				sudokuSocket.send(JSON.stringify({
					'type': 'user_left',
					'username': currentUser,
					'adversary': adversary
				}));
			}
			navigateTo('/sudoku/');
		}
	});
}

document.addEventListener('DOMContentLoaded', initialize);
