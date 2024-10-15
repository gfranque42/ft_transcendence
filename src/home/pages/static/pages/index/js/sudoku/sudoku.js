import {
  setBoard,
  setCurrentUser,
  setGame,
  setSocket,
  setRoomName,
} from "./board.js";
import { startTimer, setStartTime, stopTimer } from "./timer.js";
import { showModal } from "./modal.js";
import { getUser } from "../getUser.js";
import { sendGameResults } from "./sendGameResults.js";
import { navigateTo } from "../index.js";
import sudoku from "../../views/sudoku.js";
import { game } from "../../pong/pong.js";

let currentUser = null;
let gameended = false;
export let gameInProgress = false;
let sudokuSocket = null;
let adversary = null;
let multiplayer = false;
let roomName = null;
let startTime = null;

export function initializeWebSocket() {
  if (!roomName) {
    console.error("Room name is not provided!");
    return;
  }

  if (sudokuSocket !== null) {
    sudokuSocket.close();
    sudokuSocket = null;
  }

  const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";

  const socket = new WebSocket(
    `${wsProtocol}://${window.location.host}/ws/sudokubattle/${roomName.value}/?request_by=Home`
  );

  socket.onclose = function (e) {
    sudokuSocket = null;
    gameended = false;
    currentUser = null;
    adversary = null;
  };

  return socket;
}

function handleSocketMessage(e) {
  const data = JSON.parse(e.data);
  if (data.type === "game_start") {
    const board = data.board;
    if (!gameInProgress) {
      startTime = data.time;
      gameInProgress = true;
    }
    if (data.multiplayer === true) {
      multiplayer = true;
      adversary = data.adversary;
    }

    setStartTime(startTime);
    startTimer();
    setBoard(board);
    setRoomName(roomName);
    setSocket(sudokuSocket);
    setCurrentUser(currentUser);
    setGame();
  }

  if (data.type === "board_complete") {
    if (gameended !== true) {
      gameended = true;
      gameInProgress = false;
      const timeUsed = data.time_used || "N/A";
      const winningUser = data.winner || "N/A";
      const winningId = data.winner_id;

      if (window.location.pathname !== `/sudoku/${roomName.value}/`) return;
      showModal(timeUsed, winningUser, currentUser);
      if (currentUser === winningUser && multiplayer === true) {
        const losingId = data.loser_id;
        const losingUser = data.loser;
        sendGameResults(winningId, losingId, 1, 0);
      }
      stopTimer();
      if (sudokuSocket) {
        sudokuSocket.close();
      }
    }
  }

  if (data.type === "close_room") {
    gameended = true;
    gameInProgress = false;
    navigateTo("/sudoku/");
    stopTimer();
    if (sudokuSocket) {
      sudokuSocket.close();
    }
  }
}

export function eventFunc(event) {
  if (!window.location.pathname.includes("/sudoku/")) return;
  const confirmation = confirm(
    "Are you sure you want to leave? Leaving now means you will give up the game."
  );
  if (!confirmation) {
    event.preventDefault();
    event.stopImmediatePropagation();
  } else {
    if (sudokuSocket) {
      sudokuSocket.send(
        JSON.stringify({
          type: "user_left",
          username: currentUser,
          adversary: adversary || "",
        })
      );
    }
    gameInProgress = false;
    stopTimer();
    if (sudokuSocket) {
      sudokuSocket.close();
    }
  }
}

export async function initialize() {
  roomName = document.getElementById("room-name");
  const userInfo = await getUser();
  if (userInfo.expired) {
    navigateTo("/login/");
    return;
  }

  if (!roomName) return;

  sudokuSocket = initializeWebSocket();
  currentUser = userInfo.Username;

  if (sudokuSocket) sudokuSocket.onmessage = handleSocketMessage;

  const homeButton = document.getElementById("home");

  homeButton.addEventListener("click", eventFunc);
  window.addEventListener("beforeunload", eventFunc);
}
