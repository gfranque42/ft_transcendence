import { navigateTo } from "../index.js";

export function showModal(timeUsed, winningUser, currentUser) {
  const modal = document.getElementById("game-result-modal");
  const resultTitle = document.getElementById("result-title");
  const resultMessage = document.getElementById("result-message");

  if (winningUser === currentUser) {
    resultTitle.textContent = "You Won!";
    resultMessage.textContent = `Time used: ${timeUsed}`;
  } else {
    resultTitle.textContent = `You Lost!\n${winningUser} is the winner!`;
    resultMessage.textContent = `Winner's time: ${timeUsed}`;
  }

  modal.style.display = "block";
  document.getElementById("close-modal").onclick = function () {
    modal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  };

  document.getElementById("play-again").onclick = function () {
    navigateTo("/sudoku/");
  };
}
