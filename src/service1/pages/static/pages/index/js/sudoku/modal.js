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
		resultTitle.textContent = "You Lost!";
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
		window.location.href = "https://localhost:8083/sudoku/";  // Redirect to the lobby page
	};
}

// Example usage when the game is finished
// showModal(true, "12:34", "10:00"); // If player won
// showModal(false, "15:00", "12:34"); // If player lost
