import { setBoard, setCurrentUser, setGame, setSocket, setRoomName } from './board.js';
import { startTimer, setStartTime, stopTimer } from './timer.js';
import { showModal } from './modal.js';
import { getUser } from '../getUser.js';
import { sendGameResults } from './sendGameResults.js';
import { navigateTo } from '../index.js';
import sudoku from '../../views/sudoku.js';
import { game } from '../../pong/pong.js';

let currentUser = null;
let gameended = false;
export let gameInProgress = false;
let sudokuSocket = null;
let adversary = null;
let multiplayer = false;
let roomName = null;
let startTime = null;

export function initializeWebSocket() {
	console.log('initializing websocket');
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
		`${wsProtocol}://${window.location.host}/ws/sudokubattle/${roomName.value}/?request_by=Home`
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
		if (!gameInProgress)
		{
			console.log('gameInProgress: ', gameInProgress);
			startTime = data.time;
			gameInProgress = true;
		}
		if (data.multiplayer === true) {
			multiplayer = true;
			adversary = data.adversary;
		}

		console.log("data: ", data);

		console.log("gameInProgress: ", gameInProgress);

		setStartTime(startTime);
		startTimer();
		setBoard(board);
		setRoomName(roomName);
		setSocket(sudokuSocket);
		setCurrentUser(currentUser);
		setGame();
	}

	if (data.type === 'board_complete') {
		// Show the game result modal
		if (gameended !== true) {
			gameended = true;
			gameInProgress = false;
			const timeUsed = data.time_used || "N/A"; // Time used to win
			const winningUser = data.winner || "N/A";
			const winningId = data.winner_id;

			if (window.location.pathname !== `/sudoku/${roomName.value}/`) {
				console.log('wrong location???');
				return;
			}
			showModal(timeUsed, winningUser, currentUser);
			if (currentUser === winningUser && multiplayer === true) {
				const losingId = data.loser_id;
				const losingUser = data.loser;
				console.log('sending game results :', losingId, winningId, losingUser, winningUser);
				sendGameResults(winningId, losingId, 1, 0);
			}
			stopTimer();
			if (sudokuSocket) {
				sudokuSocket.close();
			}
		}
	}

	if (data.type === 'close_room') {
		console.log('Room is closing! Redirecting to home page...');
		gameended = true;
		gameInProgress = false;
		navigateTo('/sudoku/');
		stopTimer();
		if (sudokuSocket) {
			sudokuSocket.close();
		}
	}
}

export function eventFunc(event) {
	console.log("eventFunc");
	if (!window.location.pathname.includes('/sudoku/'))
		return;
	const confirmation = confirm("Are you sure you want to leave? Leaving now means you will give up the game.");
	if (!confirmation) {
		console.log("event: ", event.defaultPrevented);
		// event.defaultPrevented = true;
		console.log("no confirmation in sudoku.js");
		event.preventDefault();
		event.stopPropagation();

		console.log("event: ", event.defaultPrevented);
	}
	else {
		console.log("HELLO ?? UNLOADING");
		if (sudokuSocket) {
			sudokuSocket.send(JSON.stringify({
				'type': 'user_left',
				'username': currentUser,
				'adversary': adversary || ''
			}));
		}
		console.log("leaving confirmed");
		gameInProgress = false;
		console.log(gameInProgress);
		stopTimer();
		if (sudokuSocket) {
			sudokuSocket.close();
		}
	}
}

function beforeUnloadEvent(event) {
	console.log("beforeUnloadEventFunc");
	if (!window.location.pathname.includes('/sudoku/'))
		return;
	if (gameInProgress) {
		const confirmationMessage = "Are you sure you want to leave? Leaving now means you will give up the game.";
		event.returnValue = confirmationMessage;
		return confirmationMessage;
	}
}

function handleUnload() {
	console.log("Unloading...");
	if (sudokuSocket) {
		sudokuSocket.send(JSON.stringify({
			'type': 'user_left',
			'username': currentUser,
			'adversary': adversary || ''
		}));
	}
	gameInProgress = false;
	stopTimer();
	if (sudokuSocket) {
		sudokuSocket.close();
	}
}

export async function initialize() {

	roomName = document.getElementById('room-name');
	console.log(`inirialize`);
	const userInfo = await getUser();
	if (userInfo.expired) {
		navigateTo('/login/');
		return ;
	}

	if (!roomName)
		return;
	
	sudokuSocket = initializeWebSocket();
	currentUser = userInfo.Username;
	
	console.log('sudokuSocket: ', sudokuSocket);
	if (sudokuSocket) {
		sudokuSocket.onmessage = handleSocketMessage;
	}
	
	const homeButton = document.getElementById("home");

	homeButton.addEventListener("click", eventFunc);
	// window.addEventListener('popstate', eventFunc);
	window.addEventListener('beforeunload', beforeUnloadEvent);
	window.addEventListener('unload', function(event) {
		if (window.location.pathname.includes(`/sudoku/${roomName.value}/`))
			handleUnload();
	});
}
