import { navigateTo } from "../index.js";

// TODO: Change the modal to have a play again button and a go back to lobby button
export function showModal(timeUsed, winningUser, currentUser) {
	const modal = document.getElementById("game-result-modal");
	const resultTitle = document.getElementById("result-title");
	const resultMessage = document.getElementById("result-message");

	console.log("users are: ", winningUser, currentUser);
	if (winningUser === currentUser) {
		resultTitle.textContent = "You Won!";
		resultMessage.textContent = `Time used: ${timeUsed}`;
	} else {
		resultTitle.textContent = `You Lost!\n${winningUser} is the winner!`;
		resultMessage.textContent = `Winner's time: ${timeUsed}`;
	}

	// Display the modal
	modal.style.display = "block";

	// Close the modal when the user clicks on the close button or anywhere outside the modal
	document.getElementById("close-modal").onclick = function() {
		modal.style.display = "none";
	};

	window.onclick = function(event) {
		if (event.target === modal) {
			modal.style.display = "none";
		}
	};

	document.getElementById("play-again").onclick = function() {
		navigateTo('/sudoku/');
	};
}
