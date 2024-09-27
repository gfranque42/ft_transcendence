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

	// Add functionality for "Play Again" button
	document.getElementById("play-again").onclick = function() {
		location.reload();  // This reloads the page to start a new game
	};
}

// Example usage when the game is finished
// showModal(true, "12:34", "10:00"); // If player won
// showModal(false, "15:00", "12:34"); // If player lost
